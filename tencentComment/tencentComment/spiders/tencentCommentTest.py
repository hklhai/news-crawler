# -*- coding: utf-8 -*-

import random
import time

import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver

from tencentComment.utils.common import get_chrome_executable_path, debug_option, get_now_time
from tencentComment.utils.global_list import *
from tencentComment.utils.global_list import NO_COMMENT


class TencentcommentSpider(scrapy.Spider):
    name = 'tencentCommentTest'
    allowed_domains = [NEWS, NEW, SOCIETY, MIL, TECH, ENT, FINANCE, SPORTS]
    start_urls = [START_URL]

    def parse(self, response):
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=debug_option())
        browser.get("https://new.qq.com/omn/20180831/20180831A08F17.html")
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
                        try:
                            comment.click()
                        except Exception as err:
                            print(err)
                        time.sleep(5)
        # print(browser.page_source)
        soup = BeautifulSoup(browser.page_source, "html.parser")

        create_date = get_now_time()
        content = ""

        if len(soup.select("title")) != 0:
            title = response.url

            soup.select("#J_CommentTotal")
            if len(soup.select("#J_ShortComment .comment")) > 0:
                comment_block = soup.select("#J_ShortComment .comment .comment-block")
                for x in range(len(comment_block)):
                    """
                    soup.select("#J_ShortComment .comment .comment-block")[0].select("div")[0].text

                    soup.select("#J_ShortComment .comment .comment-block")
                    [0].select(".comment-operate")[0].select("span > i")[0]
                    [116].select(".comment-operate")[0].select("span > i")[0]
                    """
                    comment_text = comment_block[x].select("div")[0].text
                    comment_vote = comment_block[x].select(".comment-operate")[0].select("span > i")[0]
                    print(comment_text + " " + str(vote_num(str(comment_vote))))

                    """
                    soup.select("#J_ShortComment .comment .comment-block .reply-block")[0]
                    .select(".reply-content")[0].text

                    soup.select("#J_ShortComment .comment .comment-block .reply-block")
                    [0].select("div")[1].select("span > i")
                    [5].select("div")  size = 0   评论数据为0
                    """
                    reply_block = comment_block[x].select(".reply-block")
                    for y in range(len(reply_block)):
                        reply_text = reply_block[y].select(".reply-content")[0].text.split("  :  ")[1]
                        vote_list = reply_block[y].select("div")
                        if len(vote_list) == 2:
                            reply_vote = str(vote_list[1].select("span > i")[0])
                            reply_vote = vote_num(reply_vote)
                        else:
                            reply_vote = 0
                        print("    " + reply_text + " " + str(reply_vote))


def vote_num(str):
    str = str.replace("<i>", "").replace("</i>", "")
    if len(str) == 0:
        str = 0
    else:
        str = int(str)
    return str
