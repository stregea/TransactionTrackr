import sqlite3
from sqlite3 import Error
from utils import globals
from utils.logger.logger import log


class DB:
    """
    This class will serve as the interface between client and the database.
    """

    def __init__(self, db_file) -> None:
        """
        Set up a connection to the database.
        :param db_file: The database to connect to.
        """
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_file)
        except Error as e:
            log(str(e), level="error")

    def close(self) -> None:
        """
        Close the connection to the database
        """
        self.conn.close()

    def commit(self, query: str, values: tuple = None) -> None:
        """
        Commit a query to the database.
        :param query: The  query to commit.
        :param values: The values associated with the query.
        """
        cursor = self.conn.cursor()

        if values is not None and len(values) > 0:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        cursor.close()
        # log("Query committed.", level="debug")
        self.conn.commit()

    def fetchall(self, query: str, values: tuple = None) -> list:
        """
        Perform a fetchall from a selection.
        :param query: The query to perform.
        :param values: The values associated with the query.
        :return: a list of tuples from the query.
        """
        cursor = self.conn.cursor()

        if values is not None and len(values) > 0:
            cursor.execute(query, values)
        else:
            cursor.execute(query)

        # log("Query fetched.", level="debug")
        data = cursor.fetchall()
        cursor.close()
        return data

    def setup_tables(self) -> None:
        """
        Setup the database's tables.
        """
        for table in globals.TABLES:
            self.commit(table)
            # log(f"Table created.", level="debug")

    def fetch_all_dates(self) -> list:
        """
        Return all transactions ever made.
        """
        query = """SELECT * 
                   FROM Transactions 
                   WHERE Date 
                   BETWEEN DATE('1970-01-01') AND DATE('now') Order By Date;"""
        return self.fetchall(query)

    def fetch_dates(self, date1, date2) -> list:
        query = f"""SELECT * 
                    FROM Transactions 
                    WHERE Date 
                    BETWEEN DATE('{date1}') AND DATE('{date2}');"""
        return self.fetchall(query)
