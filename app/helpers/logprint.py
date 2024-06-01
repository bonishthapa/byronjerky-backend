import logging

from django.conf import settings


class LogPrint:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.debug_mode = settings.DEBUG

    def debug(self, msg, title=""):
        self.logger.debug(msg)
        if not title:
            title = "DEBUG"
        if self.debug_mode:
            print(f"######### {title} #########")
            print(msg)

    def info(self, msg, title=""):
        self.logger.info(msg)
        if not title:
            title = "INFO"
        if self.debug_mode:
            print(f"######### {title} #########")
            print(msg)

    def warning(self, msg, title=""):
        self.logger.warning(msg)
        if not title:
            title = "WARNING"
        if self.debug_mode:
            print(f"######### {title} #########")
            print(msg)

    def error(self, msg, title=""):
        self.logger.error(msg)
        if not title:
            title = "ERROR"
        if self.debug_mode:
            print(f"######### {title} #########")
            print(msg)

    def critical(self, msg, title=""):
        self.logger.critical(msg)
        if not title:
            title = "CRITICAL"
        if self.debug_mode:
            print(f"######### {title} #########")
            print(msg)

    def exception(self, msg, title=""):
        self.logger.exception(msg)
        if not title:
            title = "EXCEPTION"
        if self.debug_mode:
            print(f"######### {title} #########")
            print(msg)
