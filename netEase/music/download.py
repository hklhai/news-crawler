# -*- coding: utf-8 -*-
import urllib

from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse

from netEase.music.common import *

url = "https://music.163.com/#/discover/toplist?id=3778678"
path = "E://music//"

browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
browser.get(url)
sleep_time = random.uniform(2, 3)
time.sleep(sleep_time)

iframe = browser.find_elements_by_tag_name('iframe')[0]
browser.switch_to.frame(iframe)

response = HtmlResponse(url=url, body=browser.page_source, encoding="utf-8", request=None)
html = response.body.decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

"""
0~2
soup.select("tbody .tt")[i].select("a")[1].select("b")[0]["title"]
soup.select("tbody .tt")[i].select("a")[1]["href"]

3~n-1
soup.select("tbody .tt")[j].select("a")[0].select("b")[0]["title"]
soup.select("tbody .tt")[j].select("a")[0]["href"]
"""
name_url_list = []
i = 0
for e in soup.select("tbody .tt"):
    if i < 3 & len(e.select("a")) == 2:
        title = e.select("a")[1].select("b")[0]["title"]
        href = e.select("a")[1]["href"]
    else:
        if len(e.select("a")[0].select("b")) >= 1:
            title = e.select("a")[0].select("b")[0]["title"]
        else:
            title = e.select("a")[1].select("b")[0]["title"]
        href = e.select("a")[0]["href"]

    i += 1
    num = str(href).split("=")[1]
    down_href = "http://music.163.com/song/media/outer/url?id=" + num + ".mp3"
    name_url_list.append((title, down_href))

print(len(name_url_list))

for m in range(0, len(name_url_list)):
    print('正在下载第{}首。。。', (m + 1))
    print(str(m).zfill(3) + ":" + name_url_list[m][1])

    name = '{}.mp3'.format(str(m + 1).zfill(3) + name_url_list[m][0]).replace("/", "").replace(":", "")
    name = path + name
    urllib.request.urlretrieve(name_url_list[m][1], name)
