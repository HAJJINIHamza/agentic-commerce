import logging 
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from datetime import datetime 

logging_path = Path("logs/")

def get_logger(
    name: str = __name__, 
    level: int = logging.INFO
    ) -> logging.Logger:

    """
    Handles project loggings

    It creates loggings on the console as well as in a file stored in "logs/" dire.
    It creates a log file every day.

    args:
        name : str : defaults to __name__
        level : log level to capture

    returns:
        logging object
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    counsel_handler = logging.StreamHandler(sys.stdout)
    counsel_handler.setLevel(level)

    formatter = logging.Formatter(
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S"
    )

    counsel_handler.setFormatter(formatter)
    logger.addHandler(counsel_handler)

    logging_path.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")

    file_handler = TimedRotatingFileHandler(
        filename = logging_path / f"{today}.log",
        when = "midnight",
        backupCount = 30,
        encoding = "utf-8"
    )

    file_handler.suffix = "%Y-%m-%d.log"
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger