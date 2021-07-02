from objects.interface.dbconn import DB
from objects.BaseObject import BaseObject
from objects.accounts import Apple, ESL
from utils.enums import Tables


class Transaction(BaseObject):
    """
    Class that will be used to construct a Transaction object.
    """

    def __init__(self, db: DB, receipt: BaseObject, user_id: int) -> None:
        """
        Construct a Transaction.
        :param db: The database connection.
        :param receipt: The object creating this Transaction.
        :param user_id: The id of the current user.
        """
        super(Transaction, self).__init__()

        self.db = db
        self.date = None
        self.amount = None
        self.card_type = None
        self.merchant = None
        self.description = None
        self.user_id = user_id
        values = receipt.to_dictionary()

        if isinstance(receipt, Apple.AppleReceipt):
            self.date = values['transaction_date']
            self.amount = values['amount']
            self.card_type = values['card_type']
            self.merchant = values['merchant']
            self.description = values['description']

        elif isinstance(receipt, ESL.ESLReceipt):
            self.date = values['date']
            self.amount = receipt.format_amount()
            self.card_type = values['card_type']
            self.merchant = values['memo']
            self.description = values['description']

    def __repr__(self) -> repr:
        """
        Inherit the parent object's __str__.
        :return: the __repr__ of this object.
        """
        return super(Transaction, self).__repr__()

    def __str__(self) -> str:
        """
        Inherit the parent object's __repr__.
        :return: the __repr__ of this object.
        """
        return super(Transaction, self).__str__()

    def to_list(self) -> list:
        """
        Create a list representation of this object.
        :return: a list containing the components corresponding to the table this
                 object corresponds to.
        """
        return [self.date, self.amount, self.card_type,
                self.merchant, self.description, self.user_id]

    def to_tuple(self) -> tuple:
        """
        Create a tuple representation of this object.
        :return: a tuple containing the components corresponding to the table this
                 object corresponds to.
        """
        return (self.date, self.amount, self.card_type,
                self.merchant, self.description, self.user_id)

    def to_dictionary(self) -> dict:
        """
        Create a dictionary representation of this object.
        :return: a dictionary containing the components corresponding to the table this
                 object corresponds to.
        """
        return {
            'date': self.date,
            'amount': self.amount,
            'card_type': self.card_type,
            'merchant': self.merchant,
            'description': self.description,
            'user_id': self.description
        }

    def insert_to_db(self) -> None:
        """
        Insert this transaction into the database.
        TODO: Add ESL / Apple ID
        """
        query = '''INSERT INTO Transactions(Date, Amount, Card_Type, Merchant, Description, User_id)
                   VALUES(?,?,?,?,?,?);'''
        self.db.commit(query, values=self.to_tuple())

    def exists_in_db(self) -> bool:
        """
        May not work with duplicate transactions on same dates, may want to figure out better query.
        Check to see if this object exists within the db.
        :return: true if in db, false otherwise.
        """
        query = '''SELECT * 
                   FROM Transactions 
                   WHERE Date=? AND Amount=? AND Card_Type=? AND Merchant=? AND Description=? AND User_id=?;'''
        return len(self.db.fetchall(query, values=self.to_tuple())) > 0

    def get_id(self) -> int:
        """
        Retrieve the id of this object from the database.
        :return: The id associated with a Transaction object.
        """
        query = '''SELECT id 
                   FROM Transactions 
                   WHERE Date=? AND Amount=? AND Card_Type=? AND Merchant=? AND Description=? AND User_id=?;'''
        return int(self.db.fetchall(query, values=self.to_tuple())[0][0])

    def get_type(self) -> str:
        """
        Retrieve the string representation of this objects' type.
        :return: The type associated with the object.
        """
        return Tables.TRANSACTION.name
