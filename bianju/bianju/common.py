# -*- coding: utf-8 -*-

import datetime
import hashlib
import json
import platform
import random
import time
from urllib import parse

from selenium import webdriver

# 电视剧剧本-青春
# YOUTH_PAGE = "https://www.bianju.me/telescript/?ClassName2=%C7%E0%B4%BA"
# PAGE_URL_END = "&ClassName=%B5%E7%CA%D3%BE%E7%BE%E7%B1%BE&ClassName2=%C7%E0%B4%BA&byType="

# 电视剧剧本
# YOUTH_PAGE = "https://www.bianju.me/telescript/"
# PAGE_URL_END = "&ClassName=%B5%E7%CA%D3%BE%E7%BE%E7%B1%BE&ClassName2=&byType="

# 电影剧本
YOUTH_PAGE = "https://www.bianju.me/screenplay/"
PAGE_URL_END = "&ClassName=%B5%E7%D3%B0%BE%E7%B1%BE&ClassName2=&byType="

# 网络大电影剧本
# YOUTH_PAGE = "https://www.bianju.me/NetScreenplay/"
# PAGE_URL_END = "&ClassName=%CD%F8%C2%E7%B4%F3%B5%E7%D3%B0%BE%E7%B1%BE&ClassName2=&byType="

# 网剧剧本
# YOUTH_PAGE = "https://www.bianju.me/NetTelescript/"
# PAGE_URL_END = "&ClassName=%CD%F8%C2%E7%BE%E7%BE%E7%B1%BE&ClassName2=&byType="

# 微电影剧本
# YOUTH_PAGE = "https://www.bianju.me/MicroFilm/"
# PAGE_URL_END ="&ClassName=%CE%A2%B5%E7%D3%B0%BE%E7%B1%BE&ClassName2=&byType="

# 小说
# YOUTH_PAGE = "https://www.bianju.me/novel/"
# PAGE_URL_END ="&ClassName=С˵&ClassName2=&byType="

# 其它
# YOUTH_PAGE = "https://www.bianju.me/other/"
# PAGE_URL_END ="&ClassName=%C6%E4%CB%FB&ClassName2=&byType="


PAGE_URL_START = "https://www.bianju.me/telescript/?Page="
PRODUCT_URL_START = "http://www.bianju.me/"
PRODUCT_URL_END = "&CType=content"

SPIDER_NAME = "cnbianjuTest"

LOGIN_PAGE = "https://www.bianju.me/user_login.asp"

# ElasticSearch
# HOST_PORT = 'spark3:9200'
HOST_PORT = 'ubuntu3:9200'

# ElasticSearch index
# SCRIPT_INDEX = "script_data"
# SCRIPT_TYPE = "script"
# SCRIPT_INDEX = "telescript_data"
# SCRIPT_TYPE = "telescript"
SCRIPT_INDEX = "screenplay_data"
SCRIPT_TYPE = "screenplay"


def get_url_product_id(url):
    urla = url.split("?")
    res = parse.parse_qs(urla[1])
    return res['id'][0]


def get_url_product_page(url):
    urla = url.split("?")
    res = parse.parse_qs(urla[1])
    return res['page'][0]


def get_md5(url):
    if isinstance(url, str):
        url = url.encode()
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def format_url(url):
    """
    返回处理后的url
    :param url: //new.qq.com/omn/20180511/20180511A08NHD.html
    :return: http://new.qq.com/omn/20180511/20180511A08NHD.html
    """
    if url.startswith("//"):
        return "http:" + url


def get_now_time():
    """
    返回形如2018-05-03 09:33:00的日期
    :return: 返回当前时间
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_system():
    """
    获取当前系统
    :return:  Windows\Linux\Other System
    """
    sys_str = platform.system()
    if sys_str == "Windows":
        return "Windows"
    elif sys_str == "Linux":
        return "Linux"
    else:
        return "Other System"


def get_file_system_path():
    """
    获取爬虫持久化路径
    :return: 当前系统路径
    """
    linux_path = "/home/hadoop/news/"
    windows_path = "E://news//"
    path = windows_path if get_system() == "Windows" else linux_path
    return path


def get_comment_file_system_path():
    """
    获取评论爬虫持久化路径
    :return: 当前系统路径
    """
    linux_path = "/home/hadoop/comment/"
    windows_path = "E://comment//"
    path = windows_path if get_system() == "Windows" else linux_path
    return path


def get_chrome_executable_path():
    linux_path = "/usr/bin/chromedriver"
    windows_path = "E://Program//chromedriver.exe"
    path = windows_path if get_system() == "Windows" else linux_path
    return path


def get_now_date():
    """
    返回形如2018-05-03的日期
    :return: 返回当前时间
    """
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def chrome_option():
    """
    设置 chrome option
    :return:  chrome option
    """
    global options
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)

    # 设置为无界面浏览器
    options.set_headless()
    options.add_argument(get_user_agent())
    return options


def debug_option():
    """
    设置 chrome option
    :return:  chrome option
    """
    global options
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2
        }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument(get_user_agent())
    return options


def get_user_password():
    """"
    随机获取用户名、密码
    """
    user_passwords = {"hkhai": "hk85151918", "jeesite": "123456", "amy26": "13579", "xxxx11": "xxxx11"}
    user = random.choice(list(user_passwords))
    user_tuple = (user, user_passwords[user])
    return user_tuple


def get_user_agent():
    """"
    随机获取HTTP_User_Agent
    """
    user_agents = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    user_agent = random.choice(user_agents)
    return user_agent


def remove_special_label(s):
    """
    去除html中的不必要字符
    :param s: html网页
    :return: 处理后的html网页
    """
    re = s.replace(u'\u3000', u'').replace('\r', '').replace('\n', '').replace('\t', '')
    return re


def get_pre_week():
    """
    获取上周日期
    :return:  字符串格式日期
    """
    today = datetime.date.today()
    one_week = datetime.timedelta(days=7)
    pre_week = today - one_week
    return pre_week.__str__()


def get_pre_week_url_list():
    """
    读取文件并解析为列表
    :return: url列表
    """
    pre_week = get_pre_week()
    json_file = get_file_system_path() + pre_week
    dic_list = [json.loads(line)["url"] for line in open(json_file)]
    return dic_list
