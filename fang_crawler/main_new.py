#!usr/bin/env python3
# -*- coding: utf-8 -*-

from ProxiesPool import ProxiesPool
import csv
import sys
sys.path.append('./chapter04/')
from MongoQueue import MongoQueue
from DiskCache import MongoCache
from datetime import timedelta
from process_crawler import threaded_crawler
from DetailPageCallback import DetailPageCallback

def get_urls():
    file_name = '/Users/zhangming/ENV/fang_crawler/data_csv/index_urls.csv'
    urls = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) # 从第二行开始读取，将头换到第二行
        for row in reader:
            urls.extend(row)
    return urls

def main(max_threads):
    # cache = MongoCache(expires=timedelta())
    seed_url = get_urls()
    # print(seed_url)
    cache = MongoCache(expires=timedelta())
    # cache.clear()
    callback = DetailPageCallback(path='/Users/zhangming/ENV/fang_crawler/data_csv')
    threaded_crawler(
        seed_url,
        cache=None,
        scrape_callback=callback,
        proxies=ProxiesPool(),
        max_threads=max_threads
    )


if __name__ == '__main__':
    # max_threads = int(sys.argv[1])
    main(10)
