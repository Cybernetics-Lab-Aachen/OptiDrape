import logging
import coloredlogs


def get_logger():
    logger = logging.getLogger(__name__)
    coloredlogs.install(level='DEBUG', logger=logger)
    return logger
