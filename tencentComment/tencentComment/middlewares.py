# -*- coding: utf-8 -*-

import random
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from tencentComment.utils.common import get_chrome_executable_path, chrome_option
from tencentComment.utils.global_list import NO_COMMENT


class TencentcommentSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TencentcommentDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.name == "tencentComment":
            browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
            browser.get(request.url)
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

            return HtmlResponse(url=title, body=browser.page_source, encoding="utf-8", request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
