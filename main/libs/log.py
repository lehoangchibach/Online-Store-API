import json
import logging
import sys

from main import config


class ServiceLogger:
    __LOGGERS: dict[str, logging.Logger] = {}

    def __init__(self, name):
        if name in self.__LOGGERS:
            self.logger = self.__LOGGERS[name]
            return

        # Create a logger for services
        logger = logging.getLogger(name)
        logger.setLevel(config.LOGGING_LEVEL)

        # Append current date time and log level to the beginning of the log message
        formatter = logging.Formatter(
            "[%(asctime)s][%(name)s][%(levelname)s] %(message)s"
        )

        handler = logging.StreamHandler(stream=sys.stdout)
        handler.setFormatter(formatter)

        if not logger.hasHandlers():
            logger.addHandler(handler)
        logger.propagate = False

        self.logger = logger
        self.__LOGGERS[name] = logger

    def info(self, **kwargs):
        return self.log(level=logging.INFO, **kwargs)

    def debug(self, **kwargs):
        return self.log(level=logging.DEBUG, **kwargs)

    def warning(self, **kwargs):
        return self.log(level=logging.WARNING, **kwargs)

    def error(self, **kwargs):
        return self.log(level=logging.ERROR, **kwargs)

    def exception(self, **kwargs):
        # Only be used when there's an exception
        return self.log(level=logging.CRITICAL, **kwargs)

    def log(self, level, message, data=None):
        if data:
            message = f"{message} | {json.dumps(data, default=str)}"

        if level == logging.CRITICAL:
            self.logger.exception(message)
        else:
            self.logger.log(level, message)
