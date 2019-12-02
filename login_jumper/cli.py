# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import os
import sys
import optparse

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from login_jumper.bin.server_gate import JumperServer
from login_jumper.utils.get_logger import logger_generate

VERSION = '2.1.3'

logger = logger_generate()


def main():
    parser = optparse.OptionParser(
        version='%prog version ' + VERSION,

        usage='python server_gate.py [-H [host]] [-a [action]]',
        description='Login server via jumper')
    parser.add_option(
        '-H', '--host',
        dest='host',
        help="specify the host, default: env4",
        metavar='HOST',
        default='env4',
    )
    parser.add_option(
        '-a', '--action',
        dest='action',
        help="specify the type, login or query, default: login",
        metavar='ACTION',
        choices=['login', 'query'],
        default='login',
    )
    options, args = parser.parse_args()
    host = options.host
    action = options.action

    if not host and action != 'query':
        parser.error('missing host')

    jumper_server = JumperServer()
    jumper_server.login_choice(host=host, action=action)


if __name__ == '__main__':
    main()
