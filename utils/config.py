#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 配置管理

import os
import sys

version = sys.version_info
v_info = str(version.major) + '.' + str(version.minor) + '.' + str(version.micro)

# 判断Python版本号
if version < (3, 0):
    import ConfigParser as config_parser
else:
    import configparser as config_parser


def get_config(section, option):
    if os.getenv(option, None):
        if os.getenv(option):
            return os.getenv(option)

    file_path = '../conf/config.ini'

    if version < (3, 0):
        conf = config_parser.ConfigParser(allow_no_value=True)
        conf.read(file_path)
    else:
        conf = config_parser.RawConfigParser()
        conf.read_file(open(file_path))
    if conf.has_section(section):
        if conf.has_option(section, option):
            jumper_host = conf.get(section, option)
            return jumper_host
        else:
            return None
    else:
        return None
