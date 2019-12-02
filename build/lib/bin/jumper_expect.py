# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import os
import re
import sys
import pexpect
import signal
from sentry_sdk import capture_exception
import rollbar
import json

from utils import config
from utils.get_logger import logger_generate
from utils.jumper_info import jumper_info
from utils.terminal_size import get_terminal_size
from utils.my_redis import redis_handler

version = sys.version_info
v_info = str(version.major) + '.' + str(version.minor) + '.' + str(version.micro)

# 判断Python版本号
if version < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

logger = logger_generate(__name__)


def search_string(string):
    if re.match(r'^\d+$', string):
        searching_str = ':' + string
    else:
        searching_str = '/' + string
    return searching_str


def child_timeout(child_timout):
    logger.info("Debug console info: %s" % child_timout.before)
    logger.info("Timeout while searching host!")
    logger.info("Loging out jumper!")
    logger.info('Left interactive mode.')
    logger.info('########################################')


def filter_output(s):
    global child
    global output_buf, search_str, server_exit, login_status, login_prompt, \
        user_prompt, root_user, login_user, output_buf_size, server_match_result

    root_str = ']#'
    jumper_str = 'USMShell'
    if version < (3, 0):
        output_buf += s
    else:
        output_buf += s.decode('utf-8')
    output_buf = output_buf[-output_buf_size:]
    server = search_str[1:]
    if login_prompt.search(output_buf):
        if user_prompt.search(output_buf) and not login_status:
            logger.info("Login server %s success!" % server)
            login_user = 1
            login_status = True
        if root_str in output_buf:
            if login_user < 2 and not server_exit:
                logger.info("Login server as root!")
                login_user = 2
                root_user = True
            if jumper_str in output_buf and not server_exit:
                logger.info("Exit from server success!")
                server_exit = True
                child.sendline("ls")

    return s


def filter_input(s):
    global child
    global user_prompt, filter_buf, filter_buf_size, search_str, server_exit, \
        jumper_exit, root_user, login_status, login_user

    exit_str = 'exit'
    quit_str = ':q'
    if version < (3, 0):
        filter_buf += s
    else:
        filter_buf += s.decode('utf-8')
    filter_buf = filter_buf[-filter_buf_size:]

    if exit_str in filter_buf:
        if login_user == 1 and login_status:
            if not server_exit:
                logger.info("Start exit from server!")
                logger.info("Logout server success!")
                server_exit = True
        else:
            if root_user and login_user == 2:
                logger.info("Logout as root to normal!")
                root_user = False
    if (exit_str in filter_buf and server_exit) or quit_str in filter_buf and not jumper_exit:
        logger.info("Logout jumper success!")
        logger.info('########################################')
        jumper_exit = True

    return s


def sigwinch_pass_through(sig, data):
    global child

    if not child.closed:
        child.setwinsize(*get_terminal_size())


def jumper_login():
    jumper_infos = jumper_info()
    host = jumper_infos["host"]
    port = jumper_infos["port"]
    system_profile = config.get_config('System', 'system_profile')

    if system_profile:
        os.system('source ' + system_profile)
    username = os.getenv("jumper_username")
    lang = os.getenv("LANG")
    lc_type = os.getenv("LC_CTYPE")

    if not username:
        if version < (3, 0):
            username = raw_input('jumper server loging username: ')
        else:
            username = input('jumper server loging username: ')
        os.environ['jumper_username'] = username
        with open(system_profile, 'a+') as f:
            if username not in f.readlines():
                f.writelines(('\n' + 'export jumper_username=' + username + '\n'))

    # set environment vars
    if not lang:
        lang = 'en_US.utf8'
        os.environ['LANG'] = lang
        with open(system_profile, 'a+') as f:
            if lang not in f.readlines():
                f.writelines(('\n' + 'export LANG=' + lang + '\n'))
    if not lc_type:
        lc_type = 'en_US.utf8'
        os.environ['LC_CTYPE'] = lc_type
        with open(system_profile, 'a+') as f:
            if lc_type not in f.readlines():
                f.writelines(('\n' + 'export LC_CTYPE=' + lc_type + '\n'))

    command = 'ssh -o StrictHostKeyChecking=no %(user)s@%(host)s -p %(port)s' \
              % {"user": username, "host": host, "port": str(port)}
    global child
    child = pexpect.spawn(command, maxread=1024 * 1024 * 1024, timeout=30)
    child.setwinsize(*get_terminal_size())
    signal.signal(signal.SIGWINCH, sigwinch_pass_through)
    logger.info('########################################')
    logger.info('Loging jumper!')
    index1 = child.expect('usmshell')
    if index1 != 0:
        logger.error("Login jump failed!")
        logger.info('########################################')
        return False
    logger.info('Loging jumper success!')
    return child


