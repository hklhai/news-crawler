# -*- coding: utf-8 -*-
from urllib import parse
from urllib.parse import urlencode

url = '?ClassName=电视剧剧本&ClassName2=青春'
urla = url.split("?")
res = parse.parse_qs(urla[1])
print(res)
print(urlencode(res))
