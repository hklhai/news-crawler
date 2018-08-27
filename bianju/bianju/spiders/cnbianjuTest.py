# -*- coding: utf-8 -*-

import urllib

import scrapy
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from bianju.common import *


class CnbianjuSpider(scrapy.Spider):
    name = 'cnbianjuTest'
    allowed_domains = ['www.bianju.me']
    start_urls = ['http://www.bianju.me/']

    def parse(self, response):
        # 登录成功
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=debug_option())
        browser.get("https://www.bianju.me/user_login.asp")
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"username\"]").send_keys("hkhai")
        browser.find_element_by_xpath("//*[@id=\"password\"]").send_keys("hk85151918")
        # browser.find_element_by_xpath("//*[@id=\"utype\"]").send_keys("编剧")
        browser.find_element_by_xpath('//input[@value="编剧"]').send_keys(Keys.SPACE)
        browser.find_element_by_xpath("//*[@name=\"Submit\"]").click()

        s = "https://www.bianju.me/telescript/?ClassName2=%C7%E0%B4%BA"
        browser.get(s)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        self.get_page_url_list(soup)

        # 翻页操作 获取是否存在下一页，存在就翻页，再调用get_page_url_list
        total_page = int(soup.select(".MainTableBorder")[5].findAll('tr')[45].select('font')[2].text)
        for i in range(2, total_page + 1):
            next_page_href = "https://www.bianju.me/telescript/?Page" + str(
                i) + "&ClassName=%B5%E7%CA%D3%BE%E7%BE%E7%B1%BE&ClassName2=%C7%E0%B4%BA&byType="
            print(next_page_href)
            browser.get(next_page_href)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            self.get_page_url_list(soup)
            print("=====")

    # 翻页获取所有的url
    def get_page_url_list(self, soup):
        tab = soup.select(".ziti3")[0]
        for tr in tab.findAll('tr'):
            for td in tr.findAll('td'):
                x = td.findAll("a")
                if len(x) > 0 and x[0]['href'].startswith('/Art'):
                    print("http://www.bianju.me/" + x[0]['href'] + "&CType=content")
