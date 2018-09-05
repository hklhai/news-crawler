# -*- coding: utf-8 -*-

import codecs
import os

from elasticsearch import Elasticsearch


def export(file_path):
    """
    导出到指定文件夹下所有作品信息
    :param file_path: 文件路径
    """
    es = Elasticsearch(["ubuntu3:9200"])
    index_name = "telescript_data"
    type_name = "telescript"

    count = es.count(index=index_name, doc_type=type_name)['count']
    body = {"size": count}
    data = es.search(index=index_name, doc_type=type_name, body=body)['hits']['hits']

    for i in range(len(data) - 1):
        es_source = data[i]["_source"]
        path_name = file_path + es_source['category']
        is_exists = os.path.exists(path_name)
        if not is_exists:
            os.makedirs(path_name)

        # 去除作品名中的特殊字符
        title = es_source['title'].replace("/", "")
        file_name = file_path + es_source['category'] + "/" + title
        file = codecs.open(file_name, 'w', encoding="utf-8")
        file.write(es_source['content'])


if __name__ == '__main__':
    file_path = "/home/hadoop/bianju/telescript/"
    export(file_path)
