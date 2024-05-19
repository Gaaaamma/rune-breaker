"""Logger"""

import sys

from logging import getLogger, Logger, Formatter, StreamHandler

from setting import SETTINGS

def get_logger(level: int) -> Logger:
    """Get logger with formatter"""

    logger: Logger = getLogger(__name__)
    logger.setLevel(level)

    stream_handler: StreamHandler = StreamHandler(sys.stdout)
    stream_handler.setFormatter(Formatter(SETTINGS.formatter))
    
    logger.addHandler(stream_handler)
    return logger


logger: Logger = get_logger(SETTINGS.log_level)