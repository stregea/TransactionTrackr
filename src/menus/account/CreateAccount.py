import re
from objects.user.User import User
from objects.interface.dbconn import DB
import utils.globals as _globals
from utils.print import print_message, print_error
from utils.encryption.encrypt import encrypt_string
from utils.user.user_helper import username_exists


def valid_username(username: str) -> bool:
    """
    Usernames can be any size greater than or equal to 3, Usernames also cannot contain
    any spaces.
    :param username: The name to validate.
    :return: True if valid, false otherwise.
    """
    if " " in username:
        print_error("Cannot have spaces in username.")
        return False
    elif len(username) < 3:
        print_error("Invalid size for username. Username must have at least 3 characters.")
        return False

    return True


def username_check(username: str) -> str:
    """
    Run a loop to check and determine if a username is valid.
    :param username: The username to check.
    """
    running = True

    while running:
        flag1 = True
        flag2 = True

        if username_exists(username):
            print_error(f"'{username}' already exists.")
            flag1 = False
        if not valid_username(username):
            flag2 = False

        running = not (flag1 and flag2)

        if running:
            username = input("Enter a new username:\n")

    return username


def create_username(update_mode: bool = False) -> str:
    """
    Function that is used to prompt a user to input a valid username.
    :param update_mode: The mode to determine if the user is creating or updating a username.
    :return: The username for the user.
    """
    mode_string = "Update your username:" if update_mode else "Create a username:"
    return username_check(username=input(f"{mode_string}\n"))


def create_password(update_mode: bool = False) -> str:
    """
    Function that is used to prompt a user to input a safe and acceptable password.
    :param update_mode: The mode to determine if the user is creating or updating a password.
    :return: The password for the user.
    """
    while True:
        mode_string = "Update your password:" if update_mode else "Create a password:"
        password = input(f"{mode_string}\n")
        if len(password) < 8:
            print_error("Make sure your password has at least 8 letters.")
        elif re.search('[0-9]', password) is None:
            print_error("Make sure your password has at least one number.")
        elif re.search('[A-Z]', password) is None:
            print_error("Make sure your password has at least one capital letter.")
        else:
            break
    return password


def create_account() -> None:
    """
    Prompt a user to create a new account.
    """
    print_message("--- CREATE ACCOUNT ---")
    username = create_username()
    password = create_password()

    encrypted_password = encrypt_string(password)

    db = DB(_globals.DATABASE)
    user = User(db, username=username, password_hash=encrypted_password)
    user.create_user()
    db.close()
    print_message(f"Account for '{username}' has been created.")
