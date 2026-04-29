import os
import logging
from logging.handlers import TimedRotatingFileHandler


if not os.path.exists("./logs"):
    os.mkdir("./logs")

log_file = f"./logs/app.log"

# Create a single logger instance
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    handler = TimedRotatingFileHandler(
        log_file, when="midnight", interval=1, backupCount=7)

    formatter = logging.Formatter(
        "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
