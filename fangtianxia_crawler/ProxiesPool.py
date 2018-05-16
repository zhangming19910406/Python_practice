#!usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import re
import csv
import os

class ProxiesPool(object):
    def __init__(self):
        self.name = 'zhangming'

    def __call__(self):
        proxy = self.get_proxy()
        return proxy

    def get_proxy(self):
        proxy_bytes = requests.get("http://127.0.0.1:5010/get/").content
        proxy = str(proxy_bytes, encoding='utf-8')
        return proxy.split(' ')

    def get_all_proxies(self):
        proxies_bytes = requests.get('http://127.0.0.1:5010/get_all/').content
        proxies = str(proxies_bytes, encoding='utf-8')
        proxies_list = re.findall('(\d+\.\d+\.\d+\.\d+:\d+)', proxies) # 匹配出所有IP
        return proxies_list

    def delete_proxy(self, proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def check_out_proxies(self, url=None):
        # checking out prroxy had been written in Library，so it's NOT necessary.(by zhangming)
        ids =  self.get_all_proxies()
        proxies = []
        if url:
            for proxy_ip in ids:
                proxy_to_pass = {'http': "http://{}".format(proxy_ip)}
                try:
                    requests.get(url, proxies=proxy_to_pass , timeout=3)
                    print('proxy ' + proxy_ip + ' is OK')
                    proxies.extand(proxy_ip)
                except:
                    print('proxy ' + proxy_ip + ' is ERROR')
                    self.delete_proxy(proxy_ip)
        else:
            proxies = ids
        return proxies


if __name__ == '__main__':
    random_proxy = ProxiesPool()
    proxy = random_proxy.get_proxy()
    print(type(proxy))
    print(proxy)

    # file_name = os.path.join('/Users/zhangming/ENV/fang_crawler/data_csv/', 'proxies.csv')
    # r = csv.writer(open(file_name, 'w'))
    # to_write_links = [(proxy, ) for proxy in proxies]
    # r.writerows(to_write_links)
    # print(len(ids))
