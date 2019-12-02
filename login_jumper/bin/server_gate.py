# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import json
import os
import sys

import rollbar
import sentry_sdk

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from login_jumper.bin.jumper_expect import jumper_login, query_servers, search_server
from login_jumper.bin.jumper_expect import server_login, str_to_dicts
from login_jumper.utils.get_logger import logger_generate
from login_jumper.utils import config
from login_jumper.utils.my_redis import redis_handler


class JumperServer:
    def __init__(self):
        self.logger = logger_generate()

        self.sentry_id = config.get_config('Sentry', 'sentry_id')
        self.roll_bar = config.get_config('App', 'roll_bar')

    def login_choice(self, host=None, action='login'):
        if self.roll_bar:
            rollbar.init(self.roll_bar)
            rollbar.report_message('Rollbar is configured correctly')
        if self.sentry_id:
            sentry_sdk.init(self.sentry_id)
        if action == 'login':
            self.logger.info('Login for {0} now'.format(host))
        else:
            self.logger.info('Query for all hosts!')
        # 登录堡垒机
        child = jumper_login()
        if not child:
            self.logger.error("Login jumper server failed")
        else:
            self.logger.info("Login jumper server success")

        if action == 'query':
            # 查询所有服务器
            servers_list, server = search_server(child)
            self.logger.debug('Debug servers {}'.format(servers_list))
            self.logger.info('########################################')
            if len(servers_list) > 3:
                str_to_dicts(servers_list[2:-1])
                print('\r\n'.join(servers_list[2:-1]))
            else:
                str_to_dicts(child, servers_list[:-1])
                print(servers_list)
        else:
            if not host:
                self.logger.error('Login host could not be None')
            self.login_in(child, host)

    def login_in(self, child, host):
        # 从缓存获取
        r = redis_handler()
        keys_list = r.keys('*' + host + '*')
        servers_list = list(map(lambda key: json.loads(r.get(key)), keys_list))
        if servers_list:
            server_match_result = True
            server_match_list = servers_list
        else:
            self.logger.warning("Host is not in Cache!")
            server_match_result, server_match_list, server_regex = query_servers(child, host)

        # 登录主机
        if server_match_result and server_match_list:
            if len(server_match_list) > 1:
                self.logger.warning("More than one host matched! Login in 1st auto!")
                self.logger.warning(server_match_list)
                print("More than one host matched!")
                print(server_match_list)
                child.close(force=True)
            if len(server_match_list) == 1:
                server_dict = server_match_list[0]
                server_login(child, server_dict)
        else:
            self.logger.error("No server matched found")
            print('No server matched')
            child.sendline('exit')


if __name__ == '__main__':
    jumper_server = JumperServer()
    jumper_server.login_choice(host='env4')
