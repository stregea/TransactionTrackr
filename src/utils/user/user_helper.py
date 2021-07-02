from objects.interface.dbconn import DB
from objects.user.User import User
from utils import globals as _globals
from utils.exceptions import UserNotFound
from utils.encryption.encrypt import match
from utils.logger.logger import log


def username_exists(username: str) -> bool:
    """
    Check to see if the specified username exists within the db.
    :param username: The username to search for.
    :return: True if in db, False otherwise.
    """
    db = DB(_globals.DATABASE)
    query = """SELECT * 
               FROM Users 
               WHERE Username=?;"""
    user_exists = len(db.fetchall(query, values=(username,))) > 0
    db.close()
    return user_exists


def password_is_valid(username: str, password_to_check: str) -> bool:
    """
    Determine if an entered password matches the one associated with a username.
    :param username: The username associated with the user.
    :param password_to_check: The password to determine if entered correctly.
    :return: True if password_to_check is the original password.
    """
    db = DB(_globals.DATABASE)
    query = """SELECT Password
               FROM Users
               WHERE Username=?;"""
    password_hash = db.fetchall(query, (username,))[0][0]
    db.close()
    return match(hashed_string=password_hash, string_to_encrypt=password_to_check)


def get_user(username: str) -> User:
    """
    Get the user information from the database.
    :param username: The username for the user.
    :raises UserNotFound: exception to be raised if the wanted user wasn't found within the database.
    :return: A user object.
    """
    db = DB(_globals.DATABASE)
    query = """SELECT id, Password, Firstname, Surname, Currency_id, Has_First_Sign_In
               FROM Users 
               WHERE Username=?;"""
    user_info = db.fetchall(query, values=(username,))

    if len(user_info) > 0:  # If the user exists
        user = User(db, username=username, password_hash=user_info[0][1])
        user.id = int(user_info[0][0])
        user.firstname = user_info[0][2]
        user.surname = user_info[0][3]
        user.currency_id = user_info[0][4]
        user.has_first_sign_in = bool(int(user_info[0][5]))
        return user

    db.close()
    raise UserNotFound(username)


def update_user(user: User) -> None:
    """
    Update a user's information within the database.
    :param user: The user to update.
    """
    db = DB(_globals.DATABASE)
    query = """UPDATE Users
               SET Username=?, Password=?, Firstname=?, Surname=?, Currency_id=? 
               WHERE id=?;"""
    db.commit(query, values=(user.username, user.password, user.firstname, user.surname, user.currency_id, user.id))
    log(f"User:{user.id} has updated their information.")
    db.close()
