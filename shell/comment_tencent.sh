#! /bin/sh
export PATH=$PATH:/usr/local/bin:/home/ubuntu1/.virtualenvs/news-crawler-DDLWWNG6/bin


#进入.py脚本所在目录
cd /home/ubuntu1/Project/news-crawler/tencentComment

#执行.py中定义的项目，并指定日志文件，其中nohup....&表示可以在后台执行，不会因为关闭终端而导致程序执行中断。
v_date=$(date +%Y%m%d)

nohup scrapy crawl tencentComment  >> /home/hadoop/log/comment/comment_$v_date.log 2>&1 &