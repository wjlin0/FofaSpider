#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-02-26 15:56
# @File     :fofaapi


import FofaApp
import click

import shoDan
from FofaApi import FofaApiClass
from Global import conn
from loging import logs


@click.group()
@click.version_option(conn.get("fofa", "version"))
def main():
    logs.clear()
    logs.success("慢慢在完善刚起步 有什么建议 联系邮箱")


@main.command()
@click.option('-s', '--size', help="默认100", default=100)
@click.option('-p', '--page', help="默认第一页", default=1, )
@click.option('-c', '--code', help="查询条件")
def FofaApi(size, page, code):
    """
    Fofaapi 接口
    """
    logs.info("请求的参数: " + str(code))
    FofaApiClass(code, size, page).run()


@main.command()
@click.option('-c', '--code', help="查询条件")
def fofaapp(code):
    """
    Fofaapp 平台
    """
    logs.info("请求的参数: " + str(code))
    FofaApp.FofaApp(code).run()


@main.command()
@click.option('-c', '--code', help="查询条件")
def shoDanApp(code):
    """
    shoDan 平台
    """
    logs.info("请求的参数: " + str(code))
    shoDan.shoDanApp(code).run()


if __name__ == '__main__':
    main()
