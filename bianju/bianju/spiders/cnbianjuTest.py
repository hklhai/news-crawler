# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request
from selenium.webdriver.common.keys import Keys

from bianju.common import *
from bianju.items import BianjuItem


class CnbianjuSpider(scrapy.Spider):
    name = "cnbianjuTest"
    allowed_domains = ['www.bianju.me']
    start_urls = ['http://www.bianju.me/']

    def parse(self, response):
        # 登录成功
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=debug_option())
        browser.get("https://www.bianju.me/user_login.asp")
        time.sleep(1)

        # 随机获取用户名密码
        user_tuple = get_user_password()

        browser.find_element_by_xpath("//*[@id=\"username\"]").send_keys(user_tuple[0])
        browser.find_element_by_xpath("//*[@id=\"password\"]").send_keys(user_tuple[1])
        browser.find_element_by_xpath('//input[@value="编剧"]').send_keys(Keys.SPACE)
        browser.find_element_by_xpath("//*[@name=\"Submit\"]").click()

        browser.get(YOUTH_PAGE)
        soup = BeautifulSoup(browser.page_source, "html.parser")

        # 翻页操作 获取是否存在下一页，存在就翻页，再调用get_page_url_list
        total_page = int(soup.select(".MainTableBorder")[5].findAll('tr')[45].select('font')[2].text)
        for i in range(1, total_page + 1):
            next_page_href = PAGE_URL_START + str(i) + PAGE_URL_END
            print(next_page_href)
            time.sleep(1)
            browser.get(next_page_href)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            tab = soup.select(".ziti3")[0]
            for tr in tab.findAll('tr'):
                for td in tr.findAll('td'):
                    x = td.findAll("a")
                    if len(x) > 0 and x[0]['href'].startswith('/Art'):
                        url = PRODUCT_URL_START + x[0]['href'] + PRODUCT_URL_END
                        print(url)
                        yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        """
        处理需要爬取页面的

        :param response: 内容页面返回信息
        :return: 待持久化item
        """
        bianju_item = BianjuItem()

        soup = BeautifulSoup(response.body.decode("utf-8"), "html.parser")
        title = soup.select(".title")[0].text
        print(title)
        category = soup.findAll("table")[5].findAll('table')[0].findAll('font')[0].text
        table = soup.findAll("table")[5].findAll('table')[5]
        for tr in table.tbody.findAll('tr'):
            for td in tr.findAll('td'):
                text = td.getText()
                if text.startswith("【本作品已"):
                    continue
                print(text + "\n")
            break;
