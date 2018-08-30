# -*- coding: utf-8 -*-

import random
import time

import scrapy
from selenium import webdriver

from tencentComment.utils.common import get_chrome_executable_path, debug_option
from tencentComment.utils.global_list import *
from tencentComment.utils.global_list import NO_COMMENT


class TencentcommentSpider(scrapy.Spider):
    name = 'tencentCommentTest'
    allowed_domains = [NEWS, NEW, SOCIETY, MIL, TECH, ENT, FINANCE, SPORTS]
    start_urls = [START_URL]

    def parse(self, response):
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=debug_option())
        browser.get("https://new.qq.com/omn/20180810/20180810A065JA.html")
        sleep_time = random.uniform(2, 3)
        time.sleep(sleep_time)
        title = browser.find_elements_by_tag_name("h1")[0].text

        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        browser.switch_to.frame("commentIframe")
        time.sleep(2)

        if browser.page_source.__contains__("comment-moreBtn"):
            comment_element = browser.find_element_by_xpath("//*[contains(@class, 'comment-moreBtn')]")
            comment_text = comment_element.text
            comment_element.click()
            time.sleep(2)

            if comment_element is not None:
                while True:
                    if comment_text == NO_COMMENT:
                        break
                    else:
                        # reply-allBtn J_ReplyMoreBtn  查看全部回复   J_ReplyMoreBtn reply-moreBtn
                        while browser.page_source.__str__().__contains__("reply-allBtn J_ReplyMoreBtn"):
                            reply = browser.find_element_by_xpath(
                                "//*[contains(@class, 'reply-allBtn J_ReplyMoreBtn')]")
                            reply.click()
                            time.sleep(1)

                        # J_ReplyMoreBtn reply-moreBtn 查看更多回复
                        while browser.page_source.__str__().__contains__("J_ReplyMoreBtn reply-moreBtn"):
                            try:
                                reply_more_btn = browser.find_element_by_xpath(
                                    "//*[contains(@class, 'J_ReplyMoreBtn reply-moreBtn')]")
                                reply_more_btn.click()
                                time.sleep(1)
                            except Exception as err:
                                print(err)

                        # comment-noMore 更多评论
                        if browser.page_source.__str__().__contains__("comment-noMore"):
                            comment = browser.find_element_by_xpath("//*[contains(@class, 'comment-noMore')]")
                        else:
                            comment = browser.find_element_by_xpath("//*[contains(@class, 'comment-moreBtn')]")

                        comment_text = comment.text
                        time.sleep(2)
                        comment.click()
                        time.sleep(5)
        print(browser.page_source)
