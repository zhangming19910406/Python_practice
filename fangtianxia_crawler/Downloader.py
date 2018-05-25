#!usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from Throttle import Throttle
from DiskCache import MongoCache
from datetime import timedelta
import random
from ProxiesPool import ProxiesPool


class Downloader(object):
    def __init__(self, delay=1, headers=None, cookies=None, proxies=None, num_retries=5, cache=None):
        self.throttle = Throttle(delay)
        self.headers = headers
        self.cookies = cookies
        # self.proxies = ProxiesPool()
        self.proxies = proxies
        self.num_retries = num_retries
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                # load cache
                result = self.cache[url]
                if result['code'] == 200:
                    print('Loading html from cache ' + url)
                else:
                    result = None
            except KeyError:
                pass

        if result is None:
            result = self.download(url, self.headers, self.cookies, self.proxies, self.num_retries)
            if self.cache:
                self.cache[url] = result # 字典中存放字典{'html': html, 'code': code}
        return result['html']

    def download(self, url, headers, cookies, proxies, num_retries):
        print('Downloading ' + url)
        html = ''  # 当异常发生以及服务多次响应5XX，也能返回空字符串
        code = None
        proxies_to_pass = None
        proxy_ip = proxies.get_proxy() if proxies else None # 随机获取代理ip
        if proxy_ip:
            proxies_to_pass = {'http': "http://{}".format(proxy_ip[0])}
        if num_retries > 0:
            try:
                self.throttle.wait(url)
                # print(proxies_to_pass)
                r = requests.get(url, headers=headers, cookies=cookies, proxies=proxies_to_pass, timeout=30)
                code = r.status_code
                # print(code)
                r.raise_for_status()
                if code == 200:
                    html = r.text
                    # print(html)
                elif code and 500 < code < 600:
                    # retry 5XX HTTP errors
                    return self.download(url, headers, cookies, proxies, num_retries-1)
            except requests.exceptions.HTTPError:
                print('----Download error: ' + r.reason)
                return self.download(url, headers, cookies, proxies, num_retries-1)
            except requests.exceptions.Timeout:
                print('----Download error: Timeout, we download it again with another proxy.')
                return self.download(url, headers, cookies, proxies, num_retries-1)
            except:
                print('----Unknow error:May be CANNOT connect to proxy.')
                return self.download(url, headers, cookies, proxies, num_retries-1)
        else:
            print('----Unknow error:We download to much times.')
        result = {'html': html, 'code': code}
        if self.cache:
            self.cache[url] = result
        # print(result)
        return result

if __name__ == '__main__':
    # proxy_pool = ProxiesPool()
    # proxies = proxy_pool.get_all_proxies()
    for i in range(5):
        print('this is {} times\n'.format(i))
        D = Downloader(proxies=ProxiesPool(), cache=None, delay=0)
        html = D('http://esf.nb.fang.com/')
        # print(html)
