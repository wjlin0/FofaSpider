## **更新**
GUI出来大家快去看啊
[https://github.com/wjlin0/FofaSpider_GUI](https://github.com/wjlin0/FofaSpider_GUI)
## **FofaApi**


FofaApi3.x 是基于Python3.x ，采用 多线程，selenium无头浏览器，requests 等多项技术开发而成的爬虫脚本。提取关键信息
## **安装**
```bash
git clone -b v3.0.6 https://github.com/wjlin0/Fofaapi.git
cd Fofaapi && main.exe --version # output: main, version v4.0.1
```
## **使用**

#### 1. 指定cookies
```text
将fofa中的cookie字段提取出来放入config/config.yaml 或 指定 --cookies 中
```
#### 2. 指定输出样式
```text
指定输出样式 支持 json、txt、csv 导出格式 其中 csv 导出格式 excel 打开时会有乱码现象（为正常）</br> 
默认为txt 导出格式 导出位置 为 output/url.txt 且会覆盖上次搜索结果
或三者都选择 则，csv优先级最高 其次是json 最后为txt
```
#### 3.指定搜索语句
最终的执行命令可能为
```bash
main.exe -c 'domain="baidu.com"' 
```
## 配置文件

>若你嫌每次都需要配置cookies 等其他参数麻烦 则可 指定配置文件 --config</br>
>若指定--config 也会麻烦则可将配置全部添加至config/config.yaml 文件中</br>
>下列为配置实例 参数详情可 使用命令 main.exe --help 查看

> 导出csv格式的配置实例
```text
fofaSpider:
  size: 20 #
  page: 30 
  flag: 
  worker: 2
  timeout: 1.2 # 暂时无用
  output: 
  cookies:
  code:
  csv: "output/url.csv"
  json:
  config:
```
> 导出json格式的实例
```text
fofaSpider:
  size: 20 #
  page: 30 
  flag: 
  worker: 2
  timeout: 1.2 # 暂时无用
  output: 
  cookies:
  code:
  csv: 
  json: "output/url.json"
  config:
```
## 配置文件与参数的优先级
```text
假设 运行参数中制定了code 配置文件中也存在code 那么 会根据参数指定的code 进行覆盖
```
## 运行截图

![img.png](https://cdn.wjlin0.com/img/202206291029382.png)

## 功能

**1.支持csv导出**

**2.支持json格式导出**

**3.支持调整每个城市爬取的最大页数**

**4.fofa原生查询语句**



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
    1. 解决fofa更新个人主页apikey的位置导致程序无法正常启动 (v3.0.6 之前的版本都无法正常运行)
    2. 配置文件 更新结构 
    3. 新增配置文件 默认配置
    4. 配置文件新增
        fofaapp 新增
         - size  每页的大小 - 默认 20
         - page 每个城市爬取的页数 - 默认 30页
         - flag 每个城市是否爬取完 - 默认 不完全爬取 即 默认爬取最大page页
        fofaapi 新增
         - page 每页的多少 默认 100
         - size 第几页 默认 第1页
  v4.0.1 - 2022-06-29
    1.移除fofaapi
    2.升级配置文件 可定制化配置
    3.修改底层代码，使得更加优化
```



