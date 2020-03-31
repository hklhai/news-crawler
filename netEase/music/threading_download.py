# -*- coding: utf-8 -*-
import threading
import urllib

from bs4 import BeautifulSoup
from scrapy.http import HtmlResponse

from netEase.music.common import *

url = "https://music.163.com/#/discover/toplist?id=3778678"
path = "E://music//"
# 线程数
thread_num = 20


def download(music_url, music_name, i):
    music_name = music_name.replace("/", "").replace(":", "")
    name = '{}.mp3'.format(str(i + 1).zfill(3) + music_name)
    name = path + name
    urllib.request.urlretrieve(music_url, name)


def get_music_list():
    browser = webdriver.Chrome(executable_path=get_chrome_executable_path(), chrome_options=chrome_option())
    browser.get(url)
    sleep_time = random.uniform(2, 3)
    time.sleep(sleep_time)

    iframe = browser.find_elements_by_tag_name('iframe')[0]
    browser.switch_to.frame(iframe)

    response = HtmlResponse(url=url, body=browser.page_source, encoding="utf-8", request=None)
    html = response.body.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    i = 0
    for e in soup.select("tbody .tt"):
        if i < 3 & len(e.select("a")) == 2:
            title = e.select("a")[1].select("b")[0]["title"]
            href = e.select("a")[1]["href"]
        else:
            title = e.select("a")[0].select("b")[0]["title"]
            href = e.select("a")[0]["href"]
        i += 1
        num = str(href).split("=")[1]
        down_href = "http://music.163.com/song/media/outer/url?id=" + num + ".mp3"
        # name_url_list.append((title, down_href))
        yield down_href, title, i


lock = threading.Lock()


def loop(imgs):
    print('thread %s is running...' % threading.current_thread().name)
    while True:
        try:
            with lock:
                img_url, img_name, i = next(imgs)
        except StopIteration:
            break
        try:
            download(img_url, img_name, i)
        except:
            print('exceptfail\t%s' % img_url)

    print('thread %s is end...' % threading.current_thread().name)


music_list = get_music_list()

for i in range(0, thread_num):
    t = threading.Thread(target=loop, name='LoopThread %s' % i, args=(music_list,))
    t.start()
