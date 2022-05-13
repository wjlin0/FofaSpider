#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-02-11 19:35
# @File     :Global.py
import base64
import os
import platform
import time
from configparser import RawConfigParser
from pathlib import Path
from urllib import parse

from loguru import logger


def enBase64code(strs):
    return parse.quote(str(base64.b64encode(strs.encode("utf-8")), "utf-8"))


def deBase64code(strs):
    return parse.quote(str(base64.b64decode(parse.unquote(strs, "utf-8")), "utf-8"))


SYSTEMTYPE = platform.system()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
OUTPUT_DIR = ROOT_DIR + 'outputs/' + str(time.strftime("%Y-%m-%d", time.localtime(time.time()))) + '/'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
# 设置输出保存文件路径
SAVEFILENAME_PATH = OUTPUT_DIR + "IP-" + \
                    str(time.strftime("%Y-%m-%d-%H", time.localtime(time.time()))) + \
                    ".txt"
SAVEINFO_PATH = OUTPUT_DIR + "INFO-" + \
                str(time.strftime("%Y-%m-%d-%H", time.localtime(time.time()))) + \
                ".txt"

# 设置配置文件路径
CONFIG_PATH = ROOT_DIR + 'config' + '/' + 'config.ini'
if not os.path.exists(CONFIG_PATH):
    logger.error('配置文件不存在')
    exit()

# 获取配置文件的对象
conn = RawConfigParser()
conn.read(CONFIG_PATH)


# DB = {
#     'host': conn.get('database', 'host') if conn.get('database', 'host') is None else '127.0.0.1',
#     'type': conn.get('database', 'type') if conn.get('database', 'type') is None else 'mysql',
#     'port': conn.get('database', 'port') if conn.get('database', 'port') is None else '3306',
#     'user': conn.get('database', 'user') if conn.get('database', 'user') is None else 'root',
#     'pass': conn.get('database', 'pass') if conn.get('database', 'pass') is None else 'root',
#     'charset': conn.get('database', 'charset') if conn.get('database', 'charset') is None else 'utf8',
#     'dbname': conn.get('database', 'dbname') if conn.get('database', 'dbname') is None else 'test',
# }
