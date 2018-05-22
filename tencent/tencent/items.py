# -*- coding: utf-8 -*-

import scrapy

class TencentItem(scrapy.Item):
    """
    持久化新闻信息
    """
    title = scrapy.Field()              # 新闻标题
    create_date = scrapy.Field()        # 爬取时间
    url = scrapy.Field()                # 爬取url
    url_object_id = scrapy.Field()      # url标识
    content = scrapy.Field()            # 新闻内容
