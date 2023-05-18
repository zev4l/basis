import logging

class Logger():
    """
    Simple utility class to log messages to the console.
    """
    def __init__(self, name = "ROOT", level = logging.INFO) -> None:
        formatter = logging.Formatter(fmt='[%(asctime)s][%(levelname)s]: %(message)s')
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)
    
    