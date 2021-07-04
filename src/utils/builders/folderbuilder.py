import os
import csv
from objects.accounts.Apple import AppleReceipt
from objects.accounts.ESL import ESLReceipt
from objects.interface.dbconn import DB
from objects.user.User import User
import utils.globals as _globals
from utils.exceptions import UserNotFound
from utils.logger.logger import log


def insert_files(db: DB, files: list, user_id: int,) -> bool:
    """
    Insert files into the database.
    :param db: The connection to the database.
    :param files: The list of files to insert.
    :param user_id: The id of the current user.
    :return: True if file insertion was successful. False otherwise.
    """
    db_updated = False
    for file in files:

        with open(file, newline='') as csv_file:
            rows = list(csv.reader(csv_file))

            row = 1 if "Apple" in file else 4

            for i in range(row, len(rows)):
                receipt = None

                if "Apple" in file:
                    receipt = AppleReceipt(db, rows[i], user_id)
                elif "ESL" in file:
                    receipt = ESLReceipt(db, rows[i], user_id)

                if receipt is not None and not receipt.exists_in_db():
                    receipt.insert_to_db()
                    db_updated = True

    if db_updated:
        log("The database has been updated.", level="debug")
    else:
        log("No updates made to the database.", level="debug")

    return db_updated


def get_list_of_files(directory: str, file_type: str) -> list:
    """
    Search a specified directory and add csv file to a list.
    :param directory: The directory to search.
    :param file_type: The type of file to add to the list.
    :return: A list of files within the specified directory.
    """
    ret = []
    for (root, subdirectories, files) in os.walk(directory):
        for file in files:
            if file.endswith(file_type):
                ret.append(os.path.abspath(os.path.join(root, file)))
    return ret


def create_user_folder(user: User) -> None:
    """
    Create a folder to contain the .csv files that hold all of the
    transaction information for a user.
    :param user: The user to create information for.
    :raises UserNotFound: Exception to be raised when a user does not currently exist within the database.
    """

    if not user.exists_in_db():
        raise UserNotFound

    users_directory = os.path.join(_globals.USERS_FOLDER, 'users')
    current_user_directory = os.path.join(users_directory, str(user.id))

    # create parent directory if it doesn't exist
    if not os.path.isdir(_globals.USERS_FOLDER):
        os.mkdir(_globals.USERS_FOLDER)
        log(f"Directory '{_globals.USERS_FOLDER}' has been created.", level="info")

    # create user directory if it doesn't exist.
    if not os.path.isdir(users_directory):
        os.mkdir(users_directory)
        log(f"Directory '{users_directory}' has been created.", level="info")

    # create the user folder
    if not os.path.isdir(current_user_directory):
        os.mkdir(current_user_directory)
        log(f"Directory '{current_user_directory}' has been created.", level="info")

    # Create the accepted accounts directories (Apple, ESL, etc.)
    for account in _globals.ACCOUNTS:
        path = os.path.join(current_user_directory, account)
        if not os.path.isdir(path):
            os.mkdir(path)
            log(f"Directory '{path}' has been created.", level="info")
