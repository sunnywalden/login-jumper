# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

from utils.get_logger import Logger
from utils import config

log = Logger()
logger = log.logger_generate(__name__)


def jumper_info():
    jumper_infos = {
            "host": config.get_config('Server', 'jumper_host'),
            "port": int(config.get_config('Server', 'jumper_port')),
            "interval": int(config.get_config('Session', 'alive_interval'))
        }

    return jumper_infos
