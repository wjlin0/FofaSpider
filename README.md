## FofaApi

FofaApi 2.x 是基于Python3.x ，采用 异步协程，selenium无头浏览器，requests 等多项技术开发而成的爬虫脚本。提取关键信息



## 安装

```
git clone https://github.com/wjlin0/Fofaapi.git
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



配置好上述两项之后，在使用，如需帮助 ，则可使用命令

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

对高级会员有所限制，因为高级会员查询不搜限制，最好使用api查询，为了使协程的任务尽量少，对单次请求的page进行了限制为15，以防止程序出错，若为注册会员，则无需关心。

对于注册会员，每天的请求次数不得超过2000次 这是fofa规定的。

。。。协程太快还是用线程吧3.x  fofa 有限制很烦


电脑中 要有 chrome浏览器

