#!/home/hadoop/anaconda3/bin/python
# -*- coding: utf-8 -*-

import schedule

from crawler.tencent.crawlerNews import *

# tencent news
schedule.every().day.at("09:26").do(crawler_tencent_news())

while True:
    schedule.run_pending()
    time.sleep(1)
