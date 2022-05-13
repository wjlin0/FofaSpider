#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-02-26 15:56
# @File     :fofaapi
import loguru

import FofaApp
import click

from FofaApi import FofaApiClass


@click.group()
@click.version_option("v2.0.2")
def main():
    pass


@main.command()
@click.option('-s', '--size', help="默认100", default=100)
@click.option('-p', '--page', help="默认第一页", default=1, )
@click.option('-c', '--code', help="查询条件")
def FofaApi(size, page,code):
    """
    Fofaapi 接口
    """
    loguru.logger.info(code)
    FofaApiClass(code, size, page).run()


@main.command()
@click.option('-c', '--code', help="查询条件")
def fofaapp(code):
    """
    Fofaapp 平台
    """
    loguru.logger.info(code)
    FofaApp.FofaApp(code).run()


if __name__ == '__main__':
    main()
