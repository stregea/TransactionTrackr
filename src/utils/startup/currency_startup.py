import csv
import utils.globals as _globals
from objects.interface.dbconn import DB
from objects.user.Currency import Currency
from utils.logger.logger import log


def startup() -> None:
    """
    Insert all of the available currencies into the database.
    """
    db = DB(_globals.DATABASE)
    db_updated = False
    file = _globals.CURRENCIES

    with open(file, newline='') as csvf:
        rows = list(csv.reader(csvf))
        for i in range(1, len(rows)):
            currency = Currency(db, rows[i])

            if not currency.exists_in_db():
                currency.insert_to_db()
                db_updated = True

    if db_updated:
        log("New currencies have been added to the database.", level="debug")
    else:
        log("No new currencies added to the database.", level="debug")

    db.close()
