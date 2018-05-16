#!usr/bin/env python3
# -*- coding: utf-8 -*-

from zipfile import ZipFile
import pandas as pd
# import class from parent folde
import sys
sys.path.append('../')
# D = Downloader()

zipped_data = '/Users/zhangming/ENV/fang_crawler/thread_crawler/top-1m.csv.zip'
zf = ZipFile(zipped_data)
file_name = zf.namelist()[0]
df = pd.read_csv(zf.open(file_name))
urls = []
for website in df.iloc[:, 1].tolist():  # top 1 millon url's will be stored in this list
    urls.append('http://' + website)
print(urls[1:20])
