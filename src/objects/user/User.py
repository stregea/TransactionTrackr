from datetime import datetime
from objects.BaseObject import BaseObject
from objects.interface.dbconn import DB
from utils.enums import Tables
from utils.logger.logger import log
from utils.exceptions import NoDataFound


class User(BaseObject):
    """
    Class that will be used to construct the User object.
    """

    def __repr__(self) -> str:
        return super(User, self).__repr__()

    def __str__(self) -> str:
        return super(User, self).__str__()

    def __init__(self, db: DB, username: str, password_hash: str) -> None:
        """
        Construct a User.
        :param db: The database connection.
        """
        super(User, self).__init__()
        self.db = db
        self.id = -1
        self.username = username
        self.password = password_hash
        self.firstname = ""
        self.surname = ""
        self.currency_id = -1
        self.has_first_sign_in = False
        self.account_created = None
        self.last_sign_in = None
        self.is_signed_in = False

    def to_list(self) -> list:
        """
        Create a list representation of this object.
        :return: a list containing the components corresponding to the table this
                 object corresponds to.
        """
        return [
            self.username, self.password, self.firstname, self.surname, self.currency_id,
            int(self.has_first_sign_in), self.account_created, self.last_sign_in
        ]

    def to_tuple(self) -> tuple:
        """
        Create a tuple representation of this object.
        :return: a tuple containing the components corresponding to the table this
                 object corresponds to.
        """
        return (self.username, self.password, self.firstname, self.surname, self.currency_id,
                int(self.has_first_sign_in), self.account_created, self.last_sign_in)

    def to_dictionary(self) -> dict:
        """
        Create a dictionary representation of this object.
        :return: a dictionary containing the components corresponding to the table this
                 object corresponds to.
        """
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'firstname': self.firstname,
            'surname': self.surname,
            'currency_id': self.currency_id,
            'has_first_sign_in': self.has_first_sign_in,
            'account_created': self.account_created,
            'last_sign_in': self.last_sign_in
        }

    def insert_to_db(self) -> None:
        """
        Insert this form of currency into the database.
        """
        query = """INSERT INTO Users(Username, Password, Firstname, Surname, Currency_id,
                                     Has_First_Sign_In, Account_Created, Last_Sign_In)
                   VALUES(?,?,?,?,?,?,?,?);"""
        self.db.commit(query, values=self.to_tuple())

    def exists_in_db(self) -> bool:
        """
        Check to see if this user exists within the db.
        :return: true if in db, false otherwise.
        """
        query = """SELECT * 
                   FROM Users 
                   WHERE Username=?;"""
        return len(self.db.fetchall(query, values=(self.username,))) > 0

    def get_type(self) -> str:
        """
        Retrieve the string representation of this objects' type.
        :return: The type associated with the object.
        """
        return Tables.USER.name

    def set_up(self) -> None:
        """
        Set up the user's firstname, lastname, currency, and change the bit to determine that the user has a first sign in.
        """
        query = """Update Users
                   SET Firstname=?, Surname=?, Currency_id=?, Has_First_Sign_In=?
                   Where id=?;"""
        self.db.commit(query,
                       values=(self.firstname, self.surname, self.currency_id, int(self.has_first_sign_in),
                               self.id))

    def create_user(self) -> None:
        """
        Create a user by inserting them into the database.
        """
        # update when the account was created
        self.account_created = datetime.now().date()
        self.insert_to_db()
        log(f"An account for User:{self.id} has been created.")

    def sign_in(self) -> None:
        """
        Sign in the user by updating the database and changing a boolean value.
        """
        self.is_signed_in = True
        self.last_sign_in = datetime.now().date()
        query = """Update Users
                   SET Last_Sign_In=? 
                   WHERE id=?;"""
        self.db.commit(query, (self.last_sign_in, self.id))
        log(f"User:{self.id} has signed in.")

    def sign_out(self) -> None:
        """
        Sign a user out of the application.
        """
        self.is_signed_in = False
        self.db.close()
        log(f"User:{self.id} has signed out.")

    def delete_user(self) -> None:
        """
        Delete all information about this user in the database.
        """
        table_dictionary = {
            'Apple': {
                'table': 'AppleReceipts',
                'user_id': 'User_id'
            },
            'ESL': {
                'table': 'ESLReceipts',
                'user_id': 'User_id'
            },
            'Transactions': {
                'table': 'Transactions',
                'user_id': 'User_id'
            },
            'Users': {
                'table': 'Users',
                'user_id': 'id'
            },
        }

        # delete the current user's information from the db.
        for key in table_dictionary:
            query = f"""
                     DELETE
                     FROM {table_dictionary[key]['table']}
                     WHERE {table_dictionary[key]['user_id']}=?;
                     """
            self.db.commit(query, values=(self.id,))

        # perform a sign out
        self.sign_out()

        log(f"User:{self.id} has deleted their account.")

    def get_earliest_transaction_date(self) -> str:
        """
        Get the earliest transaction date for this user.
        :raises NoDataFound: Exception that is raised when there is no earliest transaction data available for this user.
        :return: The date that has the first transaction made for the user.
        """
        first_transaction = """
                           SELECT MIN(Date)
                           FROM Transactions
                           WHERE User_id=?;
                           """
        transaction = self.db.fetchall(query=first_transaction, values=(self.id,))[0][0]

        if transaction is not None:
            return transaction

        raise NoDataFound

    def get_latest_transaction_date(self) -> str:
        """
        Get the latest transaction date for this user.
        :raises NoDataFound: Exception that is raised when there is no latest transaction data available for this user.
        :return: The date that has the latest transaction made for the user.
        """
        latest_transaction = """
                           SELECT MAX(Date)
                           FROM Transactions
                           WHERE User_id=?;
                           """
        transaction = self.db.fetchall(latest_transaction, values=(self.id,))[0][0]

        if transaction is not None:
            return transaction

        raise NoDataFound

    def get_total_transactions(self) -> int:
        """
        Get the total number of transactions this user has made within their accounts.
        :raises NoDataFound: Exception that is raised when there is no transaction data available for this user.
        :return: The total number of transactions this user has made.
        """
        total_transactions = """
                            SELECT COUNT(*)
                            FROM Transactions
                            WHERE User_id=?;
                            """
        total = self.db.fetchall(total_transactions, values=(self.id,))[0][0]

        if total is not None:
            return int(total)

        raise NoDataFound
