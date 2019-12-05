# Login Lumper

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://github.com/hhyo/archery/blob/master/LICENSE)
[![version](https://img.shields.io/badge/python-3.7.5-blue.svg)](https://www.python.org/downloads/release/python-375/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5c735378085b404caf09a441238ad034)](https://www.codacy.com/manual/sunnywalden/login-jumper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sunnywalden/login-jumper&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/sunnywalden/login-jumper.svg?branch=master)](https://travis-ci.org/sunnywalden/login-jumper)

## 使用


## 部署

#### 部署依赖

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

部署方式，可选择pip安装或下载版本源码。

### pip安装(推荐)

注：请替换'~/Documents/jump-server/'为安装路径

---

pip install login-jumper==2.1.5

---

### 直接下载源码

#### 下载项目发布版本

下载release版本，解压

安装依赖

---

sudo pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

---


## 配置

进入安装路径下的conf目录，修改redis配置

---


[single]

host = 127.0.0.1

port = 6379

database = 2

password = 123456

---

修改堡垒机配置

---


[Server]

# 堡垒机IP

jumper_host = 192.168.1.100

# 堡垒机ssh端口

jumper_port = 22


[Session]

# 会话超时时长

alive_interval = 20000000000


[System]

# .bash_profile路径

system_profile = ~/.bash_profile

---

## 使用

#### 进入路径bin

#### 指定主机参数，运行主程序

请通过-H参数指定需要登录的主机，支持主机名称或IP地址（查询需登录主机的主机名称或IP地址可登录堡垒机，执行jmp -a query）。如需要登录env3主机：

---
    source env/bin/activate
    
    jmp -H env3

---


### 注意事项

请在堡垒机设置中开启""Usmshell使用命令行方式"

