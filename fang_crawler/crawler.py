#!usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import urllib.parse
from urllib.parse import urlparse, urljoin, urldefrag
from urllib import robotparser
import requests
import time
from datetime import datetime, timedelta
from collections import deque
from bs4 import BeautifulSoup
from Throttle import Throttle
from Downloader import Downloader
from ScrapeCallback import ScrapeClassbackIhdexPage
from DiskCache import MongoCache
# from RandomProxy import get_proxy, delete_proxy, get_all_proxies
SLEEP_TIME = 5

def link_crawler(seed_url,link_regex=None, delay=5, max_depth=-1, max_urls=-1, headers=None, proxies=None, cookies=None, num_retries=1, scrape_callback=None, cache=None):
    """Crawl from the given seed URL following links matched by link_regex
    seed_url:种子链接，爬虫的初始链接
    delay:避免请求太频繁，所采取的延时
    max_depth:从种子链接向下，所链接的深度
    max_urls:连续max_urls次下载同一个网页，得到404后，停止下载，跳出循环
    headers:请求头
    proxy:代理, 列表的形式
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
    headers = headers or {}
    D = Downloader(delay=delay, headers=headers, cookies=cookies, proxies=proxies, num_retries=num_retries, cache=cache)

    # while crawl_queue:
    #     url = crawl_queue[-1]
    #     # check url passes robots.txt restrictions
    #     html = D(url)
    #     try:
    #         num_urls[url] += 1
    #     except KeyError:
    #         num_urls[url] = 1
    #
    #     links = []
    #     if scrape_callback:
    #         links.extend(scrape_callback(url, html) or [])
    #
    #     depth = seen[url] # 标记爬取的链接以及此链接属于第几层
    #     if depth != max_depth:
    #         # can still crawl further
    #         if link_regex:
    #             links.extend(link for link in get_links(html) if re.match(link_regex, link))
    #         else:
    #             links.extend(link for link in get_links(html))
    #         for link in links:
    #             link = normalize(seed_url, link)
    #             # check whether already crawled this link
    #             if link not in seen:
    #                 seen[link] = depth + 1
    #                 # check link is within same domain
    #                 if same_domain(seed_url, link):
    #                     # success! add this new link to queue
    #                     crawl_queue.appendleft(link)
    #
    #
    #     if num_urls[url] == max_urls:
    #         break
    #
    #     # check whether have reached downloaded maximum
    while True:
        try:
            url = crawl_queue.pop()
        except IndexError:
            break
        else:
            html = D(url)
            seen[seed_url] = seen[seed_url] + 1
            links = []
            if scrape_callback:
                links.extend(scrape_callback(url, html) or [])
            next_urls = get_links(html)
            print(next_urls)
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
        time.sleep(SLEEP_TIME)



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
    tags = soup.find_all(id='PageControl1_hlk_next')
    return [tag.get('href') for tag in tags]

if __name__ == '__main__':
    # cache = MongoCache(expires=timedelta())
    # cache.clear()
    # proxies = get_all_proxies()
    # cache = MongoCache(expires=timedelta())
    link_crawler('http://esf.nb.fang.com/house-a01047-b020965/', max_urls=5, cache=None, proxies=None, delay=10)
