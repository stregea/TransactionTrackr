from objects.user.User import User
from objects.interface.dbconn import DB
from objects.user.Currency import get_currency_symbol
from objects.threads.UploadThread import UploadThread
import utils.globals as _globals
from utils.print import print_message, print_error
from utils.enums import Months, SettingsSelection, is_valid_month, month_string_to_enum
from utils.visualizer import visualizer, visualizer_helper
from utils.builders.folderbuilder import create_user_folder
from utils.exceptions import NoDataFound, NoTotalFound, InvalidMonth, InvalidYear, UserNotFound
from utils.dates.dates import get_dates, subtract_days
from utils.averager.averager import calculate_average
from utils.formatting.formatter import format_date_pretty, format_month_enum_to_string
from utils.generators.csv_generator import generate_transaction_files
from menus.user.Settings import Settings


def user_has_data(user: User) -> bool:
    """
    Test to determine if a user has any data
    :param user: The user to check.
    :return: True if the user has data. False otherwise.
    """
    # Determine if the user has any available data.
    try:
        user.get_earliest_transaction_date()
    except Exception:  # excepting NoDataFound here does not work for some reason?
        print_error("No data is currently available.")
        return False
    return True


def is_valid_year(year_to_check: str) -> bool:
    """
    Determine if the passed in year currently exists within the database.
    :param year_to_check: The year to check.
    :return: True if the year exists, false otherwise.
    """
    year_is_valid = False
    db = DB(_globals.DATABASE)
    years = db.fetchall(f"SELECT DISTINCT strftime('%Y', Date) from Transactions;")
    db.close()

    # search through all the years. If the year that was specified exists, set the flag to true.
    for year in years:
        if year_to_check == year[0]:
            year_is_valid = True
            break

    return year_is_valid


def get_month_and_year() -> (Months, str):
    """
    Prompt a user to enter a month and a year.
    :raises InvalidMonth: Exception that is to be raised when user enters an invalid month.
    :raises InvalidYear: Exception that is to be raised when user enters an invalid year.
    :return: A Month enum and the year the user selected.
    """
    month = input("Enter a month:\t")
    month_enum = month_string_to_enum(month)
    if is_valid_month(month_enum):
        year = input("Enter a year:\t")
        if is_valid_year(year):
            return month_enum, year
        else:
            raise InvalidYear(year)
    else:
        raise InvalidMonth(month)


def get_year():
    """
    Prompt a user to enter a year.
    :raises InvalidYear: Exception that is to be raised if a user enters an invalid year.
    :return: The year the user enters.
    """
    year = input("Enter a year:\t")
    if is_valid_year(year):
        return year
    raise InvalidYear(year)


def display_monthly_information(user: User, month: Months, year: str, show_console: bool = False,
                                show_visual: bool = False) -> None:
    """
    Display information regarding the total money spent within a month.
    :param user: The current user.
    :param month: The month to get the information regarding how much was spent.
    :param year: The year corresponding to the month.
    :param show_console: Boolean to determine whether or not to display the information of the total spent
                         in a month to the console.
    :param show_visual: Boolean to determine whether or not to display a visualization of the total spent in the month.
    """
    try:
        # Dictionary that contains the information about all of the transactions in a given month.
        # The key is the day, the value is the total spent on that day.
        transactions_dictionary = visualizer_helper.get_transactions_by_month(month, year, user.id)

        # The total amount of money spent during the specified month.
        total = visualizer_helper.get_monthly_total(month, year, user.id)
    except (NoDataFound, NoTotalFound) as n:
        print_error(n.message)
        return

    # List to hold the dollar values for each day.
    dollars = []

    # List to hold the labels that correspond to each day in the month that had a transaction.
    day_labels = []

    # List of hold the labels that correspond to the dollar values for the transactions.
    dollars_labels = []

    # The type of currency the current user is using.
    currency_symbol = get_currency_symbol(user.currency_id)

    # The title to be displayed on the console and/or the visualization
    title = f"Total spent in {format_month_enum_to_string(month)} {year}: {currency_symbol}{total:,}"

    for date_key in transactions_dictionary:
        day_labels.append(date_key)

    # Sort the labels (YYYY-MM-DD - End of Month)
    day_labels.sort()

    # Add the dollar amount to the corresponding day index, then create a label for that day.
    for day in day_labels:
        value = round(float(transactions_dictionary[day]), 2)
        dollars.append(value)
        dollars_labels.append(f"{currency_symbol}{value:,}")

    # Display each day and then display the total spent for the month
    if show_console:  # TODO: change to function to prevent duplicated code.
        for i, day in enumerate(day_labels):
            print_message(f"{day}:\t{dollars_labels[i]}")
        print_message(f"{title}")

    # Display a visualization of the money spent in the month specified
    if show_visual:
        visualizer.display_bar_chart(title=title,
                                     list_of_values=dollars,
                                     list_of_labels=day_labels,
                                     currency_labels=dollars_labels)


