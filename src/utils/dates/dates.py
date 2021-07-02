from datetime import datetime, timedelta
from objects.interface.dbconn import DB
from utils import globals as _globals
from utils.enums import Months
from utils.exceptions import NoTotalBetweenDates
from utils.formatting.formatter import format_date_pretty


def subtract_days(starting_date: str, days: int) -> str:
    """
    Subtract n number of days from a starting date.
    :param starting_date: The starting date.
    :param days: The number of days to subtract.
    :return: The date representation of the date created from subtracting the days from the start date.
    """
    return str((datetime.strptime(starting_date, "%Y-%m-%d") - timedelta(days)).date())


def is_leap_year(year: str) -> bool:
    """
    Helper function used to determine if a string is a leap year or not.
    :param year: The year to check.
    :return: True if a leap year, false otherwise.
    """
    if int(year) % 4 == 0:
        if int(year) % 100 == 0:
            if int(year) % 400 == 0:
                return True
            return False
        return True
    return False


def get_starting_dates() -> dict:
    """
    Retrieve a dictionary of months with their starting dates.
    :return: A dictionary  containing months as the keys, and date as the value.
             Note: the date is in ##-## format.
    """
    return {
        Months.JANUARY.name: "01-01",
        Months.FEBRUARY.name: "02-01",
        Months.MARCH.name: "03-01",
        Months.APRIL.name: "04-01",
        Months.MAY.name: "05-01",
        Months.JUNE.name: "06-01",
        Months.JULY.name: "07-01",
        Months.AUGUST.name: "08-01",
        Months.SEPTEMBER.name: "09-01",
        Months.OCTOBER.name: "10-01",
        Months.NOVEMBER.name: "11-01",
        Months.DECEMBER.name: "12-01",
    }


def get_ending_dates(leap_year: bool = False) -> dict:
    """
    Retrieve a dictionary of months with their starting dates.
    :param leap_year: Boolean to determine to return a dictionary containing values for a leap-year.
    :return: A dictionary  containing months as the keys, and date as the value.
             Note: the date is in ##-## format.
    """
    ending_dates = {
        Months.JANUARY.name: "01-31",
        Months.FEBRUARY.name: "02-28",
        Months.MARCH.name: "03-31",
        Months.APRIL.name: "04-30",
        Months.MAY.name: "05-31",
        Months.JUNE.name: "06-30",
        Months.JULY.name: "07-31",
        Months.AUGUST.name: "08-31",
        Months.SEPTEMBER.name: "09-30",
        Months.OCTOBER.name: "10-31",
        Months.NOVEMBER.name: "11-30",
        Months.DECEMBER.name: "12-31",
    }

    if leap_year:
        ending_dates['february'] = "02-29"

    return ending_dates


def get_dates(month: Months, year: str) -> (str, str):
    """
    Return the starting and ending dates to a specified month.
    :param month: The month to retrieve the dates for.
    :param year: The year corresponding to the month.
    :return: The start and end dates for the specified date.
    """
    starting_date = get_starting_dates()[month.name]
    ending_date = get_ending_dates(leap_year=is_leap_year(year))[month.name]
    return f"{year}-{starting_date}", f"{year}-{ending_date}"


def get_all_years(user_id: int) -> list:
    """
    Get all the years available to a user.
    :param user_id: The id of the user.
    :return: A list of tuples that contain every year that contains transactional data.
    """
    db = DB(_globals.DATABASE)
    years = db.fetchall(f"SELECT DISTINCT strftime('%Y', Date) "
                        f"FROM Transactions "
                        f"WHERE User_id=?;", values=(user_id,))
    db.close()
    years.sort()  # sort the tuples containing the years in ascending value.
    return years


def get_total_between_dates(dates: tuple, user_id: int) -> float:
    """
    Get the total money spent between two specified dates.
    :param dates: The tuple containing the starting and ending dates. Note: dates[0] - start_date, dates[1] - end_date.
    :param user_id: The id of the current user.
    :raises NoTotalBetweenDates: Exception to be raised when there is no data between the start and end dates.
    :return: The total money spent between starting_date and ending_date
    """
    db = DB(_globals.DATABASE)
    total = db.fetchall(
        f"SELECT SUM(Amount) "
        f"FROM Transactions "
        f"WHERE Date BETWEEN DATE('{dates[0]}') AND DATE('{dates[1]}') AND User_id=?;",
        values=(user_id,))[0][0]
    db.close()

    if total is not None:
        return round(float(total), 2)

    raise NoTotalBetweenDates(format_date_pretty(dates[0]), format_date_pretty(dates[1]))
