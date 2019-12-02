# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import fcntl
import struct
import sys
import termios


def get_terminal_size():
    s = struct.pack("HHHH", 0, 0, 0, 0)
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, s))
    return a[0], a[1]
