#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: sunnywalden@gmail.com

import logging
import os
import socket
import sys
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)


def logger_generate(name):
    logger = logging.getLogger('logger')

    # logger.setLevel(logging.INFO)
    logger.setLevel(logging.ERROR)

    log_file = os.path.join('../logs', name + '.log')

    handler = RotatingFileHandler(filename=log_file, mode='a', encoding='utf-8', maxBytes=1024 * 4096,
                                  backupCount=3)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(process)d %(levelname)s %(thread)d - %(funcName)s %(filename)s:%(lineno)d %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    socket.setdefaulttimeout(10)

    return logger
