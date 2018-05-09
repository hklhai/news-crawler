# -*- coding: utf-8 -*-
import scrapy


class NeteasespiderSpider(scrapy.Spider):
    name = 'netEaseSpider'
    allowed_domains = ['news.163.com']
    start_urls = ['http://news.163.com/']

    def parse(self, response):
        pass
