from sys import stderr
from objects.user.Currency import get_currency, get_currency_from_input
from objects.user.User import User
from utils.print import print_message, print_error
from utils.exceptions import UserNotFound, BadSignIn
from utils.user.user_helper import get_user, username_exists, password_is_valid
from utils.logger.logger import log
from menus.account.CreateAccount import create_account


def set_up(user: User):
    """
    Set up the user's account upon their initial sign-in.
    :param user: The user to set up their account information.
    TODO: Have user upload csv files. Create script to generate random financial data.
    """
    print_message("Welcome to your new account! It's time to now set it up.")

    firstname = input("What is your first name?\n")
    surname = input("What is your last name?\n")
    currency_acronym = get_currency_from_input()

    user.firstname = firstname
    user.surname = surname
    user.currency_id = get_currency(currency_acronym).get_id()
    user.has_first_sign_in = True
    user.set_up()


def sign_in(username: str, password: str) -> User:
    """
    Perform a user sign in.
    :param username: The username of the user.
    :param password: The password of the user.
    :raises BadSignIn: exception to be raised when the sign in is unsuccessful.
    :return: The user upon a successful sign in.
    """
    if username_exists(username) and password_is_valid(username, password):
        try:
            user = get_user(username=username)

            if isinstance(user, User) and not user.has_first_sign_in:
                set_up(user)

            user.sign_in()

            return user
        except UserNotFound as unf:
            log(unf.message, level="warning")

    raise BadSignIn(username)


class SignIn:
    """
    This class will be used create a menu to sign in a user.
    """

    def __init__(self):
        self.user = None

    def sign_in(self) -> User:
        """
        Perform a user sign in.
        :raises BadSignIn: exception to be raised when the sign in is unsuccessful.
        :return: The user upon a successful sign in.
        """

        print_message("--- SIGN IN ---")
        username = input("What is your username?\n")
        password = input("What is your password?\n")

        return sign_in(username, password)

    def run(self) -> (User, bool):
        """
        Run the menu to prompt the user to sign in or create an account.
        :return: The user upon a successful log in as well as a boolean to determine to keep the program running or not.
        """
        signed_in = False
        program_running = True
        print_message("--- Welcome! Please select an option. ---")
        while not signed_in:
            print_message("1.\tSign in")
            print_message("2.\tCreate Account")
            print_message("3.\tQuit")

            option = input()

            if option == "3" or option.lower() == "quit":
                program_running = False
                break
            elif option == "1":
                try:
                    self.user = self.sign_in()
                    signed_in = True
                except BadSignIn as bsi:
                    log(bsi.message, level="warning")
                    print_error(bsi.message)
            elif option == "2":
                create_account()
            else:
                print_error("Invalid option")

        return self.user, program_running
