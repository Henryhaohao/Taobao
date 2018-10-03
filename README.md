淘宝商品信息的定向爬取 ![enter image description here](Pic/logo.png)
===========================
![](https://img.shields.io/badge/Python-3.6.3-green.svg) ![](https://img.shields.io/badge/pymongo-3.6.1-green.svg) ![](https://img.shields.io/badge/pyquery-1.4.0-green.svg) ![](https://img.shields.io/badge/selenium-3.8.1-green.svg)
### 淘宝官网 - https://www.taobao.com/ 
|Author|:sunglasses:Henryhaohao:sunglasses:|
|---|---
|Email|:hearts:1073064953@qq.com:hearts:

    
****
## :dolphin:声明
### 软件均仅用于学习交流，请勿用于任何商业用途！感谢大家！
## :dolphin:介绍
### 该项目为[淘宝网](https://www.taobao.com/)商品信息的定向爬虫
- 项目介绍:通过淘宝搜索关键字爬取指定的商品信息
- 爬取方式:通过Python的Selenium自动化测试库以及配合Phantomjs无头浏览器
- 爬虫文件:运行Spiders目录下的spider.py
- 配置文件:运行前修改Spiders目录下的config.py,其中的KEYWORD为你要搜索商品名称的关键字,以及mongodb相关配置
- 补充:如果想要增加爬取的字段,可以自行在item中添加,目前包括商品名、城市、详情链接、封面、售价、销量、店铺名
## :dolphin:运行环境
Version: Python3
## :dolphin:安装依赖库
```
pip3 install -r requirements.txt
```
## :dolphin:运行截图
> - 运行
![enter image description here](Pic/run.png)

> - 数据结构
![enter image description here](Pic/data.png)



