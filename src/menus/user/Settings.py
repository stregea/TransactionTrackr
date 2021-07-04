import shutil
import os
from objects.user.User import User
from objects.user.Currency import get_currency, get_currency_from_input
from objects.threads.UploadThread import UploadThread
from utils.print import print_message, print_error
from utils.user.user_helper import update_user
from utils.encryption.encrypt import match, encrypt_string
from utils.globals import USERS_FOLDER
from utils.logger.logger import log
from utils.enums import SettingsSelection
from utils.generators.csv_generator import generate_transaction_files
from menus.account.CreateAccount import create_username, create_password


class Settings:
    """
    This class will be used to run the User's settings, allowing for the user to change any information they see fit.
    """

    def __init__(self, user: User):
        self.user = user
        self.user_directory = os.path.join(USERS_FOLDER, os.path.join('users', str(self.user.id)))

    def user_can_update_information(self) -> bool:
        """
        Perform a password check to determine if the user can update their information.
        :return: True if the user's input matches the password to the account. False otherwise.
        """
        password = input("Please enter your password...\n")
        return match(self.user.password, password)

    def change_username(self):
        """
        Allow a user to perform a username change.
        """
        if self.user_can_update_information():
            old_username = self.user.username
            self.user.username = create_username(update_mode=True)
            update_user(self.user)
            print_message(f"The username '{old_username}' has been updated to '{self.user.username}'")
        else:
            print_error("Password is incorrect. Cannot update username.")

    def change_password(self):
        """
        Allow a user to perform a password change.
        """
        if self.user_can_update_information():
            password = create_password(update_mode=True)
            password2 = input("Please enter your new password again.\n")
            if password == password2:
                self.user.password = encrypt_string(password)
                update_user(self.user)
                print_message("Password updated.")
            else:
                print_error("Passwords do not match. Please try again.")
        else:
            print_error("Password is incorrect. Cannot update password.")

    def change_name(self):
        """
        Allow a user to perform a name change.
        """
        if self.user_can_update_information():
            old_firstname = self.user.firstname
            old_surname = self.user.surname
            self.user.firstname = input("What is your firstname?\n")
            self.user.surname = input("What is your lastname?\n")
            update_user(self.user)
            print_message(f"The name '{old_firstname} {old_surname}' has been updated to "
                          f"'{self.user.firstname}' {self.user.surname}'")
        else:
            print_error("Password is incorrect. Cannot update name.")

    def change_currency(self):
        """
        Allow a user to perform a currency change.
        """
        if self.user_can_update_information():
            selected_currency = get_currency(acronym=get_currency_from_input())
            self.user.currency_id = selected_currency.get_id()
            print_message(f"The currency has been set to the {selected_currency.name} ({selected_currency.acronym}).")
        else:
            print_error("Password is incorrect. Cannot update currency.")

    def delete_account(self):
        """
        Allow a user to delete their account.
        """
        if self.user_can_update_information():
            self.user.delete_user()
            try:
                shutil.rmtree(self.user_directory)
            except OSError as e:
                log(f"Unable to remove the directory '{self.user_directory}'.", level='warning')

            print_message("Your account has been deleted.")
        else:
            print_error("Password is incorrect. Cannot delete the account.")

    def upload_random_data(self):
        """
        Allow a user to upload automatically generated data if they choose not to use
        real information.
        """
        if self.user_can_update_information():

            # Generate the files
            generate_transaction_files(user=self.user)

            # Upload the files
            UploadThread(self.user).run()
        else:
            print_error("Password is incorrect. Cannot generate new data.")

    def run(self) -> SettingsSelection:
        """
        Run the settings menu.
        """
        last_selection = SettingsSelection.EXIT
        running = True
        print_message("--- SETTINGS ---")

        while running:
            print_message("1.\tChange Username")
            print_message("2.\tChange Password")
            print_message("3.\tChange Name")
            print_message("4.\tChange Currency")
            print_message("5.\tUpload Random Data")
            print_message("6.\tDelete Account")
            print_message("7.\tExit")

            option = input()

            if option == "7" or option.lower() == "exit":
                last_selection = SettingsSelection.EXIT
                running = False
            elif option == "1":
                self.change_username()
                last_selection = SettingsSelection.CHANGE_USERNAME
            elif option == "2":
                self.change_password()
                last_selection = SettingsSelection.CHANGE_PASSWORD
            elif option == "3":
                self.change_name()
                last_selection = SettingsSelection.CHANGE_NAME
            elif option == "4":
                self.change_currency()
                last_selection = SettingsSelection.CHANGE_CURRENCY
            elif option == "5":
                self.upload_random_data()
                last_selection = SettingsSelection.UPLOAD_RANDOM_DATA
            elif option == "6":
                self.delete_account()
                return SettingsSelection.DELETE_ACCOUNT
            else:
                print_error("Invalid option.")

        return last_selection
