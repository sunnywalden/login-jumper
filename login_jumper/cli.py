# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.getcwd(), ".."))
sys.path.append(BASE_DIR)

from bin.server_gate import login_choice


def main():
    args = sys.argv
    print(args)
    parse_args = args[1:]
    login_choice(parse_args)


if __name__ == '__main__':
    main()
