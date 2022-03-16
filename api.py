#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-02-26 15:56
# @File     :fofaapi
import FofaApi
import FofaApp

import click


@click.group()
@click.version_option("v1.0.0")
def main():
    pass


@main.command()
@click.option('-s', '--size', help="默认100", default=100)
@click.option('-p', '--page', help="默认第一页", default=1, )
@click.option('-c', '--code', help="查询条件")
def FofaApi(code, size, page):
    """
    Fofaapi 接口
    """
    FofaApi.FofaApi(code, size, page).run()


@main.command()
@click.option('-c', '--code', help="查询条件")
def fofaapp(code):
    """
    Fofaapp 平台
    """
    FofaApp.FofaApp(code).run()


if __name__ == '__main__':
    main()
#    FofaApp.FofaApp("port=\"3306\"").run()
