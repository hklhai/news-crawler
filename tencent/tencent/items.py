# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TencentItem(scrapy.Item):
    """
    持久化新闻信息
    """
    title = scrapy.Field()              # 新闻标题
    create_date = scrapy.Field()        # 爬取时间
    url = scrapy.Field()                # 爬取url
    url_object_id = scrapy.Field()
    content = scrapy.Field()
