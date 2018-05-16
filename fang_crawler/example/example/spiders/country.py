# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from example.items import ExampleItem


class CountrySpider(CrawlSpider):
    name = 'country'
    start_urls = ['http://example.webscraping.com/']
    allowed_domains = ['example.webscraping.com']

    rules = (
        Rule(LinkExtractor(allow=r'/places/default/view/'), follow=True),
        Rule(
            LinkExtractor(allow=r'/places/default/index/'),
            callback='parse_item',
            follow=True,
        ),
    )

    def parse_item(self, response):
        item = ExampleItem()
        name_css = 'tr#places_country__row td.w2p_fw::text'
        pop_css = 'tr#places_population__row td.w2p_fw::text'
        item['name'] = response.css(name_css).extract()
        item['population'] = response.css(pop_css).extract()
        return item
