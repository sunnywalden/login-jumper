# !/usr/bin/env python
# -*- coding: utf-8 -*-

import redis

from utils import config
from utils.get_logger import logger_generate

logger = logger_generate(__name__)


def redis_handler(mode='single'):
    file_path = "../conf/redis.ini"
    section = mode
    ip = config.get_config(section, "host", file_path=file_path)
    port = config.get_config(section, "port", file_path=file_path)
    db = config.get_config(section, "database", file_path=file_path)
    password = config.get_config(section, "password", file_path=file_path)

    r = redis.Redis(host=ip, port=port, db=db, password=password)

    return r

