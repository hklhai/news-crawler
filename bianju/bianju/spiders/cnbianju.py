# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
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
        browser.find_element_by_xpath('//input[@value="编剧"]').send_keys(Keys.SPACE)
        browser.find_element_by_xpath("//*[@name=\"Submit\"]").click()

        browser.get("https://www.bianju.me/Art_list.asp?ID=17167&page=1&CType=content")
        soup = BeautifulSoup(browser.page_source, "html.parser")
        title = soup.select(".title")[0].text
        print(title)
        category = soup.findAll("table")[5].findAll('table')[0].findAll('font')[0].text
        print(category)
        table = soup.findAll("table")[5].findAll('table')[5]
        a_list = soup.findAll("table")[5].findAll('table')[5].select('a')
        total_page = soup.findAll("table")[5].findAll('table')[5].select('a')[len(a_list) - 4].text[1:2]

        content = ""
        for i in range(int(total_page)+1):
            url = "https://www.bianju.me/Art_list.asp?ID=17167&page=" + str(i) + "&CType=content"
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
