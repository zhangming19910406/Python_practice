from datetime import timedelta
from zipfile import ZipFile
import pandas as pd
import sys
sys.path.append('../')
from crawler import link_crawler
from DiskCache import MongoCache


class AlexaCallback(object):
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_path = '/Users/zhangming/ENV/fang_crawler/thread_crawler/top-1m.csv.zip'

    def __call__(self, url, html):
        if url == 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip':
            urls = []
            zf = ZipFile(self.seed_path)
            file_name = zf.namelist()[0]
            df = pd.read_csv(zf.open(file_name))
            urls = []
            for website in df.iloc[:, 1].tolist():  # top 1 millon url's will be stored in this list:df.iloc[:, 1].tolist()
                urls.append('http://' + website)
                if len(urls) == self.max_urls:
                    break
            return urls
if __name__ == '__main__':
    cache = MongoCache(expires=timedelta())
    url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'
    # the url can't be downloaded, so be we use requests package in Downloader.py
    # so it run incorrectly.
    link_crawler(url, link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, proxies=None, num_retries=1, scrape_callback=AlexaCallback(url), cache=cache)
