# -*- coding: utf-8 -*-
import scrapy


class SohuspiderSpider(scrapy.Spider):
    name = 'sohuSpider'
    allowed_domains = ['news.sohu.com']
    start_urls = ['http://news.sohu.com/']

    def parse(self, response):
        pass
