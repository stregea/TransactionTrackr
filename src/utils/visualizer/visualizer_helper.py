from objects.interface.dbconn import DB
from utils import globals as _globals
from utils.enums import Months, month_string_to_enum
from utils.exceptions import NoDataFound, NoTotalBetweenDates, NoTotalFound
from utils.logger.logger import log
from utils.dates.dates import get_dates, get_total_between_dates, get_all_years
from utils.formatting.formatter import format_month_enum_to_string, format_date_pretty


def dictionary_has_data(dictionary_to_check: dict) -> bool:
    """
    Check to see if the dictionary has any data.
    :param dictionary_to_check: The dictionary to check.
    :return: True if there is any data. False otherwise.
    """
    return len(dictionary_to_check.values()) > 0


def get_monthly_total(month: Months, year: str, user_id: int) -> float:
    """
    Get the total spent from a given month.
    :param month: The month to retrieve the total transactions from.
    :param year: The year associated with the month.
    :param user_id: The id of the current user.
    :raises NoTotalFound: Exception to be raised when there is no transaction data found for the monthly total.
    :return: The total spent in a month.
    """
    try:
        total_for_the_month = get_total_between_dates(get_dates(month, year), user_id)
        return total_for_the_month
    except NoTotalBetweenDates:
        raise NoTotalFound(f"{_globals.months[month.name]} {year}")


def get_yearly_total(year: str, user_id: int) -> float:
    """
    :param year: The year to retrieve the total transactions from.
    :param user_id: The id of the current user.
    :raises NoTotalFound: Exception that is raised when no total transactions is found for the year.
    :return: The total spent in a year.
    """
    starting_date = f"{year}-01-01"
    ending_date = f"{year}-12-31"
    dates = (starting_date, ending_date)
    try:
        total_for_the_year = get_total_between_dates(dates, user_id)
        return total_for_the_year
    except NoTotalBetweenDates:
        raise NoTotalFound(year)


def get_total_all_time(user_id: int) -> float:
    """
    Calculate the total spent all time for a user.
    :param user_id: The id of the user.
    :raises NoDataFound: Exception that is raised when there is no data to be found all time.
    :return: The total spent all time.
    """
    years = get_all_years(user_id)

    # if there is any data.
    if len(years) > 0:
        total_all_time = 0.0
        for year_tuple in years:
            year = year_tuple[0]

            # Add only the years that have data to the total.
            try:
                total_all_time += get_yearly_total(year, user_id)
            except NoTotalFound as ntf:
                log(f"User:{user_id}\t:\t{ntf.message}", level="warning")
                continue

        if total_all_time > 0:
            return round(total_all_time, 2)

    raise NoDataFound("all time")


def get_transactions_by_month(month: Months, year: str, user_id: int) -> dict:
    """
    Retrieve all of the transactions given a specified month.
    :param month: The month to retrieve the transactions from.
    :param year: The year associated with the month.
    :param user_id: The id of the current user.
    :raises NoDataFound: Exception to be raised when the query returns no transactional data.
    :return: A dictionary containing the transactions for a given month.
             The dictionary is set up as: {day : transaction_total}
    """
    dates = get_dates(month, year)
    db = DB(_globals.DATABASE)
    daily_transactions = db.fetchall(
        f"SELECT Date, Amount "
        f"FROM Transactions "
        f"WHERE Date BETWEEN DATE('{dates[0]}') AND DATE('{dates[1]}') AND User_id=?;",
        values=(user_id,))
    db.close()

    transactions_dictionary = {}

    # build the daily transactions dictionary
    for transaction in daily_transactions:
        day = transaction[0]
        amount = float(transaction[1])

        # if the current day isn't in the dictionary, set to that amount. Otherwise add to the previous amount.
        if day not in transactions_dictionary:
            transactions_dictionary[day] = amount
        else:
            transactions_dictionary[day] += amount

    if dictionary_has_data(transactions_dictionary):
        return transactions_dictionary

    raise NoDataFound(f"{format_month_enum_to_string(month)} {year}")


def get_transactions_by_year(year: str, user_id: int) -> dict:
    """
    Retrieve all of the total monthly transactions in a given year.
    :param year: The year to retrieve the transactions from.
    :param user_id: The id of the current user.
    :raises NoDataFound: Exception to be raised when the query returns no transactional data.
    :return: A dictionary containing all of the monthly totals.
             The dictionary is set up as: {month : total}
    """
    transactions_dictionary = {}
    for month in _globals.months:

        # Add only the months that have data to the dictionary.
        try:
            transactions_dictionary[month] = get_monthly_total(month_string_to_enum(month), year, user_id)
        except NoTotalFound as ntf:
            log(f"User:{user_id}\t:\t{ntf.message}", level="warning")
            continue

    # return the dictionary if there is any information, otherwise raise the NoDataFound Exception
    if dictionary_has_data(transactions_dictionary):
        return transactions_dictionary

    raise NoDataFound(year)


def get_transactions_all_time(user_id: int) -> dict:
    """
    Retrieve all of the yearly total transactions all time.
    :param user_id: The id of the current user.
    :raises NoDataFound: Exception to be raised when the query returns no transactional data.
    :return: A dictionary containing all of the monthly totals.
             The dictionary is set up as: {year : total}
    """
    transactions_dictionary = {}

    years = get_all_years(user_id)

    # if there is any data.
    if len(years) > 0:
        for year_tuple in years:
            year = year_tuple[0]

            # Add only the years that have data to the dictionary.
            try:
                transactions_dictionary[year] = get_yearly_total(year, user_id)
            except NoTotalFound as ntf:
                log(f"User:{user_id}\t:\t{ntf.message}", level="warning")
                continue

        # return the dictionary if there is any information, otherwise raise the NoDataFound Exception
        if dictionary_has_data(transactions_dictionary):
            return transactions_dictionary

    raise NoDataFound("all time")


def get_merchant_information(dates: tuple, user_id: int) -> dict:
    """
    Retrieve the transactional information regarding where the money was spent and how much was spent.
    :param dates: The tuple containing the starting and ending dates. Note: dates[0] - start_date, dates[1] - end_date.
    :param user_id: The id of the current user.
    :raises NoDataFound: Exception to be raised when the query returns no transactional data.
    :return: A dictionary containing all of the merchant information.
             The dictionary is set up as: {merchant : total_spent}
    """
    db = DB(_globals.DATABASE)

    query = f"""
            SELECT Merchant, Amount
            FROM Transactions
            WHERE User_id=? 
                  AND Date BETWEEN DATE('{dates[0]}') AND DATE('{dates[1]}');
            """
    list_of_merchants = db.fetchall(query, values=(user_id,))
    db.close()

    merchants = {}
    for merchant_info in list_of_merchants:
        merchant = merchant_info[0]
        total_spent = round(float(merchant_info[1]), 2)
        if merchant in merchants:
            merchants[merchant] += total_spent
        else:
            merchants[merchant] = total_spent

    if dictionary_has_data(merchants):
        return merchants

    raise NoDataFound(f"{format_date_pretty(dates[0])} - {format_date_pretty(dates[1])}")
