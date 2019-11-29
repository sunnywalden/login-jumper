#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: sunnywalden@gmail.com

import logging
import socket
from logging.handlers import RotatingFileHandler
import os
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)


class Logger(object):
    def logger_generate(self, name):
        logger = logging.getLogger('logger')

        logger.setLevel(logging.INFO)

        log_file = os.path.join('../logs', name + '.log')

        handler = RotatingFileHandler(filename=log_file, mode='a', encoding='utf-8', maxBytes=1024 * 4096,
                                      backupCount=3)

        formatter = logging.Formatter(
            fmt='%(asctime)s %(process)d %(levelname)s %(thread)d - %(funcName)s %(filename)s:%(lineno)d %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        socket.setdefaulttimeout(10)

        return logger
