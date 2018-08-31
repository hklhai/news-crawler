# -*- coding: utf-8 -*-
from urllib import parse
from urllib.parse import urlencode

from tencentComment.utils.common import get_pre_week

url = '?ClassName=电视剧剧本&ClassName2=青春'
urla = url.split("?")
res = parse.parse_qs(urla[1])
print(res)
print(urlencode(res))

pre_week = get_pre_week()

print(pre_week)

title = "  "
content = "  "

if len(title) > 0 & len(content) > 0:
    print(1)
else:
    print(2)

str = "<i></i>"


def vote_num(str):
    str = str.replace("<i>", "").replace("</i>", "")
    if len(str) == 0:
        str = 0
    else:
        str = int(str)
    return str


print(vote_num(str))