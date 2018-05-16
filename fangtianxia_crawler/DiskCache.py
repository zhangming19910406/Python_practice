#!usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from pymongo import MongoClient
try:
    import cPickle as pickle
except ImportError:
    import pickle
from bson.binary import Binary
import zlib


class MongoCache(object):
    def __init__(self, client=None, expires=timedelta(days=30)):
        # if a client object is not passed then try
        # conneting to mongodb at the default localhost port
        self.client = MongoClient('localhost', 27017) if client is None else client
        # create collection to store cached webpages,
        # which is the equivalent of a table
        # in a relational database
        self.db = self.client.cache  # create index to expire cached webpages
        self.db.webpage.create_index('tiemstamp', expireafterSeconds=expires.total_seconds())

    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, url):
        '''Load value at this URL
        '''
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        '''Save value for this URL
        '''
        record = {
            'result': Binary(zlib.compress(pickle.dumps(result))),
            'timestamp': datetime.utcnow()
            }
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)

    def clear(self):
        self.db.webpage.drop()

if __name__ == '__main__':
    cache = MongoCache(expires=timedelta())
    url = 'www.baidu.com'
    result = {'html': '...'}
    cache[url] = result
    print(cache[url])
