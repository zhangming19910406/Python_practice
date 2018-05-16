#! usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pymongo import MongoClient, errors


class MongoQueue(object):
    # possible states of a Downloader
    OUTSTANDING, PROCESSING, COMPLETE = range(3)

    def __init__(self, client=None, timeout=300):
        self.client = MongoClient() if client is None else client
        # create database cache, it can have many collections
        self.db = self.client.cache
        self.timeout = timeout

    def __nonzero__(self):
        '''Return True if there are more jobs to process
        '''
        record = self.db.crawl_queue.find_one(
            {'status': {'$ne': self.COMPLETE}}
        )
        return True if record else False

    def push(self, urls):
        '''Add new URLS to queue if does not exist
        '''
        for url in urls:
            try:
                self.db.crawl_queue.insert({'_id': url, 'status': self.OUTSTANDING})
            except errors.DuplicateKeyError as e:
                pass  # this is already in the queue

    def pop(self):
        '''Get an outstanding URL from the queue and set its
            status to processing.If the queues is empty a KeyError
            excetion is raised
        '''
        record = self.db.crawl_queue.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={'$set': {'status': self.PROCESSING, 'timestamp': datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError()

    def peek(self):
        record = self.db.crawl_queue.find_one({'status': self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self, url):
        self.db.crawl_queue.update(
            {'_id': url},
            {'$set': {'status': self.COMPLETE}}
        )

    def repair(self):
        '''Release stalled jobs
        '''
        record = self.db.crawl_queue.find_and_modify(
            query={
                'timestamp': {
                    '$lt': datetime.now() - timedelta(seconds=self.timeout)
                },
                'status': {'$ne': self.COMPLETE}
            },
            update={'$set': {'status': self.OUTSTANDING}}
        )
        if record:
            print('Releaeed:', record['_id'])

    def clear(self):
        self.db.crawl_queue.drop()
