from utils.formatting.formatter import format_month_from_int_to_string


class UserNotFound(Exception):
    """
    Exception to be raised when a user does not exist within the database.
    """
    def __init__(self, *args):
        self.message = f"User '{args[0]}' does not exist."

    def __str__(self):
        return "User does not exist."


class BadSignIn(Exception):
    """
    Exception to be raised when a sign in is unsuccessful.
    """
    def __init__(self, *args):
        self.message = f"Unsuccessful sign in for '{args[0]}'."

    def __str__(self):
        return "Unable to sign in the user."


class NoTotalBetweenDates(Exception):
    """
    Exception to be raised when the data found between specified dates is Null.
    """
    def __init__(self, *args):
        self.message = f"No data found for the date range {args[0]} - {args[1]}."

    def __str__(self):
        return "No total could be calculated between the dates."


class NoTotalFound(Exception):
    """
    Exception to be raised when there is no total transactions to be found.
    """
    def __init__(self, *args):
        self.message = f"No total could be found for {args[0]}."

    def __str__(self):
        return "No total found."


class NoDataFound(Exception):
    """
    Exception to be raised when no data was to be found.
    """
    def __init__(self, *args):
        self.message = f"No data found for {args[0]}." if args else "No data found."

    def __str__(self):
        return "No data found."


class InvalidMonth(Exception):
    """
    Exception to be raised when a user inputs an invalid month.
    """
    def __init__(self, *args):
        month = str(args[0])

        # convert from 1..12 to 'January'..'December' if an integer is detected.
        if month.isdigit() and (0 < int(month) <= 12):
            month = format_month_from_int_to_string(month)

        self.message = f"Currently no data is available for the month '{month}'."

    def __str__(self):
        return "Invalid month."


class InvalidYear(Exception):
    """
    Exception to be raised when a user inputs an invalid year.
    """
    def __init__(self, *args):
        self.message = f"Currently no data is available for the year '{args[0]}'."

    def __str__(self):
        return "Invalid year."
