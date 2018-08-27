# -*- coding: utf-8 -*-
import scrapy


class CnbianjuSpider(scrapy.Spider):
    name = 'cnbianju'
    allowed_domains = ['www.bianju.me']
    start_urls = ['http://www.bianju.me/']

    def parse(self, response):
        pass
