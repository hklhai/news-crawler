# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
from scrapy import Request
from selenium.webdriver.common.keys import Keys

from bianju.common import *
from bianju.items import BianjuItem


class CnbianjuSpider(scrapy.Spider):
    name = 'cnbianju'
    allowed_domains = ['www.bianju.me']
    start_urls = ['http://www.bianju.me/']

    def parse(self, response):
        # 登录成功
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
        browser.get(LOGIN_PAGE)

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
            # for i in range(1, 2):
            next_page_href = PAGE_URL_START + str(i) + PAGE_URL_END
            print(next_page_href)
            browser.get(next_page_href)
            browser.set_script_timeout(5)

            soup = BeautifulSoup(browser.page_source, "html.parser")
            tab = soup.select(".ziti3")[0]
            for tr in tab.findAll('tr'):
                for td in tr.findAll('td'):
                    x = td.findAll("a")
                    if len(x) > 0 and x[0]['href'].startswith('/Art'):
                        url = PRODUCT_URL_START + x[0]['href'] + PRODUCT_URL_END

                        # 如果存在url不做yield
                        es = Elasticsearch([HOST_PORT])
                        query_total = {'query': {'match_phrase': {'url_object_id': get_md5(url)}}}
                        total = es.count(index=SCRIPT_INDEX, doc_type=SCRIPT_TYPE, body=query_total)
                        if total['count'] > 0:
                            continue
                        print(url)
                        yield Request(url=url, callback=self.parse_detail)
        browser.close()

    def parse_detail(self, response):
        """
        处理需要爬取页面的

        :param response: 内容页面返回信息
        :return: 待持久化item
        """

        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
        browser.get(LOGIN_PAGE)
        # 随机获取用户名密码
        user_tuple = get_user_password()
        browser.find_element_by_xpath("//*[@id=\"username\"]").send_keys(user_tuple[0])
        browser.find_element_by_xpath("//*[@id=\"password\"]").send_keys(user_tuple[1])
        browser.find_element_by_xpath('//input[@value="编剧"]').send_keys(Keys.SPACE)
        browser.find_element_by_xpath("//*[@name=\"Submit\"]").click()
        browser.get(response.url)
        browser.set_script_timeout(5)

        product_id = get_url_product_id(response.url)
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

            for tr in table.tbody.findAll('tr'):
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

        create_date = get_now_time()
        url_object_id = get_md5(response.url)

        bianju_item = BianjuItem()
        bianju_item["title"] = title
        bianju_item["create_date"] = create_date
        bianju_item["url"] = response.url
        bianju_item["url_object_id"] = url_object_id
        bianju_item["word_count"] = word_count
        bianju_item["submission_time"] = submission_time
        bianju_item["modify_time"] = modify_time
        bianju_item["read_times"] = read_times
        bianju_item['content'] = content
        browser.close()
        return bianju_item
