from objects.BaseObject import BaseObject
from utils.logger.logger import log


class File(BaseObject):
    """
    Class that will be used to construct a File object.

    Note: This class was initially created to store the file name into the database upon upload/insertion of files,
    but that functionality is no longer used. The use of this class will be paused until (if ever) needed.
    """

    def __init__(self, db, name) -> None:
        """
        Construct a File.
        :param db: The database connection.
        :param name: The name of the file.
        """
        super(File, self).__init__()
        self.db = db
        self.name = name

    def __repr__(self) -> repr:
        """
        Inherit the parent object's __repr__.
        :return: the __repr__ of this object.
        """
        return super(File, self).__repr__()

    def __str__(self) -> str:
        """
        Inherit the parent object's __str__.
        :return: the __str__ of this object.
        """
        return super(File, self).__str__()

    def to_list(self) -> list:
        """
        Create a list representation of this object.
        :return: a list containing the components corresponding to the table this
                 object corresponds to.
        """
        return [self.name]

    def to_tuple(self) -> tuple:
        """
        Create a tuple representation of this object.
        :return: a tuple containing the components corresponding to the table this
                 object corresponds to.
        """
        return tuple((self.name,))

    def to_dictionary(self) -> dict:
        """
        Create a dictionary representation of this object.
        :return: a dictionary containing the components corresponding to the table this
                 object corresponds to.
        """
        return {'name': self.name}

    def insert_to_db(self):
        """
        Insert this file into the database.
        """
        query = """INSERT INTO CSVFiles(Name)
                   VALUES(?);"""
        self.db.commit(query, values=self.to_tuple())
        log(f"{self.name} has been uploaded to the database.", level="info")

    def exists_in_db(self):
        """
        Check to see if this object exists within the db.
        :return: true if in db, false otherwise.
        """
        query = """SELECT * 
                   FROM CSVFiles 
                   WHERE name=?;"""
        return len(self.db.fetchall(query, values=self.to_tuple())) > 0

    def get_id(self) -> int:
        """
        Retrieve the id of this object from the database.
        :return: The id associated with a File (CSV) object.
        """
        query = """SELECT id 
                   FROM CSVFiles
                   WHERE name=?;"""
        return int(self.db.fetchall(query, values=self.to_tuple())[0][0])
