# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from pyquery import PyQuery as pq
from tencent.items import TencentItem
from tencent.utils.common import format_url, get_md5, get_now_time
import logging


class TencentSpiderSpider(scrapy.Spider):
    """
    腾讯新闻爬虫主要逻辑
    """
    name = 'tencentSpider'
    allowed_domains = ['news.qq.com', "new.qq.com", "society.qq.com"]
    start_urls = ['http://news.qq.com/world_index.shtml']

    def parse(self, response):
        """
        1. 解析列表页中所有文章的url，并交给scrapy下载后进行解析
        2. 提取其他需要下载的标签交给scrapy下载
        :param response: 爬取返回信息
        :return: 待爬取内容页面，待爬取URL页面
        """

        # 解析列表页中所有文章的url，并交给scrapy下载后进行解析
        doc = pq(response.body)
        url_list = []

        url_list.append((doc("#subHot a div").text(), format_url(doc("#subHot a").attr.href)))
        for ele in doc(".Q-tpWrap div em a"):
            url_list.append((ele.text, format_url(ele.attrib['href'])))
        for ele in doc(".Q-pList div em a"):
            url_list.append((ele.text, format_url(ele.attrib['href'])))

        for url in url_list:
            logging.log(logging.INFO, url[0] + ":" + url[1])
            yield Request(url=response.urljoin(url[1]), callback=self.parse_detail)

        # 提取其他需要下载的标签交给scrapy下载
        # other_url = []
        # other_url.append(doc("#navlinkSociety").attr("href"))
        # for u in other_url:
        #     yield Request(url=u, callback=self.parse)

    def parse_detail(self, response):
        """
        处理需要爬取页面的

        :param response: 内容页面返回信息
        :return: 待持久化item
        """
        tencent_item = TencentItem()
        doc = pq(response.body.decode("gbk"))

        title = doc("h1").text()
        create_date = get_now_time()
        url = response.url
        url_object_id = get_md5(url)
        content = ""
        if len(doc("p").text()) > 0:
            content = doc("p").text()

        tencent_item["title"] = title
        tencent_item["create_date"] = create_date
        tencent_item["url"] = url
        tencent_item["url_object_id"] = url_object_id
        tencent_item['content'] = content
        if (len(title) > 0) & (len(content) > 0):
            return tencent_item
        else:
            logging.log(logging.ERROR, url)
            return None
