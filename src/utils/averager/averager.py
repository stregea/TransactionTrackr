from objects.interface.dbconn import DB
from utils import globals as _globals
from utils.exceptions import NoDataFound


def calculate_average(start_date: str, end_date: str, user_id: int, exception_type: str = "average") -> float:
    """
    Calculate the average total spent in transactions between two dates.
    :param start_date: The date to start at.
    :param end_date: The date to end at.
    :param user_id: The id of the current user.
    :param exception_type: The exception type to be sent within the NoDataFound parameters.
    :raises NoDataFound: Exception raised when there was no data to be found when calculating the average.
    :return: The average total spent in transactions between start_date and end_date.
    """
    db = DB(_globals.DATABASE)

    query = f"""
            SELECT AVG(Amount)
            FROM TRANSACTIONS
            WHERE Date BETWEEN DATE('{start_date}') AND DATE('{end_date}') AND User_id=?;
            """

    average = db.fetchall(query, values=(user_id,))[0][0]

    db.close()

    if average is not None:
        return round(float(average), 2)

    raise NoDataFound(exception_type)
