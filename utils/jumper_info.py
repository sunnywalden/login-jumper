# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

from utils.get_logger import Logger
from conf import config

log = Logger()
logger = log.logger_generate(__name__)


def jumper_info():
    jumper_infos = {
            "host": config.jumper_host,
            "port": config.jumper_port,
            "interval": config.alive_interval
        }

    return jumper_infos