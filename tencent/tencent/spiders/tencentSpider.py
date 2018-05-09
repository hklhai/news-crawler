# -*- coding: utf-8 -*-
import scrapy


class TencentspiderSpider(scrapy.Spider):
    name = 'tencentSpider'
    allowed_domains = ['news.qq.com']
    start_urls = ['http://news.qq.com/']

    def parse(self, response):
        print("===========================Test===================")
        page = response.url
        print(page)
