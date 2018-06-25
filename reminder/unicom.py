# -*- coding: utf-8 -*-

import time

from selenium import webdriver

from common import get_chrome_executable_path, chrome_option

for i in range(6):
    browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
    browser.get("https://uac.10010.com/portal/homeLoginNew")
    time.sleep(1)
    browser.find_element_by_id("randomPwdTips").click()
    # browser.find_element_by_xpath("//*[@id=\"userName\"]").send_keys("17600113116")
    # browser.find_element_by_xpath("//*[@id=\"userName\"]").send_keys("15650725868")
    browser.find_element_by_xpath("//*[@id=\"userName\"]").send_keys("13261296655")
    browser.find_element_by_xpath("//*[@id=\"randomCode\"]").click()
    time.sleep(1)
    browser.quit()
