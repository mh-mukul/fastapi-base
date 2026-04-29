import os
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

LOG_TO_CONSOLE = bool(int(os.getenv("LOG_TO_CONSOLE", 1)))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_DIR = os.getenv("LOG_DIR", "./logs")
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "app.log")
LOG_BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", 7))

logger = logging.getLogger("app_logger")
logger.setLevel(LOG_LEVEL)

formatter = logging.Formatter(
    "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
)

if not logger.hasHandlers():
    if LOG_TO_CONSOLE:
        handler = logging.StreamHandler()
    else:
        os.makedirs(LOG_DIR, exist_ok=True)
        log_file = os.path.join(LOG_DIR, LOG_FILE_NAME)
        handler = TimedRotatingFileHandler(
            log_file, when="midnight", interval=1, backupCount=LOG_BACKUP_COUNT)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