def search_server(host=None):
    global child

    server_info_list = []
    server = None

    if host:
        host_search_str = search_string(host)
        server = host_search_str[1:]
        host_search_str = '\d+ .+' + server + '.+' + '\r\n'

        host_search_str = host_search_str.encode(encoding='utf-8')
        searcher_prompt = re.compile(host_search_str)

    if host:
        child.sendline('ls')
        index_server = child.expect([searcher_prompt, pexpect.EOF, pexpect.TIMEOUT])
    else:
        child.sendline('ls')
        index_server = child.expect([searcher_prompt, pexpect.EOF, pexpect.TIMEOUT])
        server_infos = child.after
        if server_infos:
            if version < (3, 0):
                split_str = '[K'

            else:
                split_str = b'[K'
            server_info_list = server_infos.split(split_str)

    if host and index_server <= 0:
        if host:
            logger.info("Search host %s success!" % server)
        res = child.after
        server_infos = res
        logger.debug("Debug servers hosts: %s" % server_infos)
        logger.debug("Debug match string: %s " % child.after)
        if version < (3, 0):
            split_str = '[K'

        else:
            split_str = b'[K'
        server_info_list = server_infos.split(split_str)

        logger.debug("Debug servers list:%s" % server_info_list)

        if not version < (3, 0) and server:
            server = server.encode('utf-8')

    elif host and index_server == 2:
        child_timeout(child)
    else:
        logger.debug("Debug console info: %s" % child.before)

    return server_info_list, server


def query_servers(host=None):
    jumper_login()

    server_info_list, server_regex = search_server(host)

    servers_dict_list = []

    for server_info in server_info_list:
        server_dict = {}

        server_list = server_info.split()
        logger.debug("Debug server info: %s %s" % (server_info, server_list))

        if version < (3, 0):
            ssh_str = 'ssh'
            ssh_index = server_list.index(ssh_str)
            try:
                server_dict["id"] = server_list[0].split(":")[0]
                server_dict["name"] = server_list[1].split('(')[0]
                server_dict["host"] = server_list[ssh_index - 1].split(":")[0]
                server_dict["port"] = server_list[ssh_index - 1].split(":")[1]
                server_dict["user"] = server_list[ssh_index + 1]
            except Exception as e:
                capture_exception(e)
                rollbar.report_exc_info()
                logger.error("Exception while get server info: %s " % e)
            else:
                # 存储到缓存
                r = redis_handler()
                name_key = server_dict["name"]
                r.set(name_key, json.dumps(server_dict))
                ip_key = server_dict["host"]
                r.set(ip_key, json.dumps(server_dict))

                servers_dict_list.append(server_dict)
                logger.info("Server host info: %s" % server_dict)
                break

        else:
            ssh_str = 'ssh'.encode('utf-8')

            ssh_index = server_list.index(ssh_str)
            try:
                server_dict["id"] = server_list[0].split(b":")[0]
                server_dict["name"] = server_list[1].split(b'(')[0]
                server_dict["host"] = server_list[ssh_index - 1].split(b":")[0]
                server_dict["port"] = server_list[ssh_index - 1].split(b":")[1]
                server_dict["user"] = server_list[ssh_index + 1]
            except Exception as e:
                capture_exception(e)
                rollbar.report_exc_info()
                logger.error("Exception while get server info: %s " % e)
            else:
                servers_dict_list.append(server_dict)
                logger.info("Server host info: %s" % server_dict)
                break

    searching_str = search_string(host)
    server_info = searching_str[1:]

    # global变量
    global end_str
    end_str = '\[1B\[1024D\[K'
    global search_prompt, search_prompt_name, search_prompt_ip, \
        login_prompt, user_prompt, root_prompt
    search_prompt = re.compile('\d+: .+' + server_info + '.+' + end_str)
    search_prompt_name = re.compile('\d+: ' + server_info + '.+' + '\d+.\d+.\d+.\d+:\d+' + 'ssh' + '.+' + end_str)
    search_prompt_ip = re.compile('\d+: .+' + server_info + ':\d+' + 'ssh' + '.+' + end_str)
    login_prompt = re.compile('Welcome to Alibaba Cloud Elastic Compute Service !')
    user_prompt = re.compile('\[\w+@\w+ ~\]\$')
    root_prompt = re.compile('\[\w+@\w+ \w+\]#')

    server_match_bool, server_match_list = get_server(servers_dict_list, host)

    return server_match_bool, server_match_list, server_regex


