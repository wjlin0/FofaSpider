#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-05-16 19:57
# @File     :log
import os
import platform

from loging import time


def clear():
    """
    清屏
    :return:
    """
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def success(str_, **kwargs):
    return print_("success", str_, **kwargs)


def error(str_, **kwargs):
    return print_("error", str_, **kwargs)


def info(str_, **kwargs):
    return print_("info", str_, **kwargs)


def warning(str_, **kwargs):
    return print_("warning", str_, **kwargs)


def print_(c, s, t=None, colour=None):
    """
    :param c: 类型
    :param s: 输出的字符串
    :param t: 时间
    :param colour: 自定义颜色
    :return: 输出的样式
    """
    try:
        c = str(c).upper()
        t = f"\033[1;34m[{time.hms()}]\033[0m " if t is None else f"\033[1;34m[{t}]\033[0m "
        if c == "ERROR":
            colour = "31m" if colour is None else colour
            c = f"\033[1;{colour}[{c}]\033[0m "
        elif c == "SUCCESS":
            colour = "32m" if colour is None else colour
            c = f"\033[1;{colour}[{c}]\033[0m "
        elif c == "WARNING":
            colour = "33m" if colour is None else colour
            c = f"\033[1;{colour}[{c}]\033[0m "
        elif c == "INFO":
            colour = "34m" if colour is None else colour
            c = f"\033[1;{colour}[{c}]\033[0m "
        return print(t + c + s)
    except:
        raise
