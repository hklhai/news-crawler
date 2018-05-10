# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from pyquery import PyQuery as pq


class TencentspiderSpider(scrapy.Spider):
    name = 'tencentSpider'
    allowed_domains = ['news.qq.com']
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
            yield Request(url=response.urljoin(url[1]), callback=self.parse_detail)

        # 提取需要下载标签也交给scrapy下载

    def parse_detail(self, response):
        from tencent.tencent.items import TencentItem
        article_item = TencentItem()
        doc = pq(response.body)
        print(doc("h1"))


def format_url(url):
    if url.startswith("//"):
        return "http:" + url
