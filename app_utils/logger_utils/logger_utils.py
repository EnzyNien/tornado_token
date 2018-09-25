# -*- encoding: utf-8 -*-
from __future__ import print_function

import datetime
import logging
import os

try:
    import settings
    (settings.DEBUG, settings.CURRENT_PATH)
except:
    print('''add settings.py with:

DEBUG = True / False
CURRENT_PATH = os.getcwd()
''')
    import sys
    sys.exit()

__all__ = ('get_logger', )


def get_logger(name, level=logging.ERROR):
    utc_now = datetime.datetime.utcnow()
    path = os.path.join(
        settings.CURRENT_PATH,
        utc_now.strftime('log/%Y/%m/%d/'),
    )
    os.path.exists(path) or os.makedirs(path)
    level = logging.DEBUG if settings.DEBUG else level
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logger = logging.getLogger('{}-logger'.format(name))
    logger.setLevel(level)

    file_handler = logging.FileHandler(
        os.path.join(path, '{}.log'.format(name)),
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if settings.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
