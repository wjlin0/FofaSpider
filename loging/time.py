#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-05-16 20:02
# @File     :time
from datetime import datetime


def now():
    return datetime.now()


def timestamp():
    return now().timestamp()


def year():
    return now().strftime("%Y")


def month():
    return now().strftime("%m")


def today():
    return now().strftime("%d")


def hms():
    return now().strftime("%H:%M:%S")


def ymd():
    return now().strftime("%Y-%m-%d")


def strftime(str_):
    return now().strftime(str_)
