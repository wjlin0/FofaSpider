## FofaApi

FofaApi2.x 是基于Python3.x ，采用 异步协程，selenium无头浏览器，requests 等多项技术开发而成的爬虫脚本。提取关键信息

FofaApi3.x 是基于Python3.x ，采用 多线程，selenium无头浏览器，requests 等多项技术开发而成的爬虫脚本。提取关键信息



## 安装

```
git clone -b v3.0.4 https://github.com/wjlin0/Fofaapi.git
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt 
```

## 使用

目前版本支持 fofa的api 和 Fofa本身平台的爬取



**1**.使用fofa的api 则需要到`./config/config.ini` 中配置 `fofa_email , fofa_key`，例如

```
fofa_email = your_email
fofa_key = your_key
```

2.使用爬取平台，则需要配置 cookies参数，从fofa登录后的cookies值全部粘贴进去，以字符串的信息粘贴 例如：

```
cookies = test=123;test2=123;test3=12312;
```



3.上述两项配置需要使用的平台即可，在使用，如需帮助 ，则可使用命令

```
python api.py --help 
```



例如收集 所以3306开放的主机



```
python api.py fofaapp -c port=\"3306\"
```

注意 fofa语句中 `"" ''`等字符  最好加上 \ 转义符



![image-20220317000114584](https://cdn.wjlin0.com/img/202203170037091.png)



## 注意

page 默认不超过30（每个城市） 若需更改 在 `./config/config.ini` 中进行更改

maxWorkers 线程个数默认3个 若机型较差可降低线程个数，防止崩溃

对于注册会员，每天的请求次数不得超过2000次 这是fofa规定的。



电脑中 要有 chrome浏览器

## 更新
> v3.0.4 - 更换输出样式 增添loging包
