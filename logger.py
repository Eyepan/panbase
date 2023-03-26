import logging
import colorlog
from config import LOG_LEVEL
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(LOG_LEVEL)

formatter = colorlog.LevelFormatter(
    fmt={
        "DEBUG": "%(log_color)sDBG:\t%(asctime)s\t%(message)s (%(module)s:%(lineno)d)",
        "INFO": "%(log_color)sINFO:\t%(asctime)s\t%(message)s",
        "WARNING": "%(log_color)sWRN:\t%(asctime)s\t%(message)s (%(module)s:%(lineno)d)",
        "ERROR": "%(log_color)sERR:\t%(asctime)s\t%(message)s (%(module)s:%(lineno)d)",
        "CRITICAL": "%(log_color)sCRT:\t%(asctime)s\t%(message)s (%(module)s:%(lineno)d)",
    },
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
)


ch.setFormatter(formatter)

logger.addHandler(ch)
