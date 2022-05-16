#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   :wjlin0
# @Blog     :https://wjlin0.com
# @Email    :wjlgeren@163.com
# @Time     :2022-02-26 16:07
# @File     :FofaApp

import json
import os
import shutil
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
from loging import logs
from prettytable import PrettyTable, DEFAULT

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

import Global


def printfUserinfo(userName, userEmail, userGroup, userApikey):
    """
    打印个人信息
    :param userName: 用户名
    :param userEmail: 邮箱
    :param userGroup: 会员等级
    :param userApikey: api的key
    :return:
    """
    table = PrettyTable(['用户名', '邮箱', '组别', 'APIKEY'])
    table.add_row([userName, userEmail, userGroup, userApikey])
    table.set_style(DEFAULT)
    print(table)


def getUrlIp(soup, filename):
    """
     文件IO操作
    :param soup:
    :param filename:
    :return:
    """
    tags = soup.find_all(name="div", attrs={"class": "addrLeft"}, limit=10)
    urls = []
    ips = []
    try:
        for tag in tags:
            tag = tag.find(name="span", attrs={"class": "aSpan"})
            if tag.find(name="a", attrs={"target": "_blank"}) is None:
                ip = "ip: " + tag.string + "\n"
                if ip not in ips:
                    ips.append(ip)
            if tag.find(name="a", attrs={"target": "_blank"}):
                url = "url: " + tag.find(name="a", attrs={"target": "_blank"})['href'] + "\n"
                if url not in urls:
                    urls.append(url)
        with open(filename, "a+", encoding="utf-8")as f:
            if ips:
                f.writelines(ips)
            if urls:
                f.writelines(urls)
        return len(ips)+len(urls)
    except Exception as e:
        logs.error(e)
        return False


def getReq(url, cookies, headers, timeout):
    """
    请求 页数
    :param url:
    :param cookies:
    :param headers:
    :param timeout:
    :return:
    """
    while 1:
        try:
            time.sleep(timeout)
            html = requests.get(url=url, cookies=cookies, headers=headers)
            text = html.text
            if 'Retry later' in text:
                logs.warning("忙碌")
                time.sleep(10)
                continue
            if html.status_code != 200:
                time.sleep(timeout)
                continue
            return BeautifulSoup(text, "html.parser")
        except Exception as e:
            logs.error(e)
            return False


def futureThree(OK, maxWorkers, cookies, headers, reqUrl, page, reqCode, fileName, timeout):
    """
    多线程函数 将 请求的url整理好 放入线程队列中
    :param OK: 标志 请求
    :param maxWorkers: 线程中最大线程
    :param cookies: cookies值
    :param headers: 请求头
    :param reqUrl: 请求url
    :param page: 页数
    :param reqCode: 请求代码
    :param fileName: 保存的文件名
    :param timeout: 延时
    :return: 成功请求多少页
    """
    num = 0
    if OK:
        reqUrlList = [reqUrl + f"&page={pa + 1}&page_size=10" for pa in
                      range(int(page))]
    else:
        reqUrlList = [reqUrl + f"/result?page={pa + 1}&page_size=10&qbase64={Global.deBase64code(reqCode)}" for pa in
                      range(int(page))]
    with ThreadPoolExecutor(max_workers=maxWorkers) as pool:
        futures = [pool.submit(getReq, url, cookies, headers, timeout) for url in reqUrlList]

        for future in as_completed(futures):
            a = future.result()
            b = getUrlIp(soup=future.result(), filename=fileName)
            if not a:
                continue
            if not b:
                continue
            num = num + b
    return num


def getCityUrls(soup):
    """
    获得所有城市的url
    :param soup:
    :return:
    """
    Cityurls = {}
    countryLi = soup.find_all(name="li", attrs={"class": "countryLi"})
    for tag in countryLi:
        countryName = tag.find(name="div", attrs={"class": "titleLeft"}).a.string
        countryName = str(countryName).replace("\n", "")
        countryName = countryName.replace(" ", "")
        cityTags = tag.find_all(name="div", attrs={"class": "listCont table-label table-label-left"})
        temp = {}
        for city in cityTags:
            cityName = str(city.a.string).replace("\n", "")
            cityName = str(cityName).replace(" ", "")
            temp[cityName] = city.a['href']
        Cityurls[countryName] = temp
    return Cityurls


