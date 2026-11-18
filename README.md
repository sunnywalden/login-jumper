# Login Lumper

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://github.com/hhyo/archery/blob/master/LICENSE)
[![version](https://img.shields.io/badge/python-3.7.5-blue.svg)](https://www.python.org/downloads/release/python-375/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5c735378085b404caf09a441238ad034)](https://www.codacy.com/manual/sunnywalden/login-jumper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sunnywalden/login-jumper&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/sunnywalden/login-jumper.svg?branch=master)](https://travis-ci.org/sunnywalden/login-jumper)



## 部署

### 部署依赖

无pip环境的，请先部署pip（参考命令：sudo easy_install pip）。

1. 配置pip

---

sudo mkdir -p ~/.pip/
        
sudo echo "[global]" > ~/.pip/pip.conf
    
sudo echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf

sudo pip install --upgrade pip

---

2.安装虚拟环境

sudo pip install virtualenv

virtualenv --no-site-packages env

source env/bin/activate

### 部署方式 

二种部署方式，可选择pip安装或下载版本源码。

#### pip安装(推荐)

注：请替换'~/Documents/jump-server/'为安装路径

---

pip install login-jumper==2.1.5

---

#### 直接下载源码

##### 下载项目发布版本

下载release版本，解压

安装依赖

---

sudo pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

---


## 配置

安装目录 `login_jumper/conf/` 里的 `redis.ini` 和 `config.ini` 只保留本机回环示例，口令留空。不要把真实地址或口令写进这两个会被提交的文件。需要本机私有配置时，把同目录的 `*.ini.example` 复制为 `redis.local.ini` 或 `config.local.ini`（已在 `.gitignore` 中忽略）。

环境变量优先于 `*.local.ini`，`*.local.ini` 再优先于示例文件。推荐使用带前缀的变量：

- `LOGIN_JUMPER_SINGLE_HOST`、`LOGIN_JUMPER_SINGLE_PORT`、`LOGIN_JUMPER_SINGLE_DATABASE`、`LOGIN_JUMPER_SINGLE_PASSWORD`
- `LOGIN_JUMPER_CLUSTER_PASSWORD`
- `LOGIN_JUMPER_SERVER_JUMPER_HOST`、`LOGIN_JUMPER_SERVER_JUMPER_PORT`

仍兼容原有变量名：`host`、`port`、`database`、`password`、`jumper_host`、`jumper_port`、`sentry_id`、`roll_bar`。口令留空时不会向 Redis 发送 AUTH。

---

[single]

host = 127.0.0.1

port = 6379

database = 2

password =

---

堡垒机示例默认只指向本机。使用前用环境变量或 `config.local.ini` 改成你自己的地址。

---

[Server]

########## 堡垒机地址

jumper_host = 127.0.0.1

########## 堡垒机ssh端口

jumper_port = 22


[Session]

########## 会话超时时长

alive_interval = 20000000000


[System]

########## .bash_profile路径

system_profile = ~/.bash_profile

---

## 使用


### 指定主机参数，运行主程序

请通过-H参数指定需要登录的主机，支持主机名称或IP地址（查询需登录主机的主机名称或IP地址可登录堡垒机，执行jmp -a query）。如需要登录env3主机：

---
    source env/bin/activate
    
    jmp -H env3

---


## 注意事项

请在堡垒机设置中开启""Usmshell使用命令行方式"

