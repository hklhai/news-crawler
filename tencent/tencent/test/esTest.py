# -*- coding: utf-8 -*-
from datetime import datetime
from elasticsearch import Elasticsearch

body = {"name": 'lucy', 'sex': 'female', 'age': 10}
es = Elasticsearch(['spark3:9200'])
es.index(index='testindex', doc_type='texttype', body=body, id=None)
