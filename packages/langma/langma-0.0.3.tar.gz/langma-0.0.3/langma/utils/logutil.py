# -*- coding: utf-8 -*-
import logging.handlers
import os
import logging
from datetime import datetime


class ColorFormatter(logging.Formatter):
    """Colorizes log output."""

    LEVEL_COLORS = {
        logging.DEBUG: "\033[00;32m",  # GREEN
        logging.INFO: "\033[00;34m",  # BLUE
        logging.WARN: "\033[00;35m",  # MAGENTA
        logging.WARNING: "\033[00;35m",  # MAGENTA
        logging.ERROR: "\033[00;31m",  # RED
        logging.CRITICAL: "\033[01;31m",  # BOLD RED
    }

    COLOR_STOP = "\033[0m"

    def add_color(self, record):
        """Add color to a record."""
        if getattr(record, "_stream_is_a_tty", False):
            record.color = self.LEVEL_COLORS[record.levelno]
            record.color_stop = self.COLOR_STOP
        else:
            record.color = self.LEVEL_COLORS[record.levelno]
            record.color_stop = self.COLOR_STOP

    def remove_color(self, record):
        """Remove color from a record."""
        del record.color
        del record.color_stop

    def format(self, record):
        """Format a record."""
        self.add_color(record)
        s = super(ColorFormatter, self).format(record)
        self.remove_color(record)
        return s


def get_logger(log_path='logs', log_level='INFO', name=None):

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    _file_format = '%(color)s%(asctime)s|%(levelname)s|%(filename)s[:%(' \
               'lineno)d] %(message)s %(color_stop)s'
    _console_format = '%(color)s[%(asctime)s|%(levelname)s] %(message)s %(' \
                      'color_stop)s'

    file_formatter = ColorFormatter(fmt=_file_format,
                                    datefmt="%Y-%m-%d "
                                    "%H:%M:%S")
    console_formatter = ColorFormatter(fmt=_console_format,
                                       datefmt="%Y-%m-%d "
                                       "%H:%M:%S")

    file_handler = logging.handlers.WatchedFileHandler(
        f"{log_path}"
        f"/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S.log')}")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    efile_handler = logging.handlers.WatchedFileHandler(
        f'{log_path}/error.log')
    efile_handler.setLevel(logging.ERROR)
    efile_handler.setFormatter(file_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(efile_handler)

    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(console_formatter)
    logger.addHandler(console)

    return logger


logger = get_logger(log_path='logs', log_level='INFO')
