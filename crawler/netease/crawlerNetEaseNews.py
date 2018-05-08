#!/home/hadoop/anaconda3/bin/python
# -*- coding: utf-8 -*-

from crawler.crawler_utils import *

category_urls = []

soup = get_url_content("http://news.163.com/")
url_list = soup.find_all(name="div", attrs={"class": "ns_area list"})[0].findAll("a")
for url in url_list:
    category_urls.append((url.string, url["href"]))

url_set = set()

for url in category_urls:
    soup = get_url_content(url[1])
    if url[0] in ["首页"]:
        pass
    elif url[0] in ["国内", "国际", "社会", "军事", "航空"]:
        item_list = soup.find_all(name="h3")
        for ele in item_list:
            href = ele.a["href"]
            if href.startswith("http://news.163.com/"):
                url_set.add(href)

print("=====================")
print(url_set.__len__())
