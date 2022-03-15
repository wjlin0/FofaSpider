#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-03-15 17:18
# @File     :FofaApi
import json
import re

from loguru import logger
import requests

from Global import conn, enBase64code, SAVEFILENAME_PATH


class FofaApi:
    def __init__(self, code, size, page):
        self.url = 'https://fofa.info/api/v1/search/all'
        self.code = enBase64code(code)
        self.size = size
        self.page = page
        self.conn = conn
        try:
            self.email = self.conn.get('fofa', 'fofa_email')
            self.key = self.conn.get('fofa', 'fofa_key')
        except:
            logger.error('去配置文件把lz的fofa_email 和fofa_key加上')
            exit()
        self.ReqUrl = self.getReqUrl()
        self.Results = self.getResults()
        self.rCode = code

    def getResults(self):
        text = requests.get(url=self.ReqUrl).text
        results = json.loads(text)
        return results

    def getReqUrl(self):
        return self.url + '?email=' + self.email + '&key=' \
               + self.key + '&qbase64=' + self.code + '&page=' \
               + self.page + '&size=' + self.size

    def run(self):
        # print(self.Results)
        if self.Results['error']:
            logger.error(self.Results['errmsg'])
            exit()
        if self.Results['size'] == 0:
            logger.error('没有，滚')
            exit()
        Host = ['search Fofapi - ' + self.rCode + f' - {self.Results["size"]}' + '\n']
        for results in self.Results['results']:
            Host.append(results[0] + '\n')

        SaveFileNamePath = ''.join(re.findall('.*IP-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}'
                                              , SAVEFILENAME_PATH)) + '-api0.txt'
        # print(SaveFileNamePath)
        with open(SaveFileNamePath, 'a+')as f:
            f.writelines(Host)

        SaveFileNamePath = ''.join(re.findall('.*IP-[0-9]{4}-[0-9]{2}-[0-9]{2}-[0-9]{2}'
                                              , SAVEFILENAME_PATH)) + '-api1.csv'
        Host = ['search Fofapi - ' + self.rCode + f' - {self.Results["size"]}'+ ',,' + '\n']
        for results in self.Results['results']:
            Host.append(','.join(results) + '\n')
        with open(SaveFileNamePath, 'a+')as f:
            f.writelines(Host)
        logger.success(f'搜索完成 - {self.Results["size"]}条数据 - query:{self.Results["query"]}')