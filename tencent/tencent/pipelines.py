# -*- coding: utf-8 -*-
import codecs
import json

import pymysql
from elasticsearch import Elasticsearch
from twisted.enterprise import adbapi

from tencent.utils.common import get_file_system_path, get_now_date
from tencent.utils.global_list import NEWS_INDEX, NEWS_TYPE, HOST_PORT


class TencentPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """
    1. 保存json数据到文件
    2. 持久化至ElasticSearch
    """

    def __init__(self):
        self.file = codecs.open(get_file_system_path() + get_now_date(), 'w', encoding="utf-8")
        self.es = Elasticsearch([HOST_PORT])

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)

        item_dict = dict(item)

        # 查询是否存在该title
        query_total = {'query': {'match_phrase': {'title': item_dict['title']}}}
        total = self.es.count(index=NEWS_INDEX, doc_type=NEWS_TYPE, body=query_total)
        if total['count'] == 0:
            body = json.dumps(dict(item), ensure_ascii=False)
            self.es.index(index=NEWS_INDEX, doc_type=NEWS_TYPE, body=body, id=None)
            return item
        else:
            return None

    def spider_closed(self, spider):
        self.file.close()


class MysqlPipeline(object):
    """
    插入mysql数据库
    未在pipeline启用ITEM_PIPELINES
    """

    def __init__(self):
        self.conn = pymysql.connect(host='spark2', port=3306, user='root', passwd='mysql', db='article_spider',
                                    use_unicode=True, charset="utf8")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = '''
        insert into tb_news(title,create_date,url,url_object_id,content) VALUES (%s,%s,%s,%s,%s)
        '''

        self.cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["url_object_id"], item["content"]))
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
        insert into tb_news(title,create_date,url,url_object_id,content) VALUES (%s,%s,%s,%s,%s)
        '''
        cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["url_object_id"], item["content"]))
