# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import json
import pymysql
from twisted.enterprise import adbapi

from tencentComment.utils.common import get_file_system_path, get_now_date

class TencentcommentPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):
    """
    返回json数据到文件
    """

    def __init__(self):
        self.file = codecs.open(get_file_system_path() + get_now_date(), 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    """
    插入mysql数据库
    未在pipeline启用ITEM_PIPELINES
    """

    def __init__(self):
        self.conn = pymysql.connect(host='spark2', port=3306, user='root', passwd='mysql', db='comment_spider',
                                    use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
        insert into tb_news(title,create_date,url,content) VALUES (%s,%s,%s,%s)
        '''

        self.cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"],item["content"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    """
    采用异步的方式插入数据
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            port=settings["MYSQL_PORT"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWD"],
            db=settings["MYSQL_DB"],
            use_unicode=True,
            charset="utf8",
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将mysql插入变成异步
        :param item:
        :param spider:
        :return:
        """
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 具体插入数据
        insert_sql = '''
        insert into tb_news(title,create_date,url,content) VALUES (%s,%s,%s,%s)
        '''
        cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["content"]))
