from objects.accounts import Transaction
from objects.BaseObject import BaseObject
from objects.interface.dbconn import DB
from utils.formatting.formatter import format_date
from utils.enums import Tables


class ESLReceipt(BaseObject):
    """
    This class will be used to create a Apple receipt that will be used to insert the information about this
    transaction into the database.
    """

    def __repr__(self) -> str:
        return super(ESLReceipt, self).__repr__()

    def __str__(self) -> str:
        return super(ESLReceipt, self).__str__()

    def __init__(self, db: DB, values: list, user_id: int) -> None:
        """
        Construct an ESL Receipt.
        :param db: The database connection.
        :param values: The values to assign.
        :param user_id: The id of the current user.
        """
        super(ESLReceipt, self).__init__()

        self.db = db
        self.transaction_number = values[0]
        self.date = format_date(values[1])
        self.description = values[2]
        self.memo = values[3]
        self.amount_debit = values[4]
        self.amount_credit = values[5]
        self.balance = values[6]
        self.check_number = values[7]
        self.fees = values[8]
        self.card_type = 'ESL'
        self.is_payment = self.memo == "- PAYMENT" \
                          or self.description == "Withdrawal Internet Transfer to" \
                          or "ACH Deposit" in self.description \
                          or self.description == "Overdraft Deposit" \
                          or self.description == "Descriptive Deposit Mobile /" \
                          or self.description == "Deposit Internet Transfer from"
        self.is_transaction = not self.is_payment
        self.user_id = user_id
        self.transaction = None if self.is_payment else Transaction.Transaction(db, self, user_id)

    def to_list(self) -> list:
        """
        Create a list representation of this object.
        :return: a list containing the components corresponding to the table this
                 object corresponds to.
        """
        return [self.transaction_number, self.date, self.description, self.memo, self.amount_debit,
                self.amount_credit, self.balance, self.check_number, self.fees, self.card_type,
                self.is_payment, self.is_transaction, self.user_id]

    def to_tuple(self) -> tuple:
        """
        Create a tuple representation of this object.
        :return: a tuple containing the components corresponding to the table this
                 object corresponds to.
        """
        return (self.transaction_number, self.date, self.description, self.memo, self.amount_debit,
                self.amount_credit, self.balance, self.check_number, self.fees, self.card_type,
                self.is_payment, self.is_transaction, self.user_id)

    def to_dictionary(self) -> dict:
        """
        Create a dictionary representation of this object.
        :return: a dictionary containing the components corresponding to the table this
                 object corresponds to.
        """
        return {
            'transaction_number': self.transaction_number,
            'date': self.date,
            'description': self.description,
            'memo': self.memo,
            'amount_debit': self.amount_debit,
            'amount_credit': self.amount_credit,
            'balance': self.balance,
            'check_number': self.check_number,
            'fees': self.fees,
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
        if self.amount_debit != '':
            return self.amount_debit.replace('-', '')
        return self.amount_credit.replace('-', '')

    def insert_to_db(self) -> None:
        """
        Insert this receipt into the database as well as inserting it into the transactions table, if a transaction.
        """
        query = '''INSERT INTO ESLReceipts(Transaction_Number, Date, Description, Memo,
                                           Amount_Debit, Amount_Credit, Balance, Check_Number, 
                                           Fees, Card_Type, Is_Payment, Is_Transaction, User_id)
                   VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?);'''
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
                   FROM ESLReceipts 
                   WHERE Transaction_Number=? AND Date=? AND Description=? 
                                              AND Memo=? AND Amount_Debit=? 
                                              AND Amount_Credit=? AND Balance=? 
                                              AND Check_Number=? AND Fees=? 
                                              AND Card_Type=? AND Is_Payment=? 
                                              AND Is_Transaction=? AND User_id=?;'''
        return len(self.db.fetchall(query, values=self.to_tuple())) > 0

    def get_id(self) -> int:
        """
        Retrieve the id of this object from the database.
        :return: The id associated with an ESL object.
        """
        query = '''SELECT id 
                   FROM ESLReceipts 
                   WHERE Transaction_Number=? AND Date=? AND Description=? 
                                              AND Memo=? AND Amount_Debit=? 
                                              AND Amount_Credit=? AND Balance=? 
                                              AND Check_Number=? AND Fees=? 
                                              AND Card_Type=? AND Is_Payment=? 
                                              AND Is_Transaction=? AND User_id=?;'''
        return int(self.db.fetchall(query, values=self.to_tuple())[0][0])

    def get_type(self) -> str:
        """
        Retrieve the string representation of this objects' type.
        :return: The type associated with the object.
        """
        return Tables.ESL.name
