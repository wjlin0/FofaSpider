#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-02-26 16:07
# @File     :FofaApp
import asyncio

import json
import os
import time

import aiohttp
import requests
from bs4 import BeautifulSoup
from loguru import logger
from prettytable import PrettyTable, DEFAULT

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import Global


def _clear():
    if Global.SYSTEMTYPE == 'Windows':
        os.system('cls')
    elif Global.SYSTEMTYPE == 'Linux':
        os.system('clear')


def printfUserinfo(username, useremail, usergroup, userapikey, ):
    _clear()
    table = PrettyTable(['用户名', '邮箱', '组别', 'APIKEY'])
    table.add_row([username, useremail, usergroup, userapikey])
    table.set_style(DEFAULT)
    print(table)


def get_url_ip(soup, filename):
    tags = soup.find_all(name="div", attrs={"class": "addrLeft"}, limit=10)
    urls = []
    ips = []
    temp = []
    tempjson = {}
    try:
        for tag in tags:
            tag = tag.find(name="span", attrs={"class": "aSpan"})
            if tag.find(name="a", attrs={"target": "_blank"}) is None:
                t = tag.string
                # open(filename, "a+", encoding="utf-8").write(t + '\n')
                # with open(filename, "a+", encoding="utf-8") as f:
                #     f.write("ip: " + t + "\n")
                ips.append("ip: " + t + "\n")
            if tag.find(name="a", attrs={"target": "_blank"}):
                t = tag.find(name="a", attrs={"target": "_blank"})['href']
                # print(t)
                # with open(filename, "a+", encoding="utf-8") as f:
                #     f.write("url: " + t + "\n")
                urls.append("url: " + t + "\n")
        if ips:
            for ip in ips:
                if ip not in temp:
                    temp.append(ip)
        ips = temp
        temp = []
        # print(temp)
        if urls:
            for url in urls:
                if url not in temp:
                    temp.append(url)
        urls = temp
        # print(temp)
        with open(filename, "a+", encoding="utf-8")as f:
            if ips:
                f.writelines(ips)
            if urls:
                f.writelines(urls)
        # tempjson['ips'] = ips
        # tempjson['urls'] = urls
        # json_obj = json.dumps(tempjson,indent=4,ensure_ascii=False)
        # # print(json_obj)
        # open("txt.txt",'a+',encoding="utf-8").write(json_obj)
        return True
    except Exception as e:
        logger.error(e)
        return False


async def get_aiphttp_soup(session, requrl, page, name=None):
    # print(requrl)
    while 1:
        try:
            async with session.get(requrl, verify_ssl=False, ) as html:
                if name is not None:
                    logger.info(f"开始请求 {name},page={page}")
                content = await html.text()
                if 'Retry later' in content:
                    logger.warning("忙碌")
                    time.sleep(60)
                    continue
                if html.status != 200:
                    return False
                if name is not None:
                    logger.info(f"结束请求 {name},page={page}")
                return BeautifulSoup(content, "html.parser")
        except Exception as e:
            logger.error(e)
            # html.close()
            return False


async def asyncreqone(cookies, headers, requrl, page, reqcode, filename):
    requrl_list = [requrl + f"/result?page={pa + 1}&page_size=10&qbase64={Global.deBase64code(reqcode)}" for pa in
                   range(int(page))]
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        task_list = [asyncio.create_task(get_aiphttp_soup(session=session, requrl=url, page=pa + 1)) for pa, url in
                     enumerate(requrl_list)]
        _results, p = await asyncio.wait(task_list, timeout=100, return_when="ALL_COMPLETED")
        for _result in _results:
            if not _result.result():
                continue
            if not get_url_ip(soup=_result.result(), filename=filename):
                continue


async def asyncreqthree(requrl, page, cookies, headers, filename):
    requrl_list = [requrl + f"&page={pa + 1}&&page_size=10" for pa in range(int(page))]
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        task_list = [asyncio.create_task(get_aiphttp_soup(session=session, requrl=url, page=pa + 1)) for pa, url in
                     enumerate(requrl_list)]
        _results, p = await asyncio.wait(task_list, timeout=100, return_when="ALL_COMPLETED")
    for _result in _results:
        if not _result.result():
            continue
        if not get_url_ip(soup=_result.result(), filename=filename):
            continue


def getCityurls(soup):
    """
    获得所有城市的url
    :param soup:
    :return:
    """
    Cityurls = {}
    countryLi = soup.find_all(name="li", attrs={"class": "countryLi"})
    for tag in countryLi:
        countryname = tag.find(name="div", attrs={"class": "titleLeft"}).a.string
        cityTags = tag.find_all(name="div", attrs={"class": "listCont table-label table-label-left"})
        temp = {}
        for city in cityTags:
            temp[city.a.string] = city.a['href']
        Cityurls[countryname] = temp
    # print(Cityurls)
    return Cityurls