def server_match(server_dicts, host, server_match_bool=False):
    server_match_list = []

    if not version < (3, 0):
        host = host.encode('utf-8')
    for server_info_dict in server_dicts:
        if host in server_info_dict["name"] or server_info_dict["host"]:
            server_match_bool = True
            server_match_list.append(server_info_dict)

    return server_match_bool, server_match_list


def get_server(server_dicts, server_s):
    global end_str

    global filter_buf, filter_buf_size, output_buf, output_buf_size

    logger.info("Start search for host: %s" % server_s)

    server_match_bool, server_match_list = server_match(server_dicts, server_s)

    return server_match_bool, server_match_list


def server_login(server_info_dict):
    global child
    global filter_buf, filter_buf_size, output_buf, output_buf_size

    filter_buf, output_buf = '', ''
    filter_buf_size, output_buf_size = 125, 1024 * 1024 * 1024

    server_info = server_info_dict["host"]

    if not version < (3, 0):
        server_info = server_info.decode('utf-8')

    global search_str
    search_str = server_info

    ending_str = '\[1B\[1024D\[K'

    global search_prompt, search_prompt_name, search_prompt_ip, \
        login_prompt, user_prompt, root_prompt

    search_prompt = re.compile('\d+: .+' + server_info + '.+' + ending_str)
    search_prompt_name = re.compile('\d+: ' + server_info + '.+' + '\d+.\d+.\d+.\d+:\d+' + 'ssh' + '.+' + ending_str)
    search_prompt_ip = re.compile('\d+: .+' + server_info + ':\d+' + 'ssh' + '.+' + ending_str)
    login_prompt = re.compile('Welcome to Alibaba Cloud Elastic Compute Service !')
    user_prompt = re.compile('\[\w+@\w+ ~\]\$')
    root_prompt = re.compile('\[\w+@\w+ \w+\]#')

    # 登录状态及用户
    global login_user, server_exit, jumper_exit, login_status
    login_user = 0
    server_exit, jumper_exit, login_status = False, False, False

    if server_info_dict:
        if version < (3, 0):
            login_server_cmd = 'ssh ' + server_info_dict["user"] + '@' + server_info_dict["host"] + \
                               " -p " + server_info_dict["port"]
        else:
            login_server_cmd = b'ssh ' + server_info_dict["user"] + b'@' + server_info_dict["host"] + b" -p " + \
                               server_info_dict[
                                   "port"]
        child.sendline(login_server_cmd)
        logger.info("Entering interactive ssh dialog!")
        child.interact(output_filter=filter_output, input_filter=filter_input)
    else:
        logger.error("Jumper server Wrong!")

    child.close(force=True)
