# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BianjuItem(scrapy.Item):
    """
    持久化剧本信息
    """
    title = scrapy.Field()              # 新闻标题
    create_date = scrapy.Field()        # 爬取时间
    url = scrapy.Field()                # 爬取url
    url_object_id = scrapy.Field()      # url标识
    category = scrapy.Field()           # 类别
    content = scrapy.Field()            # 新闻内容
