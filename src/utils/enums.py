from enum import Enum, auto


class Tables(Enum):
    CURRENCY = auto()
    USER = auto()
    APPLE = auto()
    ESL = auto()
    TRANSACTION = auto()
    FILE = auto()


class Months(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12
    INVALID = -1


class Charts(Enum):
    """
    TODO: Add more charts later.
    This class is used to represent the different types of supported charts.
    """
    BAR = auto()
    HISTOGRAM = auto()
    PIE = auto()


class SettingsSelection(Enum):
    CHANGE_USERNAME = 1
    CHANGE_PASSWORD = 2
    CHANGE_NAME = 3
    CHANGE_CURRENCY = 4
    UPLOAD_RANDOM_DATA = 5
    DELETE_ACCOUNT = 6
    EXIT = -1


def month_string_to_enum(month: str) -> Months:
    """
    Convert a month string into its corresponding enum type.
    :param month: The month to convert.
    :return: The corresponding 'Months' enumerated type.
    """
    m = month.lower()
    if m == "january" or m == "01" or m == "1":
        return Months.JANUARY
    elif m == "february" or m == "02" or m == "2":
        return Months.FEBRUARY
    elif m == "march" or m == "03" or m == "3":
        return Months.MARCH
    elif m == "april" or m == "04" or m == "4":
        return Months.APRIL
    elif m == "may" or m == "05" or m == "5":
        return Months.MAY
    elif m == "june" or m == "06" or m == "6":
        return Months.JUNE
    elif m == "july" or m == "07" or m == "7":
        return Months.JULY
    elif m == "august" or m == "08" or m == "8":
        return Months.AUGUST
    elif m == "september" or m == "09" or m == "9":
        return Months.SEPTEMBER
    elif m == "october" or m == "10":
        return Months.OCTOBER
    elif m == "november" or m == "11":
        return Months.NOVEMBER
    elif m == "december" or m == "12":
        return Months.DECEMBER
    else:
        return Months.INVALID


def is_valid_month(month_to_check: Months) -> bool:
    """
    Determine if the passed in month is a valid month.
    :param month_to_check: The month to check.
    :return: True if a valid month, false otherwise.
    """
    return not month_to_check.name == Months.INVALID.name
