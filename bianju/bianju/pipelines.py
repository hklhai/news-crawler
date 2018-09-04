# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

from elasticsearch import Elasticsearch

from bianju.common import HOST_PORT, SCRIPT_INDEX, SCRIPT_TYPE


class BianjuPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    """
    返回json数据到文件
    """

    def __init__(self):
        # self.file = codecs.open(get_comment_file_system_path() + get_now_date(), 'w', encoding="utf-8")
        self.es = Elasticsearch([HOST_PORT])

    def process_item(self, item, spider):
        """
        不保存至本地文件系统，仅保存至ElasticSearch
        """
        item_dict = dict(item)
        # 查询是否存在该
        query_total = {'query': {'match_phrase': {'url_object_id': item_dict['url_object_id']}}}
        total = self.es.count(index=SCRIPT_INDEX, doc_type=SCRIPT_TYPE, body=query_total)
        if total['count'] == 0:
            # lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
            # self.file.write(lines)

            body = json.dumps(dict(item), ensure_ascii=False)
            self.es.index(index=SCRIPT_INDEX, doc_type=SCRIPT_TYPE, body=body, id=None)
            return item
        else:
            return None

    def spider_closed(self, spider):
        self.file.close()
