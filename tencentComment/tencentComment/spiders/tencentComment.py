# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup

from tencent.utils.global_list import *
from scrapy import Request
import logging

from tencentComment.items import TencentCommentItem


class TencentcommentSpider(scrapy.Spider):
    name = 'tencentComment'
    allowed_domains = [NEWS, NEW, SOCIETY, MIL, TECH, ENT, FINANCE, SPORTS]
    start_urls = [URL_WORLD]

    def parse(self, response):
        """
        腾讯新闻评论爬虫主要逻辑
        :param response:
        :return:
        """
        url_list = ["http://new.qq.com/omn/20180511/20180511A04WBW.html",
                    "http://new.qq.com/omn/20180510/20180510A1DSGA.html",
                    "http://new.qq.com/omn/20180510/20180510A1DSGA.html"]

        for url in url_list:
            yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        处理需要爬取页面的

        :param response: 内容页面返回信息
        :return: 待持久化item
        """
        tencent_comment_item = TencentCommentItem()
        soup = BeautifulSoup(response.body.decode("utf-8"), "html.parser")
        title = soup.select("h1")[0].text
        logging.log(logging.DEBUG, title)
