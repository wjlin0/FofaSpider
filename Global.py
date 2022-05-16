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
import sys
from configparser import RawConfigParser

from loging.time import strftime, year, month, today
from urllib import parse
from loging import logs

ROOT_DIR = "./"
OUTPUT_DIR = ROOT_DIR + 'outputs/' + year() + '/' + month() + '/' + today() + '/'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
# 设置输出保存文件路径
SAVEFILENAME_PATH = OUTPUT_DIR + "IP-" + \
                    strftime("%H-%M") + \
                    ".txt"
SAVEINFO_PATH = OUTPUT_DIR + "INFO-" + \
                strftime("%H-%M") + \
                ".txt"

# 设置配置文件路径
CONFIG_PATH = 'config.ini'
if not os.path.exists(CONFIG_PATH):
    logs.error('配置文件不存在')
    sys.exit()

# 获取配置文件的对象
conn = RawConfigParser()
conn.read(CONFIG_PATH, encoding="utf-8")





def enBase64code(strs):
    return parse.quote(str(base64.b64encode(strs.encode("utf-8")), "utf-8"))


def deBase64code(strs):
    return parse.quote(str(base64.b64decode(parse.unquote(strs, "utf-8")), "utf-8"))
