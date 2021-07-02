from objects.BaseObject import BaseObject
from objects.interface.dbconn import DB
import utils.globals as _globals
from utils.enums import Tables
from utils.logger.logger import log


class Currency(BaseObject):
    """
    Class that will be used to construct a Currency object.
    """

    def __repr__(self) -> str:
        return super(Currency, self).__repr__()

    def __str__(self) -> str:
        return self.acronym

    def __init__(self, db: DB, values: list) -> None:
        """
        Construct a form of Currency.
        :param db: The database connection.
        :param values: The values to assign.
        """
        super(Currency, self).__init__()
        self.db = db
        self.acronym = values[0]
        self.name = values[1]
        self.symbol = values[2]

    def to_list(self) -> list:
        """
        Create a list representation of this object.
        :return: a list containing the components corresponding to the table this
                 object corresponds to.
        """
        return [self.acronym, self.name, self.symbol]

    def to_tuple(self) -> tuple:
        """
        Create a tuple representation of this object.
        :return: a tuple containing the components corresponding to the table this
                 object corresponds to.
        """
        return (self.acronym, self.name, self.symbol)

    def to_dictionary(self) -> dict:
        """
        Create a dictionary representation of this object.
        :return: a dictionary containing the components corresponding to the table this
                 object corresponds to.
        """
        return {
            'acronym': self.acronym,
            'name': self.name,
            'symbol': self.symbol
        }

    def insert_to_db(self) -> None:
        """
        Insert this form of currency into the database.
        """
        query = '''INSERT INTO Currencies(Acronym, Name, Symbol)
                   VALUES (?,?,?)'''
        self.db.commit(query, values=self.to_tuple())
        log(f"{self.name} ({self.acronym}) is now a supported currency.", level="debug")

    def exists_in_db(self) -> bool:
        """
        Check to see if this object exists within the db.
        :return: true if in db, false otherwise.
        """
        query = '''SELECT * 
                   FROM Currencies
                   WHERE Acronym=? AND Name=? AND Symbol=?'''
        return len(self.db.fetchall(query, values=self.to_tuple())) > 0

    def get_id(self) -> int:
        """
        Retrieve the id of this object from the database.
        :return: The id associated with a Currency object.
        """
        query = '''SELECT id 
                   FROM Currencies 
                   WHERE Acronym=? AND Name=? AND Symbol=?'''
        return int(self.db.fetchall(query, values=self.to_tuple())[0][0])

    def get_type(self) -> str:
        """
        Retrieve the string representation of this objects' type.
        :return: The type associated with the object.
        """
        return Tables.CURRENCY.name


def get_currency(acronym: str) -> Currency:
    """
    Retrieve a currency object from the database.
    :param acronym: The acronym associated with a currency (USD, EUR, JPY, etc.)
    :return: A currency object.
    """
    db = DB(_globals.DATABASE)
    query = """SELECT Acronym, Name, Symbol 
                FROM Currencies
                WHERE Acronym=?"""
    values = list(db.fetchall(query, values=(acronym.upper(),))[0])
    currency = Currency(db, values=values)
    return currency


def get_currency_symbol(currency_id: int) -> str:
    """
    Retrieve the symbol used for a currency.
    :param currency_id: The id of the currency to retrieve the symbol for.
    :return: The symbol associated with a currency.
    """
    db = DB(_globals.DATABASE)
    query = """SELECT Symbol
               FROM Currencies
               WHERE id=?"""
    symbol = db.fetchall(query, values=(currency_id,))
    db.close()
    return symbol[0][0]


def get_currency_acronym(currency_id: int) -> str:
    """
    Retrieve the acronym used for a currency.
    :param currency_id: The id of the currency to retrieve the symbol for.
    :return: The acronym associated with a currency.
    """
    db = DB(_globals.DATABASE)
    query = """SELECT Acronym
               FROM Currencies
               WHERE id=?"""
    acronym = db.fetchall(query, values=(currency_id,))
    db.close()
    return acronym[0][0]


def is_valid_currency(currency_acronym: str) -> bool:
    """
    Determine if a form of currency exists in the database.
    :param currency_acronym: The currency to check.
    :return: True if the currency exists, False otherwise.
    """
    db = DB(_globals.DATABASE)
    query = """SELECT *
               FROM Currencies
               WHERE Acronym=?;"""
    validity = len(db.fetchall(query, values=(currency_acronym.upper(),))) > 0
    db.close()
    return validity


def get_currency_from_input() -> str:
    """
    Get a currency type from user input.
    :return: The acronym used for the currency the user selected.
    """
    currency = input("What form of currency do you use? (USD, EUR, JPY, etc.)\n").upper()

    bad_input = not is_valid_currency(currency)

    while bad_input:
        currency = input("The previously entered currency is either not support or valid. Please enter again.\n")
        bad_input = not is_valid_currency(currency)

    return currency
