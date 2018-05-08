#!/home/hadoop/anaconda3/bin/python
# -*- coding: utf-8 -*-

from crawler.crawler_utils import *

category_urls = ["http://news.163.com/domestic/",
                 "http://news.163.com/world/"]
url_set = set()
for url in category_urls:
    soup = get_url_content(url)
    item_list = soup.find_all(name="h3")
    for ele in item_list:
        href = ele.a["href"]
        if href.startswith("http://news.163.com/"):
            url_set.add(href)

print("=====================")
print(url_set.__len__())
