# !/usr/bin/env python
# coding=utf-8
# author: sunnywalden@gmail.com

import paramiko

from login_jumper.utils.get_logger import logger_generate
from login_jumper.utils.jumper_info import jumper_info


class JumperLogin:
    def __init__(self):
        self.logger = logger_generate(__name__)
        self.login_info = jumper_info()
        self.ssh = paramiko.SSHClient()

    def conn_jumper(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.login_info["host"], self.login_info["port"], self.login_info["username"], self.login_info["password"])

    def run_jumper(self, command):
        self.conn_jumper()
        stdin, stdout, stderr = self.ssh.exec_command(command)
        servers_info = stdout.read().decode('utf-8')
        if stderr:
            print("Login jumper failed", stderr)
        else:
            print("Login jumper success!")
            print(servers_info)

        self.ssh.close()

        return_info = servers_info if not stderr else stderr
        return return_info


