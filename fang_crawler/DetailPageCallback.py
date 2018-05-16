#!usr/bin/env python3
# -*- coding: utf-8 -*-

import csv, codecs
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
from Downloader import Downloader
import os
import re

class DetailPageCallback():
    # 将详情页重要信息写入CSV文件的回调函数
    def __init__(self, path=None):
        if path:
            file_name = os.path.join(path, 'detail_pages.csv')
        else:
            file_name = 'detail_pages.csv'
        self.writer = csv.writer(codecs.open(file_name, 'w', 'utf_8_sig'))
        self.fields = (['url', '标题', '价格（万）', '户型', '面积（平）', '单价（元/平）', '房向', '楼层', '装修', '小区', '区域', '物业费（元/平米）', '建造年份', '绿化率', '容积率'])
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        # if re.search('/chushou/', url):
        soup = BeautifulSoup(html, 'html.parser')
        # This is items we need
        # data = {
        #     'url': url,
        #     'title': soup.select('#lpname > div')[0].text.strip(),
        #     'price': soup.select('div.trl-item.sty1')[0].text.strip(),
        #     'house_type': soup.select('div.tt')[0].text.strip(),
        #     'area': soup.select('div.tt')[1].text.strip(),
        #     'unit_price': soup.select('div.tt')[2].text.strip(),
        #     'house_direction': soup.select('div.tt')[3].text.strip(),
        #     'which_floor': soup.select('div.tt')[4].text.strip(),
        #     'decoration': soup.select('div.tt')[5].text.strip(),
        #     'which_housing_estate': soup.select('#agantesfxq_C03_05')[0].text.strip(),
        #     'address': list(soup.select('#address')[0].stripped_strings),
        #     # 'school': soup.select('#agantesfxq_C03_09')[0].text.strip(),
        #     # 'when_build': soup.select('div.cont.clearfix.qu_bianqu1 > div:nth-of-type(1) > span.rcont')[0].text.strip(), # it has problem, some pages don't have the itmes.
        #     'realty_service_fees': soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(2) > span.rcont')[0].text.strip(), # 物业费
        #     'when_build': soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(4) > span.rcont')[0].text.strip(),
        #     'greening_rate': soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(5) > span.rcont')[0].text.strip(),
        #     'Plot_ratio_of_the_residential_district': soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(6) > span.rcont')[0].text.strip(),
        #     # 'geoinfo' : soup.select('iframe#iframeBaiduMap')[0].get('data-src'),
        #     # 'long_temp' : re.findall(r'\"Baidu_coord_x\"=\"(\d+.\d+)\"', geoinfo)
        #     '''
        #     #c_iframe
        #     geoinfo = soup.select('#c_iframe')[0].find_next("script")
        #     geoinfo = soup.select('body:nth-of-type(2) > script:nth-of-type(3)')
        #     long_temp = re.findall(r'\"Baidu_coord_x\"=\"(\d+.\d+)\"', geoinfo)
        #     body > script:nth-child(3)
        #     body
        #     '''
        # }
        # self.client = MongoClient() if client is None else client
        data = [
            url,
            soup.select('#lpname > div')[0].text.strip(), # 标题
            soup.select('div.trl-item.sty1')[0].text.strip()[:-1], # 价格（万）
            soup.select('div.tt')[0].text.strip(), # 户型
            soup.select('div.tt')[1].text.strip()[:-2], # 面积（平）
            soup.select('div.tt')[2].text.strip()[:-4], # 单价（元/平米）
            soup.select('div.tt')[3].text.strip(), # 朝向
            soup.select('div.tt')[4].text.strip(), # 楼层
            soup.select('div.tt')[5].text.strip(), # 装修
            soup.select('#agantesfxq_C03_05')[0].text.strip(), # 小区
            list(soup.select('#address')[0].stripped_strings)[0], # 区域
            # soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(2) > span.rcont')[0].text.strip()[:-6], # 物业费
            # soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(4) > span.rcont')[0].text.strip(),
            # soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(5) > span.rcont')[0].text.strip(),
            # soup.select('div.cont > div:nth-of-type(2) > div:nth-of-type(6) > span.rcont')[0].text.strip(),
        ]

        self.writer.writerow(data)

if __name__ == '__main__':
    D = Downloader()
    url = 'http://esf.nb.fang.com/chushou/3_303467750.htm'
    html = D(url)
    # print(html)
    Callback = DetailPageCallback('/Users/zhangming/Desktop/')
    Callback(url, html)
