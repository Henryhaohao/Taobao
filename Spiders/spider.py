# !/user/bin/env python
# -*- coding:utf-8 -*- 
# time: 2018/2/30--16:59
__author__ = 'Henry'

'''
内容:利用selenium爬取淘宝商品信息
'''

import re, pymongo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq  # pyquery模块:解析网页(数据在页面源码的js中) (基于CSS选择器)
from Spiders.config import *  # 引入数据库配置文件

# 连接数据库
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# 方法1.启动selenium运行程序 (跳出浏览器)
# web = webdriver.Firefox()

# 方法2.启动Phantomjs运行程序 (后台运行,不会启动浏览器)
web = webdriver.PhantomJS(service_args=SERVICE_ARGS)

# 设置Phantomjs窗口大小(默认太小)
web.set_window_size(1400, 900)

# 设置webdriver访问等待最大时间,超过即重新访问
wait = WebDriverWait(web, 10)


def search():
    '''搜索商品'''
    print('开始搜索...')
    try:
        web.get('http://www.taobao.com/')
        # 输入框
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
        # 点击搜索
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)  # 搜索的关键字在config文件中的KEYWORD
        submit.click()
        # 获取总页数
        total_page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        total = int(re.compile('(\d+)').search(total_page.text).group(1))
        # 第一页中获取商品信息
        get_info()
        return total
    # 若响应时间过长,重新访问页面
    except TimeoutError:
        return search()


def next_page(page):
    '''翻页'''
    print('当前正在爬取页数:' + str(page))
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        input.clear()
        input.send_keys(str(page))
        submit = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        submit.click()
        # 验证是否翻页正确(如果是,当前页会高亮显示)
        wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), page))
        # 获取第一页之后的信息
        get_info()
    except TimeoutError:
        next_page(page)


def get_info():
    '''获取商品信息'''
    # 商品信息是否加载成功
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    # 获取网页源代码
    html = web.page_source
    # 利用pyquery库解析网页
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    try:
        for i in items:
            info = {
                'name': i.find('.title').text(),  # 名称
                'url': 'http:' + i.find('.title a').attr('href'),  # 详情页
                'image': 'http:' + i.find('.pic img').attr('data-src'),  # 预览图片
                'price': i.find('.price').text()[1:],  # 价格
                'sale': i.find('.deal-cnt').text()[:-3],  # 成交量
                'shop': i.find('.shop').text(),  # 店铺名
                'location': i.find('.location').text(),  # 所属地
            }
            print(info)
            save_to_mongodb(info)
    except:
        print('出错了!')
        pass


def save_to_mongodb(result):
    '''保存入库'''
    try:
        db[MONGO_TABLE].insert(result)
    except:
        print('存储错误!')


def main():
    '''总执行函数'''
    total = search()
    for i in range(2, total + 1):
        next_page(str(i))

    web.close()


if __name__ == '__main__':
    main()
