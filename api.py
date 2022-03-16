#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-02-26 15:56
# @File     :fofaapi
import optparse
import loguru
import FofaApi
import FofaApp

import click


@click.group()
@click.version_option("v1.0.0")
# @click.option('--code', help='查询条件')
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
    click.version_option()
    main()

# usage = 'usage: python %prog -a fofa -c port=3306'
# parser = optparse.OptionParser(usage=usage, version="2.0.0")
#
# parser.add_option('-a', dest='app', type='string', help='目前支持 fofa 和 fofaapi查询', default="fofa")
# parser.add_option('-c', dest='code', type='string', help='code 查询的条件', default='')
# # parser.add_option('-k', dest='cookies', type='string', help='cookies', default='')
# parser.add_option('-s', dest='size', type='string', help='fofaapi_size 默认100', default="100")
# parser.add_option('-p', dest='page', type='string', help='fofaapi_pag 默认第一页', default="1")
# (options, args) = parser.parse_args()
# app = options.app
# code = options.code
# size = options.size
# page = options.page
#
# loguru.logger.info(code)
# if app == 'fofa':
#     FofaApp.FofaApp(code).run()
# elif app == 'fofaapi':
#     FofaApi.FofaApi(code, size, page).run()
# else:
#     print(f'暂不支持，{app}该平台')
