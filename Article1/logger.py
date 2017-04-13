import os.path

import logging
import logging.handlers

LOG_FILE_MAX_SIZE = (1024*1024) * 10

class Logger:

    def __init__(self, logFilePath):
        if not os.path.exists("log"):
            os.makedirs("log")

        # Setup rotating log files at logFilePath, each max of LOG_FILE_MAX_SIZE bytes
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(logFilePath, mode = 'w', maxBytes=LOG_FILE_MAX_SIZE, backupCount=5)
        logger.addHandler(handler)

    def debug(self, logStr):
        finalLogStr = '(SCALPTRADER_DEBUG) ' + logStr;
        logging.debug(finalLogStr)

    def warning(self, logStr):
        finalLogStr = '(SCALPTRADER_WARNING) ' + logStr;
        logging.debug(finalLogStr)

    def error(self, logStr):
        finalLogStr = '(SCALPTRADER_ERROR) ' + logStr;
        logging.debug(finalLogStr)
