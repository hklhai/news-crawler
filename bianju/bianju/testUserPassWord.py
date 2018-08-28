# -*- coding: utf-8 -*-

# user_passwords = {"hkhai": "hk85151918", "jeesite": "123456", "amy26": "13579"}
# user = random.choice(list(user_passwords))
# print(user + " " + user_passwords[user])
from bianju.common import get_user_password

tuple = get_user_password()
print(tuple[0], tuple[1])
