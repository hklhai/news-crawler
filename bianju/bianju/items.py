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
    word_count = scrapy.Field()         # 字数
    submission_time = scrapy.Field()    # 投稿时间
    modify_time = scrapy.Field()        # 修改时间
    read_times = scrapy.Field()         # 阅读数
    content = scrapy.Field()            # 新闻内容
