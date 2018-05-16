#!usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from zipfile import ZipFile
from alexa_cb import AlexaCallback
from threaded_crawler import threaded_crawler
import pandas as pd
import sys
sys.path.append('../')
from DiskCache import MongoCache


def get_thousand_urls(max_urls=1000):
    zipped_data = '/Users/zhangming/ENV/fang_crawler/chapter04/top-1m.csv.zip'
    zf = ZipFile(zipped_data)
    file_name = zf.namelist()[0]
    df = pd.read_csv(zf.open(file_name))
    urls = []
    for website in df.iloc[:, 1].tolist():  # top 1 millon url's will be stored in this list
        urls.append('http://' + website)
        if len(urls) == max_urls:
            break
    return urls


def main(max_threads):
    # cache = MongoCache(expires=timedelta())
    seed_url = get_thousand_urls(100)
    # print(seed_url)
    threaded_crawler(
        seed_url,
        scrape_callback=None,
        cache=None,
        max_threads=max_threads
    )


if __name__ == '__main__':
    # max_threads = int(sys.argv[1])
    main(10)