def display_yearly_information(user: User, year: str, show_console: bool = False, show_visual: bool = False) -> None:
    """
    Display information regarding the total money spent within a certain year.
    :param user: The current user.
    :param year: The year to gather information from.
    :param show_console: Boolean to determine whether or not to display the information of the total spent
                         in a year to the console.
    :param show_visual: Boolean to determine whether or not to display a visualization of the total spent in the month.
    """

    try:
        # Dictionary to contain the total transaction values per month given the year
        transactions_dictionary = visualizer_helper.get_transactions_by_year(year, user.id)

        # The total amount of money spent during the specified year.
        total = visualizer_helper.get_yearly_total(year, user.id)
    except (NoDataFound, NoTotalFound) as n:
        print_error(n.message)
        return

    # List to hold the dollar values for each month.
    dollars = []

    # List to hold the labels that correspond to the total number of transactions in each month.
    month_labels = []

    # List of hold the labels that correspond to the dollar values for the transactions.
    dollars_labels = []

    # The type of currency the current user is using.
    currency_symbol = get_currency_symbol(user.currency_id)

    # The title to be displayed on the console and/or the visualization
    title = f"Total Spent in {year}: {currency_symbol}{total:,}"

    for month_name in transactions_dictionary:
        value = round(float(transactions_dictionary[month_name]), 2)
        dollars.append(value)
        dollars_labels.append(f"{currency_symbol}{value:,}")

        # Not formatting month name here since the string is already in the key format for the months dictionary.
        month_labels.append(_globals.months[month_name])

    if show_console:
        for i, month in enumerate(month_labels):
            print_message(f"{month}: {dollars_labels[i]}")
        print_message(f"{title}")

    if show_visual:
        visualizer.display_bar_chart(title=title,
                                     list_of_values=dollars,
                                     list_of_labels=month_labels,
                                     currency_labels=dollars_labels)


def display_information_all_time(user: User, show_console: bool = False, show_visual: bool = False) -> None:
    """
    Display information regarding the total money spent all time.
    :param user: The current user.
    :param show_console: Boolean to determine whether or not to display the information of the total spent
                         in a year to the console.
    :param show_visual: Boolean to determine whether or not to display a visualization of the total spent in the month.
    """
    try:
        transactions_dictionary = visualizer_helper.get_transactions_all_time(user.id)
        total = visualizer_helper.get_total_all_time(user.id)
    except NoDataFound as ndf:
        print_error(ndf.message)
        return

    # List to hold the total dollar values for each available year.
    dollars = []

    # List to hold the labels that correspond to the total number of transactions in each year.
    year_labels = []

    # List of hold the labels that correspond to the dollar values for the transactions.
    dollars_labels = []

    # The type of currency the current user is using.
    currency_symbol = get_currency_symbol(user.currency_id)

    # The title to be displayed on the console and/or the visualization
    title = f"Total Spent All Time: {currency_symbol}{total:,}"

    for year in transactions_dictionary:
        value = round(float(transactions_dictionary[year]), 2)
        dollars.append(value)
        dollars_labels.append(f"{currency_symbol}{value:,}")
        year_labels.append(year)

    if show_console:
        for i, year in enumerate(year_labels):
            print_message(f"{year}: {dollars_labels[i]}")
        print_message(f"{title}")

    if show_visual:
        visualizer.display_bar_chart(title=title,
                                     list_of_values=dollars,
                                     list_of_labels=year_labels,
                                     currency_labels=dollars_labels)


