from objects.BaseObject import BaseObject
from objects.interface.dbconn import DB
from objects.accounts.Transaction import Transaction
from utils.formatting.formatter import format_date
from utils.enums import Tables


class AppleReceipt(BaseObject):
    """
    This class will be used to create a Apple receipt that will be used to insert the information about this
    transaction into the database.
    """

    def __repr__(self) -> str:
        return super(AppleReceipt, self).__repr__()

    def __str__(self) -> str:
        return super(AppleReceipt, self).__str__()

    def __init__(self, db: DB, values: list, user_id: int) -> None:
        """
        Construct an Apple Receipt.
        :param db: The database connection.
        :param values: The values to assign.
        :param user_id: The id of the current user.
        """
        super(AppleReceipt, self).__init__()

        self.db = db
        self.transaction_date = format_date(values[0])
        self.clearing_date = format_date(values[1])
        self.description = values[2]
        self.merchant = values[3]
        self.category = values[4]
        self.type = values[5]
        self.amount = values[6]
        self.card_type = 'Apple'
        self.is_payment = self.category == "Payment" or self.type == "Payment"
        self.is_transaction = not self.is_payment
        self.user_id = user_id
        self.transaction = None if self.is_payment else Transaction(db, self, user_id)

    def to_list(self) -> list:
        """
        Create a list representation of this object
        :return: a list containing the components corresponding to the table this
                 object corresponds to.
        """
        return [self.transaction_date, self.clearing_date, self.description,
                self.merchant, self.category, self.type, self.amount, self.card_type,
                self.is_payment, self.is_transaction, self.user_id]

    def to_tuple(self) -> tuple:
        """
        Create a tuple representation of this object
        :return: a tuple containing the components corresponding to the table this
                 object corresponds to.
        """
        return (self.transaction_date, self.clearing_date, self.description,
                self.merchant, self.category, self.type, self.amount, self.card_type,
                self.is_payment, self.is_transaction, self.user_id)

    def to_dictionary(self) -> dict:
        """
        Create a dictionary representation of this object
        :return: a dictionary containing the components corresponding to the table this
                 object corresponds to.
        """
        return {
            'transaction_date': self.transaction_date,
            'clearing_date': self.clearing_date,
            'description': self.description,
            'merchant': self.merchant,
            'category': self.category,
            'type': self.type,
            'amount': self.amount,
            'card_type': self.card_type,
            'is_payment': self.is_payment,
            'is_transaction': self.is_transaction,
            'user_id': self.user_id
        }

    def format_amount(self) -> str:
        """
        Remove a negative sign from the string.
        :return: a positive signed number in string format.
        """
        return self.amount.replace('-', '')

    def insert_to_db(self) -> None:
        """
        Insert this receipt into the database as well as inserting it into the transactions table, if a transaction.
        """
        query = '''INSERT INTO AppleReceipts(Transaction_Date, Clearing_Date, Description, Merchant,
                                             Category, Type, Amount, Card_Type, Is_Payment, Is_Transaction, User_id)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?);'''
        self.db.commit(query, values=self.to_tuple())

        if self.is_transaction \
                and self.transaction is not None \
                and not self.transaction.exists_in_db():
            self.transaction.insert_to_db()

    def exists_in_db(self) -> bool:
        """
        May not work with duplicate transactions on same dates, may want to figure out better query.
        Check to see if this object exists within the db.
        :return: true if in db, false otherwise.
        """
        query = '''SELECT * 
                   FROM AppleReceipts 
                   WHERE Transaction_Date=? AND Clearing_Date=? AND Description=? 
                                            AND Merchant=? AND Category=? 
                                            AND Type=? AND Amount=? 
                                            AND Card_Type=? AND Is_Payment=?
                                            AND Is_Transaction=? AND User_id=?;'''
        return len(self.db.fetchall(query, values=self.to_tuple())) > 0

    def get_id(self) -> int:
        """
        Retrieve the id of this object from the database.
        :return: The id associated with an Apple object.
        """
        query = '''SELECT id 
                   FROM AppleReceipts 
                   WHERE Transaction_Date=? AND Clearing_Date=? AND Description=? 
                                            AND Merchant=? AND Category=? 
                                            AND Type=? AND Amount=? 
                                            AND Card_Type=? AND Is_Payment=?
                                            AND Is_Transaction=? AND User_id=?;'''
        return int(self.db.fetchall(query, values=self.to_tuple())[0][0])

    def get_type(self) -> str:
        """
        Retrieve the string representation of this objects' type.
        :return: The type associated with the object.
        """
        return Tables.APPLE.name
