# -*- coding: utf-8 -*-
import logging

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from tencent.items import TencentItem
from tencent.utils.common import get_md5, get_now_time, remove_special_label
from tencent.utils.global_list import *


class TencentSpiderSpider(scrapy.Spider):
    """
    腾讯新闻爬虫主要逻辑
    """
    name = 'tencentSpider'
    allowed_domains = [NEWS, NEW, SOCIETY, MIL, TECH, ENT, FINANCE, SPORTS]
    start_urls = [START_URL]

    def parse(self, response):
        """
        1. 解析列表页中所有文章的url，并交给scrapy下载后进行解析
        2. 提取其他需要下载的标签交给scrapy下载
        :param response: 爬取返回信息
        :return: 待爬取内容页面，待爬取URL页面
        """
        html = response.body.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        url_list = []
        for e in soup.select(".detail h3 a"):
            url_list.append(e["href"])

        for u in url_list:
            logging.log(logging.DEBUG, u)
            if "video" in u:
                continue
            else:
                yield Request(url=u, callback=self.parse_detail)

        label = soup.select("#main-list li a")
        for i in range(5, 12):
            yield Request(url=START_URL + label[i]["href"], callback=self.parse)

        """
        2018年05月28日11:39:40 腾讯新闻改版
        
            # 解析列表页中所有文章的url，并交给scrapy下载后进行解析
        html = response.body.decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        url_list = []
        # if response.urljoin
        if response.url == URL_WORLD:
            url_list.append(
                (soup.select("#subHot a img")[0].attrs["alt"], format_url(soup.select("#subHot a")[0].attrs["href"])))

            for ele in soup.select(".Q-tpWrap div em a"):
                url_list.append((ele.text, format_url(ele.attrs['href'])))
            for ele in soup.select(".Q-pList div em a"):
                url_list.append((ele.text, format_url(ele.attrs['href'])))

        elif response.url == URL_TECH:
            for e in soup.select(".Q-tpList div div h3 a"):
                url_list.append((e.attrs["title"], e.attrs['href']))

        for url in url_list:
            # logging.log(logging.INFO, url[0] + ":" + url[1])
            detail_url = url[1]
            yield Request(url=response.urljoin(detail_url), callback=self.parse_detail)

        # 提取其他需要下载的标签交给scrapy下载
        other_url = []
        other_url.append(soup.select("#navlinkSociety")[0].attrs["href"])  # 社会
        other_url.append(soup.select("#navlinkMil")[0].attrs["href"])  # 军事
        other_url.append("http://tech.qq.com/")  # 科技
        # other_url.append("http://ent.qq.com/")  # 娱乐
        # other_url.append("http://finance.qq.com/")  # 财经
        # other_url.append("http://sports.qq.com/")  # 财经
        for u in other_url:
            yield Request(url=u, callback=self.parse)
        """

        """
        # PqQuery Linux(Ubuntu 17)与Windows(win 10)解析不一致
        url_list.append((doc("#subHot").text(), format_url(doc("#subHot a").attr.href)))
        for ele in doc(".Q-tpWrap div em a"):
            url_list.append((ele.text, format_url(ele.attrib['href'])))
        for ele in doc(".Q-pList div em a"):
            url_list.append((ele.text, format_url(ele.attrib['href'])))

        for url in url_list:
            logging.log(logging.INFO, url[0] + ":" + url[1])
            yield Request(url=response.urljoin(url[1]), callback=self.parse_detail)
        提取其他需要下载的标签交给scrapy下载
        other_url = []
        other_url.append(doc("#navlinkSociety").attr("href"))
        for u in other_url:
            yield Request(url=u, callback=self.parse)
        """

    def parse_detail(self, response):
        """
        处理需要爬取页面的

        :param response: 内容页面返回信息
        :return: 待持久化item
        """
        tencent_item = TencentItem()
        soup = BeautifulSoup(response.body.decode("utf-8"), "html.parser")

        title = soup.select("h1")[0].text
        create_date = get_now_time()
        url = response.url
        url_object_id = get_md5(url)
        content = ""
        if len(soup.select("p")) > 0:
            content_list = soup.select("p")
            for element in content_list:
                content = content + remove_special_label(element.text)
            content_list = soup.select(".text")
            for element in content_list:
                content = content + remove_special_label(element.text)

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
