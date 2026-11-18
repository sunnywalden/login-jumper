#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 配置管理
# 读取顺序：LOGIN_JUMPER_<SECTION>_<OPTION>，其次与选项同名的环境变量，
# 其次同目录 *.local.ini（不提交），最后才是传入的示例 ini。

import os
import sys

version = sys.version_info
v_info = str(version.major) + '.' + str(version.minor) + '.' + str(version.micro)

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), "."))

# 判断Python版本号
if version < (3, 0):
    import ConfigParser as config_parser
else:
    import configparser as config_parser


def _env_override(section, option):
    names = []
    if section and option:
        names.append(
            "LOGIN_JUMPER_%s_%s" % (str(section).upper(), str(option).upper())
        )
    if option:
        names.append(option)
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return None


def _local_override_path(file_path):
    if not file_path:
        return None
    directory, filename = os.path.split(file_path)
    base, ext = os.path.splitext(filename)
    if ext.lower() != ".ini" or base.endswith(".local"):
        return None
    return os.path.join(directory, base + ".local" + ext)


def _load_parser(file_path):
    if version < (3, 0):
        conf = config_parser.ConfigParser(allow_no_value=True)
        conf.read(file_path)
        return conf
    conf = config_parser.RawConfigParser()
    with open(file_path) as config_file:
        conf.read_file(config_file)
    return conf


def _read_option(file_path, section, option):
    conf = _load_parser(file_path)
    if conf.has_section(section) and conf.has_option(section, option):
        return True, conf.get(section, option)
    return False, None


def blank_to_none(value):
    """Treat a blank ini password as unset so clients skip AUTH."""
    if value is None:
        return None
    if hasattr(value, "strip") and value.strip() == "":
        return None
    return value


def get_config(section, option, file_path=os.path.join(BASE_DIR, 'login_jumper/conf/config.ini')):
    env_value = _env_override(section, option)
    if env_value:
        return env_value

    local_path = _local_override_path(file_path)
    if local_path and os.path.isfile(local_path):
        found, value = _read_option(local_path, section, option)
        if found:
            return value

    found, value = _read_option(file_path, section, option)
    if found:
        return value
    return None
