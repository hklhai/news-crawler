# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from bianju.common import *


class CnbianjuSpider(scrapy.Spider):
    name = "cnbianjuTest"
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

        url = "https://www.bianju.me/Art_list.asp?id=15132&CType=content"
        #
        # url = "https://www.bianju.me/Art_list.asp?id=15119&CType=content"
        product_id = get_url_product_id(url)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")

        a_list = soup.select(".ziti_14px")[0].select('a')
        total_page_url = ""
        for j in range(len(a_list) - 1, -1, -1):
            if 'href' in a_list[j].attrs and a_list[j]['href'].startswith('Art_list.asp'):
                total_page_url = a_list[j]['href']
                break

        total_page = int(get_url_product_page(total_page_url))

        title = soup.select(".title")[0].text
        print(title)
        product_info = soup.findAll("table")[5].findAll('table')[0].findAll('font')

        category = product_info[0].text
        word_count = product_info[1].text
        submission_time = product_info[2].text

        # 可能存在不存在修改时间的情况
        if len(product_info) == 5:
            modify_time = product_info[3].text
            read_times = product_info[4].text
        else:
            modify_time = ""
            read_times = product_info[3].text

        print(category + " " + word_count + " " + submission_time + " " + modify_time + " " + read_times)

        # 先获取页数 for循环取出
        content = ""
        for i in range(1, total_page + 1):
            url = "https://www.bianju.me/Art_list.asp?id=" + product_id + "&page=" + str(i) + "&CType=content"
            browser.get(url)
            browser.set_script_timeout(5)

            soup = BeautifulSoup(browser.page_source, "html.parser")
            table = soup.select("#zoom")[0]
            content_page = ""

            for tr in table.findAll('tr'):
                for td in tr.findAll('td'):
                    text = td.getText()

                    text_list = text.split('\n')
                    script_list = []
                    for x in range(len(text_list)):
                        if "【本作品" in text_list[x] or "[编辑" in text_list[x] or len(text_list[x]) < 20:
                            continue
                        else:
                            script_list.append(text_list[x])
                    print(url)
                    content_list = script_list[0].split('\u3000\u3000')
                    content_page = ""
                    for y in range(len(content_list)):
                        content_page += content_list[y]
                        content_page += "\n"
                break
            content += content_page

        print(content)
        print("======================")
