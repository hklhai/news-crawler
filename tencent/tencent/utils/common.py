import hashlib
import time
import platform


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


def get_now_date():
    """
    返回形如2018-05-03的日期
    :return: 返回当前时间
    """
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))