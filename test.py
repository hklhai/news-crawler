# -*- coding: utf-8 -*-


# url = '?ClassName=电视剧剧本&ClassName2=青春'
# urla = url.split("?")
# res = parse.parse_qs(urla[1])
# print(res)
# print(urlencode(res))
#
# pre_week = get_pre_week()
#
# print(pre_week)
#
# title = "  "
# content = "  "
#
# if len(title) > 0 & len(content) > 0:
#     print(1)
# else:
#     print(2)
#
# str = "<i></i>"
#
#
# def vote_num(str):
#     str = str.replace("<i>", "").replace("</i>", "")
#     if len(str) == 0:
#         str = 0
#     else:
#         str = int(str)
#     return str
#
#
# print(vote_num(str))


# ==================================
# url = "https://www.bianju.me/Art_list.asp?id=17313&CType=content"
# from elasticsearch import Elasticsearch
#
# from bianju.common import *
#
# url = "http://www.bianju.me/Art_list.asp?id=17313&CType=content"
# es = Elasticsearch([HOST_PORT])
# x = convert_url(url)
# url_md5 = get_md5(x)
# query_total = {"query": {"match": {"url_object_id": url_md5}}}
#
# total = es.count(index=SCRIPT_INDEX, doc_type=SCRIPT_TYPE, body=query_total)
# print(total['count'])

# ====================================
#
# url = "https://www.bianju.me//Art_list.asp?id=17313&CType=content"
# https_url = convert_url(url)
# print(https_url)


# ====================================
from bs4 import BeautifulSoup
from selenium.webdriver.android import webdriver

from bianju.common import *

browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=debug_option())
browser.get("https://www.iqiyi.com/v_19rrhohoqk.html#vfrm=2-4-0-1")
time.sleep(5)

soup = BeautifulSoup(browser.page_source, "html.parser")