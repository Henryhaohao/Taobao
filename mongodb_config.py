# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/2/30--21:19
__author__ = 'Henry'

'''
MongoDB及Phantomjs配置文件
'''

#配置MongoDB
MONGO_URL =  'localhost'
MONGO_DB = 'Henry'
MONGO_TABLE = 'taobao'

#配置Phantomjs
SERVICE_ARGS = ['--load-images=false','--disk-cache=true'] #设置不加载图片和开启缓存,加快访问速度

#搜索商品关键字
KEYWORD = '牛仔裤'
