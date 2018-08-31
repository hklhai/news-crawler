# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch

# ElasticSearch地址,其中ubuntu1为179机器
es = Elasticsearch(["ubuntu1:9200"])

# index,type
index_name = "script_data"
type_name = "script"

# 获取总数
count = es.count(index=index_name, doc_type=type_name)['count']

# 查询全部数据
data = es.search(index=index_name, doc_type=type_name, body={"size": count})['hits']['hits']

# for i in range(len(data) - 1):
for i in range(2):
    print(str(data[i]['_source']))
