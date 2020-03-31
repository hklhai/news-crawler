# -*- coding: utf-8 -*-

from tencent.utils.common import *

## my
num = "15110102180"

# num = "15652118939"

for i in range(20):
    browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
    browser.get("https://uac.10010.com/portal/homeLoginNew")
    time.sleep(1)
    browser.find_element_by_id("randomPwdTips").click()
    browser.find_element_by_xpath("//*[@id=\"userName\"]").send_keys(num)
    browser.find_element_by_xpath("//*[@id=\"randomCode\"]").click()
    time.sleep(61)
    browser.quit()
