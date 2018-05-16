#!usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urlparse
from datetime import datetime
import time


class Throttle(object):
    """Throttle downloading by sleeping between requests to same domain
    """
    def __init__(self, delay):
        # amount of delay between downloads for each domain
        self.delay = delay
        # timestamp of when a domain was last accessed
        self.domains = {}

    def wait(self, url):
        # network location part.
        # main url
        netloc = urlparse(url).netloc
        # if don't have the value of the key, it will return none.
        # so we use get.
        last_accessed = self.domains.get(netloc)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
                # print('sleep '+str(sleep_secs))
        self.domains[netloc] = datetime.now()
