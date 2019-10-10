# -*- coding: utf-8 -*-
from operator import itemgetter
from itertools import groupby

d1 = {'name': 'zhangsan', 'age': 20, 'country': 'China'}
d2 = {'name': 'wangwu', 'age': 20, 'country': 'USA'}
d3 = {'name': 'lisi', 'age': 22, 'country': 'JP'}
d4 = {'name': 'zhaoliu', 'age': 22, 'country': 'USA'}
d5 = {'name': 'pengqi', 'age': 22, 'country': 'USA'}
d6 = {'name': 'lijiu', 'age': 22, 'country': 'China'}
lst = [d1, d2, d3, d4, d5, d6]
lst.sort(key=itemgetter('age'))
lstg = groupby(lst, itemgetter('age'))

# for key, group in lstg:
#     for g in group:  # group是一个迭代器，包含了所有的分组列表
#         print(key, g)

print(dict([(key, list(group)) for key, group in lstg]))
