from argparse import ArgumentParser, Namespace
import traceback
from sys import stderr
from objects.threads.FolderThread import FolderThread
from utils.logger.logger import log
from utils.startup import currency_startup, db_startup
from utils.exceptions import BadSignIn
from utils.builders.folderbuilder import create_user_folder
from menus.user.Menu import Menu
from menus.account.SignIn import SignIn, sign_in


def setup_args() -> Namespace:
    """
    Setup the commandline arguments.
    :return: The argument parser object containing the parameters.
    """
    parser = ArgumentParser()
    parser.add_argument('-c', '--show_console', help='display information on to the console.', action='store_true')
    parser.add_argument('-v', '--show_visual', help='display information from a visualization perspective.',
                        action='store_true')
    parser.add_argument('-u', '--username', help='username')
    parser.add_argument('-p', '--password', help='password')
    return parser.parse_args()


def user_excluded_sign_in_params(args: Namespace) -> bool:
    """
    Determine if the user excluded either both the user name and password, or excluded either parameter.
    :param args: The command line arguments.
    :return: True if the user excluded the arguments, False otherwise.
    """
    return (not args.username and not args.password) or (args.username and not args.password) or (
                not args.username and args.password)


def main() -> None:
    """
    Run the application.
    """
    args = setup_args()
    user = None
    show_console_information = False
    show_visual_information = False
    bad_parameter_sign_in = False

    # Initialize the database, create the tables if they don't exist.
    db_startup.startup()

    # Populate all of the available currencies into the database.
    currency_startup.startup()

    # Perform an initial sign in if a username and password were detected.
    try:
        if args.username and args.password:
            user = sign_in(args.username, args.password)
    except BadSignIn as bsi:
        stderr.write(f"{bsi.message}\n")
        log(traceback.format_exc(), level="warning")
        log(bsi.message, level="warning")
        bad_parameter_sign_in = True  # update the boolean to have the user perform a 'regular' sign on.

    # Determine which information should be displayed.
    if args.show_console:
        show_console_information = True
    if args.show_visual:
        show_visual_information = True

    try:
        # Initialize the (daemon) folder thread, which will monitor the 'Upload' directory.
        folder_thread = FolderThread()
        folder_thread.start()

        program_running = True
        user_has_signed_out = False

        while program_running:

            # Get the user from sign-in prompt if username and password weren't included in command line parameters.
            if user_has_signed_out or user_excluded_sign_in_params(args) or bad_parameter_sign_in:
                user, program_running = SignIn().run()

            if program_running:
                # Create the current user's directory (if it doesn't already exist) within the 'Users' directory.
                create_user_folder(user=user)

                # Run the application.
                user_has_signed_out = Menu(user=user, show_console=show_console_information, show_visual=show_visual_information).run()

    except Exception as e:
        print(e)
        log(str(e), level="critical")
        log(traceback.format_exc(), level="critical")
        exit(-1)


if __name__ == '__main__':
    main()
