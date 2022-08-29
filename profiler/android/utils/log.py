
import sys
import logging
import logging.handlers

logger = logging.getLogger("Profiler")
logger.setLevel(logging.DEBUG)


def config_logger():
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)


config_logger()