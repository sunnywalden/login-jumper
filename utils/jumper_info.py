# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

from utils.get_logger import Logger
from conf import config_template

log = Logger()
logger = log.logger_generate(__name__)


def jumper_info():
    jumper_infos = {
            "host": config_template.jumper_host,
            "port": config_template.jumper_port,
            "interval": config_template.alive_interval
        }

    return jumper_infos