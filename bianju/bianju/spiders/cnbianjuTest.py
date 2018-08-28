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
        # todo
        # for i in range(1, total_page + 1):
        for i in range(1, 2):
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
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=debug_option())
        browser.get("https://www.bianju.me/user_login.asp")
        time.sleep(1)
        # 随机获取用户名密码
        user_tuple = get_user_password()
        browser.find_element_by_xpath("//*[@id=\"username\"]").send_keys(user_tuple[0])
        browser.find_element_by_xpath("//*[@id=\"password\"]").send_keys(user_tuple[1])
        browser.find_element_by_xpath('//input[@value="编剧"]').send_keys(Keys.SPACE)
        browser.find_element_by_xpath("//*[@name=\"Submit\"]").click()
        browser.get(response.url)
        product_id = get_url_product_id(response.url)

        soup = BeautifulSoup(browser.page_source, "html.parser")

        a_list = soup.findAll("table")[5].findAll('table')[5].select('a')
        total_page = 0
        for j in range(len(a_list)):
            if a_list[j]['href'].startswith('Art_list.asp'):
                total_page += 1
            else:
                if total_page == 0:
                    continue
                else:
                    break

        title = soup.select(".title")[0].text
        print(title)
        category = soup.findAll("table")[5].findAll('table')[0].findAll('font')[0].text
        print(category)

        # 先获取页数 for循环取出
        content = ""
        for i in range(1, int(total_page) + 1):
            url = "https://www.bianju.me/Art_list.asp?id=" + product_id + "&page=" + str(i) + "&CType=content"
            browser.get(url)
            time.sleep(1)

            soup = BeautifulSoup(browser.page_source, "html.parser")
            table = soup.findAll("table")[5].findAll('table')[5]
            content_page = ""

            for tr in table.tbody.findAll('tr'):
                for td in tr.findAll('td'):
                    text = td.getText()

                    text_list = text.split('\n')
                    script_list = []
                    for i in range(len(text_list)):
                        if "【本作品" in text_list[i] or "[编辑" in text_list[i] or len(text_list[i]) < 20:
                            continue
                        else:
                            script_list.append(text_list[i])
                    list = script_list[0].split('\u3000\u3000')
                    content_page = ""
                    for i in range(len(list)):
                        content_page += list[i]
                        content_page += "\n"
                # print(content_page)
                break;
            content += content_page
        print(content)
        print("======================")

        bianju_item = BianjuItem()
