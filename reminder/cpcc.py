# -*- coding: utf-8 -*-

import time

from selenium import webdriver

from tencent.utils.common import chrome_option, get_chrome_executable_path

num = "15110102180"


for i in range(23):
    browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
    browser.get("https://login.10086.cn/login.html")
    time.sleep(1)
    browser.find_element_by_id("sms_login_1").click()
    browser.find_element_by_xpath("//*[@id=\"sms_name\"]").send_keys(num)
    browser.find_element_by_xpath("//*[@id=\"getSMSPwd1\"]").click()
    time.sleep(61)
    browser.quit()