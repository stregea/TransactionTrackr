import logging
from utils.globals import LOG_FILE

logging.basicConfig(filename=LOG_FILE,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.NOTSET)


def log(message: str, level: str = "info") -> None:

    level = level.lower()
    chosen_level = logging.NOTSET

    if level == "debug":
        chosen_level = logging.DEBUG
    elif level == "info":
        chosen_level = logging.INFO
    elif level == "warning":
        chosen_level = logging.WARNING
    elif level == "error":
        chosen_level = logging.ERROR
    elif level == "critical":
        chosen_level = logging.CRITICAL
    elif level == "fatal":
        chosen_level = logging.FATAL

    logging.log(level=chosen_level, msg=message)
