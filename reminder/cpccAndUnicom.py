# -*- coding: utf-8 -*-
import os
import sys
import time
from selenium import webdriver

sys.path.append(os.path.dirname(os.getcwd()))

from reminder.common import get_chrome_executable_path, chrome_option, get_now_date


def judge_no_crawler(supervise_path):
    """
    判断制定目录下，制定文件大小为0
    :return:  返回真
    """

    filepath = supervise_path + get_now_date()
    file_size = os.path.getsize(filepath)
    if file_size == 0:
        return True
    else:
        return False


def shot_message(phone_number, phone_type):
    """
    发送两条短信
    :return:
    """
    if phone_type == "cpcc":
        for i in range(2):
            browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
            browser.get("https://login.10086.cn/login.html")
            time.sleep(1)
            browser.find_element_by_id("sms_login_1").click()
            browser.find_element_by_xpath("//*[@id=\"sms_name\"]").send_keys(phone_number)
            browser.find_element_by_xpath("//*[@id=\"getSMSPwd1\"]").click()
            time.sleep(62)
            browser.quit()
    else:
        for i in range(2):
            browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
            browser.get("https://uac.10010.com/portal/homeLoginNew")
            time.sleep(1)
            browser.find_element_by_id("randomPwdTips").click()
            browser.find_element_by_xpath("//*[@id=\"userName\"]").send_keys(phone_number)
            browser.find_element_by_xpath("//*[@id=\"randomCode\"]").click()
            time.sleep(62)
            browser.quit()


if __name__ == '__main__':
    """
    打包
    cd /home/hadoop/PycharmProjects/news-crawle
    pipenv shell
    pyinstaller -F reminder/cpccAndUnicom.py
    """
    news_path = r"/home/hadoop/news/"
    comment_path = r"/home/hadoop/comment/"

    if judge_no_crawler(news_path):
        shot_message("18813030755", "cpcc")
        shot_message("15650725868", "unicom")
        print(get_now_date() + "日新闻采集异常")
    elif judge_no_crawler(comment_path):
        shot_message("18813030755", "cpcc")
        shot_message("15650725868", "unicom")
        print(get_now_date() + "日评论采集异常")
    else:
        print(get_now_date() + "日采集正常")
