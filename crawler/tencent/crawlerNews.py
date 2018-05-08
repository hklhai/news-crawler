#!/home/hadoop/anaconda3/bin/python
# -*- coding: utf-8 -*-

from crawler.crawler_utils import *


def crawler_tencent_news():
    category_urls = []

    soup = get_url_content("http://news.qq.com/")
    url_list = soup.find(id="channelNavPart").find_all("li")
    for url in url_list:
        # 主要列表列表
        # print(url.string + " " + url.a["href"])
        category_urls.append((url.string, url.a["href"]))

    url_set = set()

    for url in category_urls:
        soup = get_url_content(url[1])
        if url[0] in ["首页", "国际", "社会", "军事"]:
            item_list = soup.select(".Q-tpWrap")
            for ele in item_list:
                url_set.add(ele.a["href"])
        elif url[0] in ["历史"]:
            item_list = soup.select(".newTopicL")[0].find_all("li")
            for ele in item_list:
                url_set.add(ele.a["href"])
        elif url[0] in ["文化"]:
            item_list = soup.select(".Q-pList")
            for ele in item_list:
                url_set.add(ele.a["href"])
        elif url[0] in ["公益"]:
            item_list = soup.select(".Q-tpWrap")
            for ele in item_list:
                if ele.a["href"].startswith("http"):
                    url_set.add(ele.a["href"])
                else:
                    url_set.add("http://gongyi.qq.com/" + ele.a["href"])
    print("=====================")
    print(url_set.__len__())

    # 遍历url获取网页内容
    for u in url_set:
        try:
            if u.startswith("//"):
                url = "http:" + u
            else:
                url = u
            title, now_time, content, url = get_title_content(url)
            if len(content) == 0:
                print(url)
            else:
                contents = title + "^" + now_time + "^" + content + "^" + url
            save_to_file(get_system_path() + get_now_date(), contents)
        except Exception as e:
            print(e)
            print(url)


crawler_tencent_news()