class Menu:
    """
    This class serves as the main menu for the user.
    """

    def __init__(self, user: User, show_console=False, show_visual=False) -> None:
        self.user = user
        self.show_console = show_console
        self.show_visual = show_visual

    def display_money_spent_per_month(self) -> None:
        """
        Menu option that will display information based on a specified month. (Menu option #1).
        """
        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        try:
            month, year = get_month_and_year()
        except (InvalidMonth, InvalidYear) as e:
            print_error(e.message)
            return

        display_monthly_information(user=self.user,
                                    month=month,
                                    year=year,
                                    show_console=self.show_console,
                                    show_visual=self.show_visual)

    def display_money_spent_per_year(self) -> None:
        """
        Menu option that will display yearly information. (Menu option #2).
        """
        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        try:
            year = get_year()
        except InvalidYear as iy:
            print_error(iy.message)
            return
        display_yearly_information(self.user, year, show_console=self.show_console, show_visual=self.show_visual)

    def display_money_spent_all_time(self) -> None:
        """
        Menu option that will display the total money spent all time. (Menu option #2).
        """
        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        display_information_all_time(self.user, show_console=self.show_console, show_visual=self.show_visual)

    def display_daily_average_spending_per_month(self) -> None:
        """
        Menu option that will display the user's daily average spending over a specified month
        as well as a Pie Chart to show where most of the money was spent.
        """
        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        try:
            month, year = get_month_and_year()
        except (InvalidMonth, InvalidYear) as e:
            print_error(e.message)
            return

        # Get the starting and end dates for the user-specified month.
        dates = get_dates(month, year)

        # Get the user's specified currency
        currency_symbol = get_currency_symbol(self.user.currency_id)
        try:
            # get the monthly average spent per day.
            monthly_average = calculate_average(start_date=dates[0],
                                                end_date=dates[1],
                                                user_id=self.user.id,
                                                exception_type="monthly average")
        except NoDataFound as ndf:
            print_message(ndf.message)
            return

        print_message(
            f"Your daily average spending for {format_month_enum_to_string(month)} {year} is: {currency_symbol}{monthly_average:,}")

    def display_daily_average_spending_per_year(self) -> None:
        """
        Menu option that will display the user's daily average spending over a specified year.
        """
        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        try:
            year = get_year()
        except InvalidYear as iy:
            print_error(iy.message)
            return

        # Get the user's specified currency
        currency_symbol = get_currency_symbol(self.user.currency_id)

        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        dates = (start_date, end_date)
        try:
            yearly_average = calculate_average(start_date=dates[0],
                                               end_date=dates[1],
                                               user_id=self.user.id,
                                               exception_type="yearly average")
        except NoDataFound as ndf:
            print_error(ndf.message)
            return

        print_message(f"Your daily average spending for {year} is: {currency_symbol}{yearly_average:,}")

    def display_daily_average_spending_all_time(self) -> None:
        """
        Menu option that will display the user's all-time daily average spending.
        """

        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        try:
            start_date = self.user.get_earliest_transaction_date()
            end_date = self.user.get_latest_transaction_date()

            all_time_average = calculate_average(start_date=start_date,
                                                 end_date=end_date,
                                                 user_id=self.user.id,
                                                 exception_type="all time average")
        except NoDataFound as ndf:
            print_error(ndf.message)
            return

        currency_symbol = get_currency_symbol(self.user.currency_id)
        print_message(f"Your all-time daily average spending is: {currency_symbol}{all_time_average:,}")

    def display_daily_average_over_n_days(self) -> None:
        """
        Menu option that will allow a user to determine the user's daily spending average over a certain number of days.
        """

        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        number_of_days = input("How many days would you like to go back?\t")

        if number_of_days.isdigit():
            try:
                earliest_date = self.user.get_earliest_transaction_date()
                end_date = self.user.get_latest_transaction_date()

                start_date = subtract_days(starting_date=end_date, days=int(number_of_days))

                # if a user selects a day that is older than their oldest transaction,
                # select the date associated with their oldest transaction.
                if start_date < earliest_date:
                    formatted_start_date = format_date_pretty(start_date)
                    formatted_earliest_date = format_date_pretty(earliest_date)
                    print_message(
                        f"The selected date is older than {formatted_earliest_date}, which is the oldest known transaction date.")
                    print_error(
                        f"Using '{formatted_earliest_date}' to calculate the average instead of '{formatted_start_date}'...")
                    start_date = earliest_date

                daily_average = calculate_average(start_date=start_date,
                                                  end_date=end_date,
                                                  user_id=self.user.id,
                                                  exception_type="all time average")
            except NoDataFound as ndf:
                print_error(ndf.message)
                return

            currency_symbol = get_currency_symbol(self.user.currency_id)
            formatted_start_date = format_date_pretty(start_date)
            formatted_end_date = format_date_pretty(end_date)
            print_message(f"Using the latest data from: {formatted_end_date}...")
            print_message(
                f"Your daily average spending between {formatted_start_date} - {formatted_end_date} is: {currency_symbol}{daily_average:,}")

        elif number_of_days.startswith("-") and number_of_days[1:].isdigit():  # if a negative number was entered.
            print_error("Please enter a positive integer.")

        else:
            print_error("Invalid number of days to go back.")

    def display_daily_average_over_period(self):

        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        try:
            earliest_date = self.user.get_earliest_transaction_date()
            latest_date = self.user.get_latest_transaction_date()
        except NoDataFound as ndf:
            print_error(ndf.message)
            return

        try:
            print_message("Select your first month/year:")
            month1, year1 = get_month_and_year()
            print_message("Select your second month/year:")
            month2, year2 = get_month_and_year()
        except (InvalidMonth, InvalidYear) as e:
            print_error(e.message)
            return

        starting_date = get_dates(month1, year1)[0]
        ending_date = get_dates(month2, year2)[1]

        # If the starting date is greater than the ending date, swap the dates by:
        #   changing the starting_date to the beginning of the second selected month,
        #   then change the ending_date to the end of the first month.
        if starting_date > ending_date:
            starting_date = get_dates(month2, year2)[0]
            ending_date = get_dates(month1, year1)[1]

        # If starting or ending day < earliest date
        if starting_date < earliest_date:
            starting_date = earliest_date
        if ending_date < earliest_date:
            ending_date = earliest_date

        # If starting date or ending date > latest date, use the latest date and the option
        if starting_date > latest_date:
            starting_date = latest_date
        if ending_date > latest_date:
            ending_date = latest_date

        try:
            average_over_period = calculate_average(start_date=starting_date,
                                                    end_date=ending_date,
                                                    user_id=self.user.id)
        except NoDataFound as ndf:
            print(ndf.message)
            return

        formatted_start_date = format_date_pretty(starting_date)
        formatted_end_date = format_date_pretty(ending_date)
        currency_symbol = get_currency_symbol(self.user.currency_id)
        print_message(
            f"Your daily average spending between {formatted_start_date} - {formatted_end_date} is: {currency_symbol}{average_over_period:,}")

    def display_total_number_of_transactions(self):
        # Determine if the user has any available data.
        if not user_has_data(self.user):
            return

        try:
            earliest_date = format_date_pretty(self.user.get_earliest_transaction_date())
            latest_date = format_date_pretty(self.user.get_latest_transaction_date())
            print_message(
                f"You have made {self.user.get_total_transactions()} total transactions between {earliest_date} and {latest_date}")
        except NoDataFound as ndf:
            print_error(ndf.message)
            return

    def run(self) -> bool:
        """
        Run the driver to this object.
        """
        # show where money is most spent + include all time total (merchant) -- maybe implement as pie chart
        # include option to perform query's -- make it dynamic
        print_message(f"--- Welcome, {self.user.username}! ---")
        print_message("Enter a number for the following prompt:")

        running = True
        while running:
            print_message("1.\tShow money spent per month")
            print_message("2.\tShow money spent per year")
            print_message("3.\tShow money spent all time")
            print_message("4.\tTotal daily average spending per month")
            print_message("5.\tTotal daily average spending per year")
            print_message("6.\tTotal daily average spending all time")
            print_message("7.\tTotal daily average spending over number of days.")
            print_message("8.\tTotal daily average spending over period.")
            print_message("9.\tDisplay total number of transactions")
            print_message("10.\tUpload Data")
            print_message("11.\tSettings")
            print_message("12.\tSign out")
            print_message("13.\tQuit")

            response = input()

            if response == '1':  # display a chart of the total money spent in a given month.
                self.display_money_spent_per_month()
            elif response == '2':  # display a chart of the total money spent in a given year.
                self.display_money_spent_per_year()
            elif response == '3':  # display a chart of all of the money spent.
                self.display_money_spent_all_time()
            elif response == '4':  # display the daily average spending that a user has made.
                self.display_daily_average_spending_per_month()
            elif response == '5':  # display the daily average spending that a user has made.
                self.display_daily_average_spending_per_year()
            elif response == '6':  # display the daily average spending that a user has made.
                self.display_daily_average_spending_all_time()
            elif response == '7':  # display the daily average spending that a user has made.
                self.display_daily_average_over_n_days()
            elif response == '8':  # display the daily average spending that a user has made.
                self.display_daily_average_over_period()
            elif response == '9':  # display the daily average spending that a user has made.
                self.display_total_number_of_transactions()
            elif response == '10' or response.lower() == 'upload':  # upload data to the database from the 'upload' directory.
                # UserNotFound Exception should never be caught here, but it is still being handled.
                try:
                    create_user_folder(user=self.user)
                    UploadThread(self.user).run()
                except UserNotFound as unf:
                    print_error(unf.message)
            elif response == '11':  # User settings
                selection = Settings(self.user).run()

                # immediately exit the user menu if the user had selected to delete their account.
                if selection.value == SettingsSelection.DELETE_ACCOUNT.value:
                    running = False

            elif response == '12' or response.lower() == 'signout':
                self.user.sign_out()
                running = False  # set running to false, then return to sign in screen.
            elif response == '13' or response.lower() == 'quit':
                self.user.sign_out()
                exit(0)  # exit the main program successfully.
            else:
                print_error("Unknown Command.")

        return not running
