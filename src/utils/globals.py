import os
from utils.enums import Months

# Database path
DATABASE = os.path.abspath('../receipt.db')

# csv containing the currencies this application can support
CURRENCIES = os.path.abspath('../src/utils/helper_files/csv/currencies.csv')

# The folder the user will upload their files to
UPLOAD_FOLDER = os.path.abspath('../Upload')
APPLE_UPLOAD_FOLDER = os.path.abspath('../Upload/Apple')
ESL_UPLOAD_FOLDER = os.path.abspath('../Upload/ESL')

# List to contain all of the supported upload types
FOLDER_UPLOADS = [
    APPLE_UPLOAD_FOLDER,
    ESL_UPLOAD_FOLDER
]

# The folder that will hold all of the users data
USERS_FOLDER = os.path.abspath('../Users')

# The log containing the pertinent information about the program
LOG_FILE = os.path.abspath('../receipt.log')

CREATE_CURRENCY_TABLE = '''CREATE TABLE IF NOT EXISTS Currencies(
                            id integer PRIMARY KEY AUTOINCREMENT,
                            Acronym text NOT NULL,
                            Name text NOT NULL,
                            Symbol text
                        );'''

CREATE_USER_TABLE = '''CREATE TABLE IF NOT EXISTS Users(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        Username text NOT NULL,
                        Password text NOT NULL,
                        Firstname text NOT NULL,
                        Surname text NOT NULL,
                        Currency_id integer,
                        Has_First_Sign_In integer NOT NULL,
                        Account_Created timestamp,
                        Last_Sign_In timestamp,
                        FOREIGN KEY(Currency_id) references Currencies(id)
                    );'''

# CREATE_CSV_TABLE = '''CREATE TABLE IF NOT EXISTS CSVFiles(
#                         id integer PRIMARY KEY AUTOINCREMENT,
#                         Name text NOT NULL,
#                         User_id integer,
#                         FOREIGN KEY(User_id) references Users(id)
#                     );'''


CREATE_APPLE_TABLE = '''CREATE TABLE IF NOT EXISTS AppleReceipts(
                          id integer PRIMARY KEY AUTOINCREMENT,
                          Transaction_Date text NOT NULL,
                          Clearing_Date text NOT NULL,
                          Description text NOT NULL,
                          Merchant text NOT NULL,
                          Category text NOT NULL,
                          Type text NOT NULL,
                          Amount text NOT NULL,
                          Card_Type text NOT NULL,
                          Is_Payment integer NOT NULL,
                          Is_Transaction integer NOT NULL,
                          User_id integer NOT NULL,
                          FOREIGN KEY(User_id) references Users(id)
                        );'''

CREATE_ESL_TABLE = '''CREATE TABLE IF NOT EXISTS ESLReceipts(
                        id integer PRIMARY KEY AUTOINCREMENT,
                        Transaction_Number text NOT NULL,
                        Date text NOT NULL,
                        Description text NOT NULL,
                        Memo text NOT NULL,     
                        Amount_Debit text NOT NULL,
                        Amount_Credit text NOT NULL,
                        Balance text NOT NULL,
                        Check_Number text NOT NULL,
                        Fees text NOT NULL,
                        Card_Type text NOT NULL,
                        Is_Payment integer NOT NULL,
                        Is_Transaction integer NOT NULL,
                        User_id integer NOT NULL,
                        FOREIGN KEY(User_id) references Users(id)
                    );'''

CREATE_TRANSACTIONS_TABLE = '''CREATE TABLE IF NOT EXISTS Transactions(
                                id integer PRIMARY KEY AUTOINCREMENT, 
                                Date text NOT NULL,
                                Amount text NOT NULL,
                                Card_Type text NOT NULL,
                                Merchant text NOT NULL,
                                Description text NOT NULL,
                                ESL_id integer,
                                Apple_id integer,
                                User_id integer NOT NULL,
                                FOREIGN KEY(User_id) references Users(id),
                                FOREIGN KEY(ESL_id) references ESLReceipts(id),
                                FOREIGN KEY(Apple_id) references AppleReceipts(id)
                           );'''

# List to contain all of the create table commands
TABLES = [
    CREATE_CURRENCY_TABLE,
    CREATE_USER_TABLE,
    # CREATE_CSV_TABLE,
    CREATE_APPLE_TABLE,
    CREATE_ESL_TABLE,
    CREATE_TRANSACTIONS_TABLE
]

# List to contain the supported account types
ACCOUNTS = [
    "Apple",
    "ESL"
]

# Dictionary to contain the Enum of a month as a Key, and the Name of the month as a value.
months = {
    Months.JANUARY.name: "January",
    Months.FEBRUARY.name: "February",
    Months.MARCH.name: "March",
    Months.APRIL.name: "April",
    Months.MAY.name: "May",
    Months.JUNE.name: "June",
    Months.JULY.name: "July",
    Months.AUGUST.name: "August",
    Months.SEPTEMBER.name: "September",
    Months.OCTOBER.name: "October",
    Months.NOVEMBER.name: "November",
    Months.DECEMBER.name: "December"
}

# Dictionary to contain the Enum of a month as a Key, and the Number of the corresponding month as the value.
months_numerical = {
    Months.JANUARY.name: "01",
    Months.FEBRUARY.name: "02",
    Months.MARCH.name: "03",
    Months.APRIL.name: "04",
    Months.MAY.name: "05",
    Months.JUNE.name: "06",
    Months.JULY.name: "07",
    Months.AUGUST.name: "08",
    Months.SEPTEMBER.name: "09",
    Months.OCTOBER.name: "10",
    Months.NOVEMBER.name: "11",
    Months.DECEMBER.name: "12"
}
