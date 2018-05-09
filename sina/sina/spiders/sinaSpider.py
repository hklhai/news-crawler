# -*- coding: utf-8 -*-
import scrapy


class SinaspiderSpider(scrapy.Spider):
    name = 'sinaSpider'
    allowed_domains = ['news.sina.com.cn']
    start_urls = ['http://news.sina.com.cn/']

    def parse(self, response):
        pass
