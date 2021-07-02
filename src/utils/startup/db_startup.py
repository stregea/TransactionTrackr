from objects.interface.dbconn import DB
import utils.globals as _globals
from utils.logger.logger import log


def startup() -> None:
    """
    Start up the database then translate the input files and insert them into the database.
    """
    log("Initializing the database...", level="debug")
    db = DB(_globals.DATABASE)
    db.setup_tables()
    db.close()
