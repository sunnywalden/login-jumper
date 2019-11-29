#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 配置管理

import configparser as config_parser


def get_config(section, option):
    conf = config_parser.RawConfigParser()
    file_path = 'conf/config.ini'

    conf.read_file(open(file_path))
    if conf.has_section(section):
        if conf.has_option(section, option):
            jumper_host = conf.get(section, option)
            return jumper_host
        else:
            return None
    else:
        return None
