# -*- coding: utf-8 -*-

# user_passwords = {"hkhai": "hk85151918", "jeesite": "123456", "amy26": "13579"}
# user = random.choice(list(user_passwords))
# print(user + " " + user_passwords[user])
from bianju.common import get_user_password, get_url_product_id

tuple = get_user_password()
print(tuple[0], tuple[1])

url = "https://www.bianju.me/Art_list.asp?id=17167&page=6&CType=content"
print(get_url_product_id(url))

a = 7
for i in range(a-1, -1, -1):
    print(i)
