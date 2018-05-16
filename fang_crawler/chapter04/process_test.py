#! usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from process_crawler import process_link_crawler
from threaded_test import get_thousand_urls
sys.path.append('../')
from DiskCache import MongoCache


def main(max_threads):
    seed_url = get_thousand_urls(1000)
    process_link_crawler(
        seed_url,
        scrape_callback=None,
        cache=None,
        max_threads=max_threads
    )


if __name__ == '__main__':
    # max_threads = int(sys.argv[1])
    main(10)
