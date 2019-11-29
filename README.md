# Login Lumper

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](http://github.com/hhyo/archery/blob/master/LICENSE)
[![version](https://img.shields.io/badge/python-3.7.5-blue.svg)](https://www.python.org/downloads/release/python-375/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/5c735378085b404caf09a441238ad034)](https://www.codacy.com/manual/sunnywalden/login-jumper?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sunnywalden/login-jumper&amp;utm_campaign=Badge_Grade)
[![Build Status](https://travis-ci.org/sunnywalden/login-jumper.svg?branch=master)](https://travis-ci.org/sunnywalden/login-jumper)

## 部署

### 下载项目代码

#### 部署依赖

无pip环境的，请先部署pip（参考命令：sudo easy_install pip）。

---
    sudo mkdir -p ~/.pip/
        
    sudo echo "[global]" > ~/.pip/pip.conf
    
    sudo echo "index-url = https://pypi.tuna.tsinghua.edu.cn/simple" >> ~/.pip/pip.conf
    
    sudo pip install --upgrade pip && sudo pip install -r requirements.txt
 
---
 
   
#### 更新conf/路径下config.py文件中的堡垒机登录信息
注：jumper_host为堡垒机地址，jumper_port为堡垒机ssh端口，必须设置。

---

jumper_host = 'Host IP'

jumper_port = 'Host ssh Port'  

---  

#### 设置堡垒机登录信息环境变量

注：username为你的堡垒机账号，一般为姓名全拼，password为堡垒机账户密码必须设置，非首次登录可忽略。

---

    export jumper_username='Your Username'

    export jumper_password='Your Password'

---


### 使用

#### 进入路径bin

---

    cd bin/

---

#### 指定主机参数，运行主程序

请通过-H参数指定需要登录的主机，支持主机名称或IP地址（需登录主机的主机名称或IP地址可登录堡垒机，执行ls命令查看）。如需要登录env3主机：

---

    python main.py -H env3

---


### 注意事项

请在堡垒机设置中开启""Usmshell使用命令行方式"