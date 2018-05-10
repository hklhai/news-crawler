# -*- coding: utf-8 -*-

def format_url(url):
    if url.startswith("//"):
        return "http:" + url
