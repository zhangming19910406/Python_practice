# !usr/bin/env python3
# -*- coding: utf-8 -*-

'''to get detail page's urls
   totally is 130 thousand
'''

from thread_crawler import link_crawler
from datetime import timedelta
from ScrapeCallback import ScrapeClassbackIhdexPage, ScrapeClassbackStreetPage
from DiskCache import MongoCache
import csv
from ProxiesPool import ProxiesPool
# from urllib.parse import urljoin

# old urls, beacause the new urls contain arguements that can load 100 div in a page.

file_name = '/Users/zhangming/ENV/fang_crawler/data_csv/street_seed_urls.csv'
urls = []
with open(file_name) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader) # 从第二行开始读取，将头换到第二行
    for row in reader:
        urls.extend(row)

headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Connection':'keep-alive'
}
proxies = ProxiesPool()
cache = MongoCache(expires=timedelta())
cache.clear()
write_csv = ScrapeClassbackIhdexPage(path='/Users/zhangming/ENV/fang_crawler/data_csv')
# 将目录页中的每个详情页的地址返回
for url in urls:
    link_crawler(url, headers=headers, proxies=proxies, cache=None, scrape_callback=write_csv)
# saved in data_csv/index_urls.csv
