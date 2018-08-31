# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from scrapy import Request

from tencentComment.items import TencentCommentItem
from tencentComment.utils.common import get_now_time, get_pre_week_url_list
from tencentComment.utils.global_list import *


class TencentcommentSpider(scrapy.Spider):
    name = 'tencentComment'
    allowed_domains = [NEWS, NEW, SOCIETY, MIL, TECH, ENT, FINANCE, SPORTS]
    start_urls = [START_URL]

    def parse(self, response):
        """
        腾讯新闻评论爬虫主要逻辑
        :param response:
        :return:
        """
        # url_list = ["http://new.qq.com/omn/20180511/20180511A04WBW.html",
        #             "http://new.qq.com/omn/20180510/20180510A1DSGA.html"]
        # 过滤
        url_list = get_pre_week_url_list()
        for url in url_list:
            yield Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        tencent_item = TencentCommentItem()
        soup = BeautifulSoup(response.body.decode("utf-8"), "html.parser")

        create_date = get_now_time()
        content = ""
        tencent_item_list = []
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
                    tencent_item = TencentCommentItem()
                    tencent_item["title"] = title
                    tencent_item["create_date"] = create_date
                    tencent_item["content"] = comment_text
                    tencent_item['vote_number'] = vote_num(str(comment_vote))
                    tencent_item_list.append(tencent_item)

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
                        tencent_item = TencentCommentItem()
                        tencent_item["title"] = title
                        tencent_item["create_date"] = create_date
                        tencent_item["content"] = reply_text
                        tencent_item['vote_number'] = reply_vote
                        tencent_item_list.append(tencent_item)

            return tencent_item_list


def vote_num(str):
    str = str.replace("<i>", "").replace("</i>", "")
    if len(str) == 0:
        str = 0
    else:
        str = int(str)
    return str
