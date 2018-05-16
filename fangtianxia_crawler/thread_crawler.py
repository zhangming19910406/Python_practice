#!usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import urllib.parse
from urllib.parse import urlparse, urljoin, urldefrag
from urllib import robotparser
import requests
import time
import threading
from datetime import datetime, timedelta
from collections import deque
from bs4 import BeautifulSoup
from Throttle import Throttle
from Downloader import Downloader
from ScrapeCallback import ScrapeClassbackIhdexPage
from DiskCache import MongoCache


def link_crawler(seed_url,link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, proxies=None, cookies=None, num_retries=5, scrape_callback=None, cache=None, max_threads=10, timeout=60):
    """Crawl from the given seed URL following links matched by link_regex
        Crawl this website in mltiple threads
    seed_url:种子链接，爬虫的初始链接
    delay:避免请求太频繁，所采取的延时
    max_depth:从种子链接向下，所链接的深度
    max_urls:连续max_urls次下载同一个网页，得到404后，停止下载，跳出循环
    headers:请求头
    proxy:传入ProxiesPool类
    num_retries:当网页的返回识别码在400和500之间时，重复下载的数，如果还不能下载返回空字符串
    cahce:是否存在缓存，用法例如：
        cache = MongoCache(expires=timedelta())
        D = Downloader(cache=cache)
        html = D('http://esf.nb.fang.com/')
    """
    # the queue of URL's that still need to be crawled
    crawl_queue = deque([seed_url])
    # the URL's that have been seen and at what depth
    seen = {seed_url: 0}
    # track how many URL's have been downloaded
    num_urls = {seed_url: 0}
    # rp = get_robots(seed_url)
    headers = headers
    D = Downloader(delay=5, headers=headers, cookies=cookies, proxies=proxies, num_retries=num_retries, cache=cache)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                break
            else:
                download_time = 1
                while download_time <= 5:
                    html = D(url)
                    download_time = download_time + 1
                    print('we download the url %s times' % download_time)
                    links = []
                    if scrape_callback:
                        links.extend(scrape_callback(url, html) or [])
                    next_urls = get_links(html)
                    if next_urls:
                        seen[seed_url] = seen[seed_url] + 1
                        break
                if link_regex:
                    links.extend(link for link in next_urls if re.match(link_regex, link))
                else:
                    links.extend(link for link in next_urls)
                for link in links:
                    if seen[seed_url] != max_depth:
                        link = normalize(seed_url, link)
                        # check whether already crawled this link
                        if link not in seen and same_domain(seed_url, link):
                            # check link is within same domain
                            # success! add this new link to queue
                            crawl_queue.append(link)

                # check whether have reached downloaded maximum
                try:
                    num_urls[url] += 1
                except KeyError:
                    num_urls[url] = 1
                if num_urls[url] == max_urls:
                    break


    threads = []
    while threads or crawl_queue:
        # the crawl is still activate
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            # set daemon so main thread can exit when receives ctrl-c
            thread.setDaemon(True)
            thread.start()
            # thread.run()
            threads.append(thread)
        # all thread have been processed
        # sleep temporarily so CPU can focus execution on other threads


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urldefrag(link)  # remove hash to avoid duplicates
    return urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urlparse(url1).netloc == urlparse(url2).netloc


def get_links(html):
    """Return a list of links from html
    """
    soup = BeautifulSoup(html, 'html.parser')
    '''//*[@id="PageControl1_hlk_next"]
    #PageControl1_hlk_next
    '''
    tags = soup.select('#PageControl1_hlk_next')
    return [tag.get('href') for tag in tags]

if __name__ == '__main__':
    cache = MongoCache(expires=timedelta())
    callback = ScrapeClassbackIhdexPage('/Users/zhangming')
    # link_crawler('http://esf.nb.fang.com/house-a0168-b015945/', max_urls=2, cache=None, scrape_callback=None)
    link_crawler('http://esf.nb.fang.com/house-a0165/', max_urls=2, cache=None, scrape_callback=None)
