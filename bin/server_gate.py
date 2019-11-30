# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import argparse
import os
import sys
import sentry_sdk
import rollbar
import json

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from bin.jumper_expect import jumper_login, search_server, query_servers, server_match
from bin.jumper_expect import get_server
from bin.jumper_expect import server_login
from utils.get_logger import logger_generate
from utils import config
from utils.my_redis import redis_handler


def login_in():
    logger = logger_generate(__name__)

    sentry_id = config.get_config('Sentry', 'sentry_id')
    roll_bar = config.get_config('App', 'roll_bar')

    if roll_bar:
        rollbar.init(roll_bar)
        rollbar.report_message('Rollbar is configured correctly')
    if sentry_id:
        sentry_sdk.init(sentry_id)

    parser = argparse.ArgumentParser(usage='python server_gate.py [-H [host]]',
                                     description='Login server via jumper')
    parser.add_argument('--host', '-H', default='env4', type=str, dest='host',
                        help="specify the host"
                             "(default: env4)")
    parser.add_argument('--type', '-T', choices=['login', 'query'], default='login', type=str, dest='type',
                        help="specify the type, login or query"
                             "(default: login)")

    args = parser.parse_args()
    host = args.host

    # 登录堡垒机
    child = jumper_login()
    if not child:
        logger.info("Login jumper server failed")

    # 从缓存获取
    r = redis_handler()
    keys_list = r.keys('*' + host + '*')
    servers_list = list(map(lambda key: json.loads(r.get(key)), keys_list))
    if servers_list:
        server_match_result = True
        server_match_list = servers_list
    else:
        logger.warning("Host is not in Cache!")
        server_match_result, server_match_list, server_regex = query_servers(host)

    # 登录主机
    if server_match_result and server_match_list:
        if len(server_match_list) >= 1:
            logger.warning("More than one host matched! Login in 1st auto!")
            server_dict = server_match_list[0]
        else:
            server_dict = server_match_list
        server_login(server_dict)
    else:
        logger.error("No server matched found")
        child.sendline(':q')


if __name__ == '__main__':
    login_in()
