#!usr/bin/env python3
# -*- coding: utf-8 -*-

'''
STEP 1
因为在目录页下，每个类目最多显示100页的信息，这样无法得到所有的房源
所以增减限定条件，让每个类目的页数少于100页
这个程序是为了获取所需要的类目的地址，遍历所有页面
存储到street_seed_urls.csv
'''

from thread_crawler import link_crawler
from ScrapeCallback import ScrapeClassbackStreetPage
from DiskCache import MongoCache
from datetime import timedelta

links = [
    'http://esf.nb.fang.com/house-a01047/',
    'http://esf.nb.fang.com/house-a0162/',
    'http://esf.nb.fang.com/house-a0166/',
    'http://esf.nb.fang.com/house-a0164/',
    'http://esf.nb.fang.com/house-a0165/',
    'http://esf.nb.fang.com/house-a0171/',
    'http://esf.nb.fang.com/house-a0169/',
    'http://esf.nb.fang.com/house-a0170/',
    'http://esf.nb.fang.com/house-a0168/',
    'http://esf.nb.fang.com/house-a0172/',
]

callback = ScrapeClassbackStreetPage(path='/Users/zhangming/ENV/fangtianxia_crawler/data_csv')
cache = MongoCache(expires=timedelta())
cache.clear()
for link in links:
    link_crawler(link, scrape_callback=callback, cache=None, max_depth=1, max_urls=1)
# saved in /data_csv/street_seed_urls.csv
