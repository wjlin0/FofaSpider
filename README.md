## FofaApi

FofaApi2.x 是基于Python3.x ，采用 异步协程，selenium无头浏览器，requests 等多项技术开发而成的爬虫脚本。提取关键信息

FofaApi3.x 是基于Python3.x ，采用 多线程，selenium无头浏览器，requests 等多项技术开发而成的爬虫脚本。提取关键信息



## 安装

```
git clone -b v3.0.6 https://github.com/wjlin0/Fofaapi.git
cd Fofaapi && api.exe --version # output: api.exe, version v3.0.6
```

## 使用

目前版本支持 fofa的api 和 Fofa本身平台的爬取



1.使用fofa的api 则需要到`config.ini` 中配置 `fofa_email , fofa_key`，例如

```text
fofa_email = your_email
fofa_key = your_key
```

2.使用爬取平台，则需要配置 cookies参数，从fofa登录后的cookies值全部粘贴进去，以字符串的信息粘贴 例如：

```
cookies = test=123;test2=123;test3=12312;
```



3.上述两项配置需要使用的平台即可，在使用，如需帮助 ，则可使用命令

```
api.exe --help 
```



例如收集 所以3306开放的主机



```
api.exe fofaapp -c port=\"3306\"
```

注意 fofa语句中 `"" ''`等字符  最好加上 \ 转义符



![image-20220317000114584](https://cdn.wjlin0.com/img/202203170037091.png)



## 注意

page 默认不超过30（每个城市） 若需更改 在 `./config.ini` 中进行更改

maxWorkers 线程个数默认3个 若机型较差可降低线程个数，防止崩溃

对于注册会员，每天的请求次数不得超过2000次 这是fofa规定的。



## 更新
```text
  v3.0.4
    1. 更换输出样式
    2. 修复输出城市获取条数不精确
    3. 新增输出国家获取总条数
    4. 源码不开源
  v3.0.5 - 2022-05-21
    1. 解决当tag未出现href时，出现报错导致无法继续进行
    2. 解决ctrl + c 无法正常结束
    3. 更新IP收集异常
  v3.0.6 - 2022-06-18
    1. 解决fofa更新个人主页apikey的位置导致程序无法正常启动
    2. 添加 fofaapp output 参数
    3. 配置文件 更新结构 
    4. 新增配置文件 默认配置
``` 
         
