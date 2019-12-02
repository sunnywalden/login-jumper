#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: sunnywalden@gmail.com

import logging
import os
import socket
import sys
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "."))


def logger_generate(name='logs/jumper_server.log'):
    logger = logging.getLogger('logger')

    # logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.ERROR)

    log_file = os.path.join(BASE_DIR, name)

    handler = RotatingFileHandler(filename=log_file, mode='a', encoding='utf-8', maxBytes=1024 * 4096,
                                  backupCount=3)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(process)d %(levelname)s %(thread)d - %(funcName)s %(filename)s:%(lineno)d %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    socket.setdefaulttimeout(10)

    return logger
