import os
from objects.threads.Thread import Thread
from utils.globals import UPLOAD_FOLDER, FOLDER_UPLOADS


class FolderThread(Thread):
    """
    This class will be used to spawn a thread that will monitor the 'Upload' folder.
    The main purpose of this thread is to make sure the 'Upload' directory will always
    be available (while the program is running), even if the user were to accidentally, or intentionally,
    delete the directory.
    """

    def __init__(self):
        """
        Initialize the Folder Thread.
        """
        super(FolderThread, self).__init__()

    def run(self) -> None:
        """
        Function to create the folders that will be used for uploading the user's data into
        the application.
        """
        while self.running:
            # Create the required upload directories
            for folder in FOLDER_UPLOADS:
                if not os.path.isdir(folder):
                    # check to see if the upload folder still exists if user were to remove it, or it doesn't exist yet.
                    if not os.path.isdir(UPLOAD_FOLDER):
                        os.mkdir(UPLOAD_FOLDER)
                    os.mkdir(folder)

    def stop(self):
        """
        Tell this thread to stop executing.
        """
        super(FolderThread, self).stop()
