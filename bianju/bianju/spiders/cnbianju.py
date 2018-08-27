# -*- coding: utf-8 -*-

import scrapy
from selenium.webdriver.common.keys import Keys

from bianju.common import *


class CnbianjuSpider(scrapy.Spider):
    name = 'cnbianju'
    allowed_domains = ['www.bianju.me']
    start_urls = ['http://www.bianju.me/']

    def parse(self, response):
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=debug_option())
        browser.get("https://www.bianju.me/user_login.asp")
        time.sleep(1)
        browser.find_element_by_xpath("//*[@id=\"username\"]").send_keys("hkhai")
        browser.find_element_by_xpath("//*[@id=\"password\"]").send_keys("hk85151918")
        # browser.find_element_by_xpath("//*[@id=\"utype\"]").send_keys("编剧")
        browser.find_element_by_xpath('//input[@value="编剧"]').send_keys(Keys.SPACE)
        browser.find_element_by_xpath("//*[@name=\"Submit\"]").click()
