#coding=utf8
# _*_ coding:utf-8 _*_
"""
    @Author: lazyliang
    @Filename: lianjia_spider.py
    @Date: 2019-07-28
    @Description:
        # usage: 爬取链家网租房数据
        # platform: macOS + python3
"""

# 导入关联库
import requests
from bs4 import BeautifulSoup
import xlwings as xw
import time

# 创建Excel文件，并命名标题行
wb = xw.Book()
sht = wb.sheets.active
sht.range('A1').value = '房源名称'
sht.range('B1').value = '标签'
sht.range('C1').value = '区域'
sht.range('D1').value = '价格'
sht.range('E1').value = '类型'
sht.range('F1').value = '经纪人'
sht.range('G1').value = '编号'

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/xxxxxxxxx Safari/537.36'}
# 构造爬取网页链接的函数
def get_html(url,pages):
    res = requests.get(url,headers = header)
    bsobj = BeautifulSoup(res.text,'lxml')
    urls = bsobj.select(' a.content__list--item--aside')
    location = 2
    for url in urls:
        url = 'https://wh.lianjia.com'+url.get('href')
        get_info(url,location,page = pages)
        location += 1

# 构造爬取详细网页网页信息的函数
def get_info(url,location,page):
    res = requests.get(url,headers = header)
    bsobj = BeautifulSoup(res.text,'lxml')
    title1 = bsobj.find('p',{'class':'content__title'})
    if title1 is None:
        return
    title = title1.get_text()
    price = bsobj.find('p',{'class':'content__aside--title'}).get_text()
    house_type = bsobj.find_all('ul',{'class','content__aside__list'})[0].get_text()
    distrinct = bsobj.find('div',{'class':'content__article__info4'}).get_text()
    houseTag = bsobj.find('p',{'class':'content__aside--tags'}).get_text()

    broker = bsobj.find('div', {'class': 'content__aside__list--title oneline'}).contents[1].attrs.get('title')
    houseCode = bsobj.find('p', {'class': 'content__aside__list--bottom oneline phone'}).attrs.get('data-housecode')
# 存储数据到Excel中
    sht.range('A'+str(page*30+location)).value = title
    sht.range('B'+str(page*30+location)).value = houseTag
    sht.range('C'+str(page*30+location)).value = distrinct
    sht.range('D'+str(page*30+location)).value = price
    sht.range('E'+str(page*30+location)).value = house_type
    sht.range('F'+str(page*30+location)).value = broker
    sht.range('G'+str(page*30+location)).value = houseCode

# 运行程序
if __name__ == '__main__':
    urls = ['https://wh.lianjia.com/zufang/hanyang/pg{}'.format(ii) for ii in range(1,101)]
    for ii,url in enumerate(urls):
        print(url)
        get_html(url,ii)
        time.sleep(5)
    wb.save('./lianjia_zufang1.xlsx')
    wb.close()