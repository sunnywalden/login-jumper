# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import argparse
import os
import sys
import sentry_sdk

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from bin.jumper_expect import jumper_login
from bin.jumper_expect import server_login
from utils.get_logger import Logger
from utils import config


def main():
    log = Logger()
    logger = log.logger_generate(__name__)

    # aliyun setting
    sentry_id = config.get_config('Sentry', 'sentry_id')

    version = sys.version_info
    v_info = str(version.major) + '.' + str(version.minor) + '.' + str(version.micro)

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
