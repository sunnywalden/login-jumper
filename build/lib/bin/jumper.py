# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import argparse
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from bin.server_gate import login_choice

if __name__ == '__main__':

    args = sys.argv
    # parser = argparse.ArgumentParser(usage='python server_gate.py [-H [host]]' [-T ['login', 'query']],
    #                                  description='Login server via jumper')
    # parser.add_argument('--host', '-H', default='env4', type=str, dest='host',
    #                     help="specify the host"
    #                          "(default: env4)")
    # parser.add_argument('--action', '-T', choices=['login', 'query'], default='login', type=str, dest='action',
    #                     help="specify the type, login or query"
    #                          "(default: login)")
    #
    # action = 'login'
    #
    # if len(args) >= 2:
    #     host = args[1]
    #     if len(args) > 2:
    #         action = args[2]
    #     final_args.host = host
    #     final_args.action = action
    # else:
    #     final_args.action = 'query'

    # final_args = parser.parse_args(args[1:])
    print(args)
    parse_args = args[1:]
    login_choice(parse_args)