class FofaApp:

    def __init__(self, code):

        self.url = "https://fofa.info"
        self.filename = Global.SAVEFILENAME_PATH
        self.conn = Global.conn
        self.code = code
        self.username = ""
        self.userGroup = ""
        self.userEmail = ""
        self.userApikey = ""
        self.cookies = self.getCookies()
        self.Page = self.getInitPage()
        self.maxWorkers = self.getWorkers()
        self.timeout = self.getTimeout()
        self.fToken = dict(name='fofa_token', value=self.cookies['fofa_token'])
        self.fUser = dict(name='user', value=self.cookies['user'])
        self.freToken = dict(name='refresh_token', value=self.cookies['refresh_token'])
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
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            chrome_options = Options()
            chrome_options.add_argument('–ignore-certificate-errors')
            chrome_options.add_argument('--ignore-ssl-errors')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_options.add_argument('headless')
            driverPath = ""
            driverInstall = Global.ROOT_DIR + "/driver/"
            if not os.path.exists(driverInstall):
                os.mkdir(driverInstall)
            try:
                for fpathe, dirs, fs in os.walk(driverInstall):
                    for f in fs:
                        if 'chromedriver.exe' in os.path.join(fpathe, f):
                            driverPath = os.path.join(fpathe, f)
                            break
                driver = webdriver.Chrome(executable_path=driverPath,
                                          chrome_options=chrome_options)
            except:
                shutil.rmtree(driverInstall)  # 清空目录
                os.mkdir(driverInstall)
                driver = webdriver.Chrome(executable_path=ChromeDriverManager(path=driverInstall).install(),
                                          chrome_options=chrome_options)

            driver.get(url=self.url)
            driver.delete_all_cookies()
            driver.add_cookie(cookie_dict=self.fToken)
            driver.add_cookie(cookie_dict=self.freToken)
            driver.add_cookie(cookie_dict=self.fUser)
            driver.get(url=self.url)
            return driver
        except Exception as e:
            logs.error(f"{e}")
            sys.exit()

    def getDriverSoup(self, reqUrl, sign):
        """
        得到driver生成的源码对象（动态获得）
        :param reqUrl: 请求url
        :param sign: 标志为False，
        :return: 返回soup对象
        """
        try:
            while 1:
                self.driver.get(url=reqUrl)
                if 'Retry later' in self.driver.page_source:
                    time.sleep(10)
                    continue
                if '查询语法错误' in self.driver.page_source:
                    logs.error('查询语句出错')
                    self.driver.close()
                    self.driver.quit()
                    sys.exit()
                if not sign:
                    WebDriverWait(driver=self.driver, timeout=15).until(
                        expected_conditions.presence_of_element_located((By.CLASS_NAME, "countryTitle")))
                html = self.driver.page_source
                return BeautifulSoup(html, "html.parser")
        except:
            logs.error('别看了没有任何数据')
            self.driver.close()
            self.driver.quit()
            sys.exit()

    def getUserinfo(self):
        """
        :return: 个人信息
        """
        userinfo = {}
        requrl = self.url + '/personalData'
        soup = self.getDriverSoup(requrl, True)
        tags = soup.find_all(name="div", attrs={"class": "personList"})
        try:
            if tags:
                userinfo['username'] = tags[1].contents[2].string
                userinfo['useremail'] = tags[2].contents[2].string
                userinfo['usergroup'] = tags[4].contents[2].string
                userinfo['userApikey'] = tags[8].contents[2].span.string
            if (tags is None) or \
                    (userinfo['username'] is None) or \
                    (userinfo['useremail'] is None) or \
                    (userinfo['usergroup'] is None) or \
                    (userinfo['userApikey'] is None):
                raise
        except:
            logs.warning("登录失败，检查cookies")
            userinfo['usergroup'] = "未登录用户"
            userinfo['username'] = "未登录用户"
            userinfo['useremail'] = "未登录用户"
            userinfo['userApikey'] = "未登录用户"
        finally:
            printfUserinfo(userinfo['username'], userinfo['useremail'], userinfo['usergroup'], userinfo['userApikey'])
            if userinfo['usergroup'] == "未登录用户":
                self.driver.close()
                sys.exit()
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
            logs.error('没有任何数据')
            sys.exit()
        cityUrls = getCityUrls(soup)
        data.append(userinfo)
        data.append(NumCode)
        data.append(cityUrls)
        return data

    def getRequestSoup(self, reqUrl):
        """
        得到requsets得到的源码，静态资源
        :param reqUrl: 请求url
        :return: soup的对象
        """
        while 1:
            try:
                html = requests.get(url=reqUrl, headers=self.headers,
                                    cookies=self.cookies)
            except Exception as e:
                logs.warning(e)
                continue
            if 'Retry later' in html.text:
                logs.warning("忙碌")
                time.sleep(35)
                continue
            if html.status_code != 200:
                return False
            return BeautifulSoup(html.content, "html.parser")

    def getNumPage(self, soup):
        """
        得到本次请求的 num page
        :param soup: soup 对象
        :return: 是否获取成功
        """
        tag = soup.find(name="p", attrs={"class": "nav-font-size"})
        num = tag.find_all(name="span")[0].string
        self.num = int(str(num).replace(',', ''))
        if self.num == 0:
            return False
        if 0 < self.num <= 10:
            self.page = 1
        if self.num >= 10:
            self.page = int(self.num / 10)
        if (self.userGroup == "注册用户") & (self.page > 5):
            self.page = 5
        if self.page > self.Page:
            self.page = self.Page
        return True

    def driverClose(self):
        self.driver.close()

    def getCookies(self):
        try:
            cookies = self.conn.get('fofa', 'cookies')
            if not cookies:
                logs.error('去到配置文件把cookies加上傻逼')
                raise
            cookies = cookies.split('; ')
            cookies_dict = {}
            for c in cookies:
                cookies_dict[c.split('=')[0]] = c.split('=')[-1]
            if ('fofa_token' not in cookies_dict.keys()) \
                    or ('user' not in cookies_dict.keys()) \
                    or ('refresh_token' not in cookies_dict.keys()):
                logs.warning('检查一下cookies是不是粘贴错了')
                raise
            return cookies_dict
        except:
            sys.exit()

    def getInitPage(self):
        try:
            page = int(self.conn.get('fofa', 'page'))
            if not page:
                page = 30
            return page
        except Exception as e:
            logs.error(e)
            return 30

    def getWorkers(self):
        try:
            Max = int(self.conn.get('fofa', 'maxWorkers'))
            if not Max:
                Max = 10
            return Max
        except Exception as e:
            logs.error(e)
            return 15

    def getTimeout(self):
        try:
            timeout = float(self.conn.get('fofa', 'timeout'))
            if not timeout:
                timeout = 1
            return timeout
        except Exception as e:
            logs.error(e)
            return 1

    def run(self):
        """
        入口函数
        :return:
        """
        # 得到个人信息
        userinfo = self.getUserinfo()
        self.userGroup = userinfo['usergroup']
        if self.userGroup != "未登录用户":
            self.username = userinfo['username']
            self.userEmail = userinfo['useremail']
            self.userApikey = userinfo['userApikey']
        # 查询初始化 得到 num、page 以及 code 所对应的连接
        data = self.getInit(userinfo)
        jsonData = json.dumps(data, indent=4, ensure_ascii=False)
        with open(Global.SAVEINFO_PATH, 'w', encoding='utf-8')as f:
            f.write(jsonData)
        self.driverClose()
        self.Num = data[1]['Num']
        self.href = data[2]
        if self.Num <= 50:
            futureThree(OK=True, maxWorkers=self.maxWorkers, reqUrl=self.url, page=self.page,
                        cookies=self.cookies,
                        headers=self.headers, reqCode=self.code, fileName=self.filename, timeout=self.timeout)
        else:
            for key, value in self.href.items():
                i = 1
                j = 1
                num = 0
                for key1, value1 in value.items():
                    reqUrl = self.url + value1
                    soup = self.getRequestSoup(reqUrl=reqUrl)
                    if not soup:
                        continue
                    if not self.getNumPage(soup=soup):
                        continue
                    times = futureThree(OK=True, maxWorkers=self.maxWorkers, reqUrl=reqUrl, page=self.page,
                                        cookies=self.cookies,
                                        headers=self.headers, reqCode=self.code, fileName=self.filename,
                                        timeout=self.timeout)
                    num = num + times
                    i += 1
                    if i >= 5 * j:
                        time.sleep(5)
                        j += 1
                    logs.success(key + "-" + key1 + " 请求完成,一共获取大约" + str(times) + "条")
                logs.success(key + " 请求完成,一共获取大约" + str(num) + "条")
