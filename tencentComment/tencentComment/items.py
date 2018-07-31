# -*- coding: utf-8 -*-


import scrapy


class TencentCommentItem(scrapy.Item):
    """
    持久化新闻评论，仅爬取一次
    """
    title = scrapy.Field()          # 新闻标题
    create_date = scrapy.Field()    # 爬取时间
    content = scrapy.Field()        # 新闻评论内容

