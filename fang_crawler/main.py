#!usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
from crawler import link_crawler
from ProxiesPool import ProxiesPool

def read_all_links():
    file_name = '/Users/zhangming/ENV/fang_crawler/data_csv/index_urls.csv'
    urls = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) # 从第二行开始读取，将头换到第二行
        for row in reader:
            urls.extend(row)
    return urls

# proxies
random_proxy = ProxiesPool()
cache = MongoCache(expires=timedelta())
urls = read_all_links()
headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Connection':'keep-alive'
}
for url in urls:
    proxies = random_proxy.get_all_proxies()
    link_crawler(url, delay=0, headers=None, proxies=proxies, max_urls=2, cache=cache, scrape_callback=None)
