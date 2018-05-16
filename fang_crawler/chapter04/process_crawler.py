#! usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import threading
import sys
from urllib.parse import urlparse, urljoin, urldefrag
from MongoQueue import MongoQueue
import multiprocessing
sys.path.append('../')
from Downloader import Downloader
SLEEP_TIME = 1


def threaded_crawler(seed_url, delay=5, cache=None, scrape_callback=None, proxies=None, num_retries=1, max_threads=10):
    """Crawl this website in multiple threads
        seed_url must be list
    """
    crawl_queue = MongoQueue(timeout=30)
    crawl_queue.clear()
    crawl_queue.push(seed_url)
    D = Downloader(
        cache=cache,
        delay=delay,
        proxies=proxies,
        num_retries=num_retries
    )

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
                # print(url)
            except KeyError:
                # crawl queue is empty
                break
            else:
                html = D(url)
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                        crawl_queue.complete(url)
                    except Exception as e:
                        print('Error in callback for: {}: {}'.format(url, e))

    # wait for all download threads to finish
    threads = []
    while threads or crawl_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)  # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            threads.append(thread)
        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(SLEEP_TIME)


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urldefrag(link)  # remove hash to avoid duplicates
    return urljoin(seed_url, link)


def process_link_crawler(args, **kwargs):
    num_cpus = multiprocessing.cpu_count()
    print('Starting {} processes'.format(num_cpus))
    processes = []
    for i in range(num_cpus):
        p = multiprocessing.Process(target=threaded_crawler, args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)
    # wait for processes to complete
    for p in processes:
        p.join()
