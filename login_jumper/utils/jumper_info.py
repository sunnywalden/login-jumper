# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

from login_jumper.utils.get_logger import logger_generate
from login_jumper.utils import config

logger = logger_generate()


def jumper_info():
    jumper_infos = {
            "host": config.get_config('Server', 'jumper_host'),
            "port": config.get_config('Server', 'jumper_port'),
            "interval": config.get_config('Session', 'alive_interval')
        }

    return jumper_infos
