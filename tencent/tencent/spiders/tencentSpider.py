# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from pyquery import PyQuery as pq

from tencent.items import TencentItem
from utils.crawler_utils import format_url
import sys

sys.path.append("..")


class tencentspiderSpider(scrapy.Spider):
    name = 'tencentSpider'
    allowed_domains = ['news.qq.com', "new.qq.com"]
    start_urls = ['http://news.qq.com/world_index.shtml']

    def parse(self, response):
        # 解析列表页中所有文章的url，并交给scrapy下载后进行解析
        doc = pq(response.body)
        url_list = []

        url_list.append((doc("#subHot a div").text(), format_url(doc("#subHot a").attr.href)))
        for ele in doc(".Q-tpWrap div em a"):
            url_list.append((ele.text, format_url(ele.attrib['href'])))
        for ele in doc(".Q-pList div em a"):
            url_list.append((ele.text, format_url(ele.attrib['href'])))

        for url in url_list:
            # print(url[0] + ":" + url[1])
            x = response.urljoin(url[1])
            yield Request(url=x, callback=self.parse_detail)

        # 提取需要下载标签也交给scrapy下载

    def parse_detail(self, response):

        article_item = TencentItem()
        html = response.body.decode("gbk")
        doc = pq(html)
        title = doc("h1").text()
        url = response.url
        content = doc("p").text()
        print(url + ":" + title + ":" + content)
