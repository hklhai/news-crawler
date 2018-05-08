#!/home/hadoop/anaconda3/bin/python
# -*- coding: utf-8 -*-
from crawler.crawler_utils import *

urls = ["https://mp.weixin.qq.com/s?__biz=MzIzNTAyODMwOA==&mid=2650208048&idx=1&sn=88008f3c0b56aaaa734de261c9aeb130&chksm=f0ef3d0bc798b41d7c32e360084226eacea7b8fc160080c120b3e7ba4754f681b90b07f69b68#rd",
        "https://news.qq.com/a/20180502/040440.htm",
        "http://new.qq.com/omn/20180503/20180503A05S0L.html"]

for url in urls:
    title, now_time, content, url = get_title_content(url)
    contents = title + "^" + now_time + "^" + content + "^" + url
    save_to_file(get_system_path() + get_now_date(), contents)
