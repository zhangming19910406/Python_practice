#!usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag
from Downloader import Downloader
import os


class ScrapeClassbackIhdexPage():
    # 将目录页中的详情页地址写入CSV文件的回调函数
    def __init__(self, path=None):
        if path:
            file_name = os.path.join(path, 'index_urls.csv')
        else:
            file_name = 'index_urls.csv'
        self.writer = csv.writer(open(file_name, 'w'))
        self.fields = (['url'])
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        # if re.search('/chushou/', url):
        links = []
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.select('dd > p.title > a')
        links = [tag.get('href') for tag in a_tags]
        normalize_links = []
        for link in links:
            link, _ = urldefrag(link)  # remove hash to avoid duplicates
            normalize_links.extend([urljoin(url, link), ])
        to_write_links = [(link, ) for link in normalize_links]
        # (link, )这样写的目的是：字符串也是可循环变量，为了不把每个字符当作循环变量
        self.writer.writerows(to_write_links)

class ScrapeClassbackStreetPage(object):
    # 在鄞州区等区的目录下，将各街道的地址写入CSV文件
    def __init__(self, path=None):
        if path:
            file_name = os.path.join(path, 'street_seed_urls.csv')
        else:
            file_name = 'street_seed_urls.csv'
        self.writer = csv.writer(open(file_name, 'w'))
        self.fields = (['url'])
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        # if re.search('/chushou/', url):
        links = []
        soup = BeautifulSoup(html, 'html.parser')
        a_tags = soup.select('#shangQuancontain > a')
        links = [tag.get('href') for tag in a_tags[1:]]
        normalize_links = []
        for link in links:
            link, _ = urldefrag(link)  # remove hash to avoid duplicates
            normalize_links.extend([urljoin(url, link), ])
        to_write_links = [(link, ) for link in normalize_links]
        # (link, )这样写的目的是：字符串也是可循环变量，为了不把每个字符当作循环变量
        self.writer.writerows(to_write_links)





if __name__ == '__main__':
    D = Downloader()
    html = D('http://esf.nb.fang.com/house/i33/')
    Callback = ScrapeClassbackIhdexPage()
    Callback('http://esf.nb.fang.com/house/i33/', html)
    html2 = D('http://esf.nb.fang.com/house-a01047/')
    callback2 = ScrapeClassbackStreetPage()
    callback2('http://esf.nb.fang.com/house-a01047/', html2)
