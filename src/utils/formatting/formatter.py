import utils.globals as _globals
from utils.enums import Months, month_string_to_enum


def format_month_enum_to_string(month: Months):
    """
    Reformat a 'Months' enum into it's string representation.
    :param month: The enum to reformat.
    :return: The string representation of the enumerated type.
    """
    return _globals.months[month.name]


def format_month_from_int_to_string(month: str):
    """
    Convert a month that is in the form of 1...12 to 'January'...'December'
    :param month: The month to convert.
    :return: The string representation of a month from an integer representation.
    """
    return _globals.months[month_string_to_enum(month).name]


def format_date(date: str):
    """
    This function formats dates that are in MM-DD-YYYY format,
    and will convert to YYYY-MM-DD, which is required sqlite.
    :param date: The date to modify.
    :return: The modified string.
    """
    tmp = date.split("/")
    return "{}-{}-{}".format(tmp[2], tmp[0], tmp[1])


def format_date_pretty(date_to_format: str) -> str:
    """
    Format a date that is in the format YYYY-MM-DD into: 'Name_Of_Month Day, Year'
    :param date_to_format: The date to convert.
    :return: An easier to read format of the date_to_format.
    """
    date_array = date_to_format.split("-")

    day = date_array[2]
    month = format_month_from_int_to_string(date_array[1])
    year = date_array[0]

    return f"{month} {day}, {year}"
