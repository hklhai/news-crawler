# -*- coding: utf-8 -*-

import time

from selenium import webdriver

from reminder.common import get_chrome_executable_path, chrome_option


def shot_message():
    for i in range(3):
        browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
        browser.get("https://login.10086.cn/login.html")
        time.sleep(1)
        browser.find_element_by_id("sms_login_1").click()
        browser.find_element_by_xpath("//*[@id=\"sms_name\"]").send_keys("18813030755")
        browser.find_element_by_xpath("//*[@id=\"getSMSPwd1\"]").click()
        time.sleep(1)
        browser.quit()


if __name__ == '__main__':
    shot_message()
