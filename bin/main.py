# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import argparse
import os
import sys
import sentry_sdk
import rollbar

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from bin.jumper_expect import jumper_login
from bin.jumper_expect import server_login
from utils.get_logger import logger_generate
from utils import config


def main():
    logger = logger_generate(__name__)

    sentry_id = config.get_config('Sentry', 'sentry_id')
    roll_bar = config.get_config('App', 'roll_bar')

    if roll_bar:
        rollbar.init(roll_bar)
        rollbar.report_message('Rollbar is configured correctly')
    if sentry_id:
        sentry_sdk.init(sentry_id)

    parser = argparse.ArgumentParser(usage='python main.py [-H [host]]',
                                     description='Login server via jumper')
    parser.add_argument('-H', default='env4', type=str, dest='host',
                        help="specify the host"
                             "(default: env4)")

    args = parser.parse_args()
    host = args.host

    child = jumper_login()
    if not child:
        logger.info("Login jumper server failed")
    server_login(child, host)


if __name__ == '__main__':
    main()
