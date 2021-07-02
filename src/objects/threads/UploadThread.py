import os
import shutil
from objects.threads.Thread import Thread
from objects.user.User import User
from objects.interface.dbconn import DB
import utils.globals as _globals
from utils.print import print_message, print_error
from utils.builders.folderbuilder import get_list_of_files, insert_files


class UploadThread(Thread):
    """
    This class will be used to spawn a thread that will monitor the 'Upload' directory found within the project.
    This thread will redirect the contents from the 'Upload' folder to the user-specific subdirectory found within
    the 'Users' directory.
    """

    def __init__(self, user: User):
        """
        Initialize the Upload Thread.
        :param user: The current user.
        """
        super(UploadThread, self).__init__()
        self.user = user
        self.user_directory = f"{_globals.USERS_FOLDER}/users/{self.user.id}"

    def run(self) -> None:
        """
        Upload the files from the Upload folder to the Users folder.
        Once moved, the files are then inserted into the database.
        """
        files = get_list_of_files(_globals.UPLOAD_FOLDER, ".csv")
        files_have_been_moved = False

        # Create the User folder if it doesn't exists.
        if not os.path.isdir(_globals.USERS_FOLDER):
            os.mkdir(_globals.USERS_FOLDER)

        # Create the User specific subdirectory if it doesn't exist
        if not os.path.isdir(self.user_directory):
            os.mkdir(self.user_directory)

        # Move the files from the Upload folder to the User folder
        for file in files:
            head, file_name = os.path.split(file)
            directory = "ESL" if "ESL" in head else "Apple"
            shutil.move(file, f"{self.user_directory}/{directory}/{file_name}")
            files_have_been_moved = True

        # Delete the folders within the Upload folder to remove any subdirectories.
        # The folder thread will create them again.
        for folder in _globals.FOLDER_UPLOADS:
            shutil.rmtree(folder)

        # Get all of the files within the user's directory, and insert them into the database.
        if files_have_been_moved:
            print_message("Uploading files...")
            files = get_list_of_files(self.user_directory, ".csv")
            db = DB(_globals.DATABASE)
            upload_successful = insert_files(db, files, self.user.id)
            db.close()
            if upload_successful:
                print_message("Data has successfully been uploaded. Upload is now complete.")
            else:
                print_error("Data has already been uploaded. Please upload new data.")
        else:
            print_error("Nothing to upload. Please make sure contents are placed within the 'Upload' directory.")

        self.stop()

    def stop(self) -> None:
        """
        Tell this thread to stop executing.
        """
        super(UploadThread, self).stop()