class FofaApp:

    def __init__(self, code):
        self.url = "https://fofa.info"
        self.filename = Global.SAVEFILENAME_PATH
        self.conn = Global.conn
        self.code = code
        self.username = ""
        self.usergroup = ""
        self.useremail = ""
        self.userApikey = ""
        # self.cookies = cookies
        self.cookies = self.getcookies()
        # self.cookies = {
        #     'fofa_token': self.conn.get('fofa', 'fofa_token'),
        #     'user': self.conn.get('fofa', 'user'),
        #     'refresh_token': self.conn.get('fofa', 'refresh_token')
        # }
        self.ftoken = dict(name='fofa_token', value=self.cookies['fofa_token'])
        self.fuser = dict(name='user', value=self.cookies['user'])
        self.fretoken = dict(name='refresh_token', value=self.cookies['refresh_token'])
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.76 ',
            'referer': self.url,
            'content-type': 'text/html; charset=utf-8',
        }
        self.page = ""
        self.num = ""
        self.Num = None
        self.href = {}
        self.driver = self.setDriver()

    def setDriver(self):
        """
        设置driver，用来模拟登录
        :return:
        """
        global driver
        try:
            chrome_options = Options()
            chrome_options.add_argument('–ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_argument('headless')
            driverPath = ""
            driverInstall = Global.ROOT_DIR + "/driver/"
            if not os.path.exists(driverInstall):
                os.mkdir(driverInstall)
            for fpathe, dirs, fs in os.walk(driverInstall):
                for f in fs:
                    if 'chromedriver.exe' in os.path.join(fpathe, f):
                        driverPath = os.path.join(fpathe, f)
                        break
            try:
                if driverPath == "":
                    driver = webdriver.Chrome(executable_path=ChromeDriverManager(path=driverInstall).install(),
                                              chrome_options=chrome_options)
                else:
                    driver = webdriver.Chrome(executable_path=driverPath,
                                              chrome_options=chrome_options)
            except:
                driver = webdriver.Chrome(executable_path=ChromeDriverManager(path=driverInstall).install(),
                                          chrome_options=chrome_options)

            # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)

            driver.get(url=self.url)
            driver.delete_all_cookies()
            # print(self.cookies)
            # driver.add_cookie(cookie_dict=self.cookies)
            driver.add_cookie(cookie_dict=self.ftoken)
            driver.add_cookie(cookie_dict=self.fretoken)
            driver.add_cookie(cookie_dict=self.fuser)
            driver.get(url=self.url)
            return driver
        except Exception as e:
            logger.error(f"{e}")
            exit()

    def getDriverSoup(self, requrl, sign):
        """
        得到driver生成的源码对象（动态获得）
        :param requrl: 请求url
        :param sign: 标志为False，
        :return: 返回soup对象
        """
        try:
            while 1:
                self.driver.get(url=requrl)
                if 'Retry later' in self.driver.page_source:
                    time.sleep(10)
                    continue
                if '查询语法错误' in self.driver.page_source:
                    logger.error('别看了没有任何数据')
                    self.driver.close()
                    self.driver.quit()
                    exit()
                if not sign:
                    WebDriverWait(driver=self.driver, timeout=15).until(
                        expected_conditions.presence_of_element_located((By.CLASS_NAME, "countryTitle")))
                html = self.driver.page_source
                return BeautifulSoup(html, "html.parser")
        except Exception as e:
            logger.error('别看了没有任何数据')
            self.driver.close()
            self.driver.quit()
            exit()

    def getUserinfo(self):
        """
        :return: 个人信息
        """
        userinfo = {}
        requrl = self.url + '/personalData'
        soup = self.getDriverSoup(requrl, True)
        tags = soup.find_all(name="div", attrs={"class": "personList"})
        if tags:
            userinfo['username'] = tags[1].contents[2].string
            userinfo['useremail'] = tags[2].contents[2].string
            userinfo['usergroup'] = tags[4].contents[2].string
            userinfo['userApikey'] = tags[8].contents[2].span.string
        else:
            logger.warning("登录失败，检查cookies")
            userinfo['usergroup'] = "未登录用户"
            userinfo['username'] = "未登录用户"
            userinfo['useremail'] = "未登录用户"
            userinfo['userApikey'] = "未登录用户"
        printfUserinfo(userinfo['username'], userinfo['useremail'], userinfo['usergroup'], userinfo['userApikey'])
        if userinfo['usergroup'] == "未登录用户":
            self.driver.close()
            exit()
        return userinfo

    def getNumCode(self, soup):
        """
        获得 IP总数
        :param soup:
        :return:
        """
        # 找到数据所在的盒子
        NumCode = {}
        tag = soup.find(name="p", attrs={"class": "nav-font-size"})
        Num = tag.find_all(name="span")[1].span.string
        if Num is None:
            Num = 0
        else:
            Num = int(str(Num).replace(',', ''))
        NumCode['Num'] = Num
        NumCode['Code'] = self.code
        return NumCode

    def getInit(self, userinfo):
        """
        初始化 获得总 Num 和 请求连接
        :param userinfo:
        :return:
        """
        data = []
        requrl = self.url + f"/result?qbase64={Global.enBase64code(self.code)}"
        soup = self.getDriverSoup(requrl, False)
        NumCode = self.getNumCode(soup)
        if NumCode['Num'] == 0:
            logger.error('没有任何数据')
            exit()
        cityUrls = getCityurls(soup)
        data.append(userinfo)
        data.append(NumCode)
        data.append(cityUrls)
        return data

    def getRequestSoup(self, requrl, key, key1):
        """
        得到requsets得到的源码，静态资源
        :param key: 国家
        :param key1: 城市
        :param requrl: 请求url
        :return: soup的对象
        """
        i = 0
        while 1:
            logger.info(f"User requesets response url start : {key}-{key1}")
            try:
                html = requests.get(url=requrl, headers=self.headers,
                                    cookies=self.cookies)
            except Exception as e:
                logger.warning(e)
                continue
            if 'Retry later' in html.text:
                logger.warning("忙碌")
                time.sleep(35)
                continue
            if html.status_code != 200:
                return False
            # logger.info(f"User requesets response url ends : {key}-{key1}")
            # logger.info(html.status_code)
            return BeautifulSoup(html.content, "html.parser")

    def getnumpage(self, soup):
        tag = soup.find(name="p", attrs={"class": "nav-font-size"})
        num = tag.find_all(name="span")[0].string
        self.num = int(str(num).replace(',', ''))
        if self.num == 0:
            return False
        if 0 < self.num <= 10:
            self.page = 1
        if self.num >= 10:
            self.page = int(self.num / 10)
        if (self.usergroup == "注册用户") & (self.page > 5):
            self.page = 5
        if self.page > 15:
            self.page = 15
        return True

    def driverclode(self):
        self.driver.close()

    def getcookies(self, ):
        try:
            cookies = self.conn.get('fofa', 'cookies')
            if not cookies:
                raise
            cookies = cookies.split('; ')
            cookies_dict = {}
            for c in cookies:
                cookies_dict[c.split('=')[0]] = c.split('=')[-1]
            return cookies_dict
        except:
            logger.error('去到配置文件把cookies加上傻逼')
            exit()

    def run(self):
        """
        入口函数
        :return:
        """
        # 得到个人信息
        userinfo = self.getUserinfo()
        self.usergroup = userinfo['usergroup']
        if self.usergroup != "未登录用户":
            self.username = userinfo['username']
            self.useremail = userinfo['useremail']
            self.userApikey = userinfo['userApikey']
        # 查询初始化 得到 num、page 以及 code 所对应的连接
        data = self.getInit(userinfo)
        jsonData = json.dumps(data, indent=4, ensure_ascii=False)
        with open(Global.SAVEINFO_PATH, 'w', encoding='utf-8')as f:
            f.write(jsonData)
        self.driverclode()
        self.Num = data[1]['Num']
        self.href = data[2]
        if self.Num <= 50:
            asyncio.get_event_loop().run_until_complete(
                asyncreqone(requrl=self.url, page=self.page, reqcode=self.code,
                            cookies=self.cookies,
                            headers=self.headers, filename=self.filename))
        else:
            for key, value in self.href.items():
                for key1, value1 in value.items():
                    # print(f'requrl={self.url+value1}')
                    tempcode = Global.deBase64code(value1[16:])
                    # print(tempcode)
                    requrl = self.url + value1
                    # logger.info(requrl)
                    soup = self.getRequestSoup(requrl=requrl, key=key, key1=key1)
                    if not soup:
                        continue
                    if not self.getnumpage(soup=soup):
                        continue
                    # name = key + ' - ' + key1
                    asyncio.get_event_loop().run_until_complete(
                        asyncreqthree(requrl=requrl, page=self.page,
                                      cookies=self.cookies,
                                      headers=self.headers, filename=self.filename))
