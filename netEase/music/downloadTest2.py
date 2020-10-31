# -*- coding: utf-8 -*-
import re
import time

import requests

from netEase.music.common import get_user_agent

headers = {
    "User-Agent": get_user_agent(),
}

session = requests.session()
res = session.get(url="http://music.163.com/song/media/outer/url?id=1365221826.mp3", headers=headers)
chunk_size = 1024
fileName = re.sub('[\/:*?"<>|]', '-', "a.mp3")
with open(fileName, 'wb') as f:
    for data in res.iter_content(chunk_size=chunk_size):
        f.write(data)
