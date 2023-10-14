import requests
from bs4 import BeautifulSoup
import pprint
import json
import os


# url = "https://baike.baidu.com/api/second/video/list?secondId=73919237&lastId=25363791&lemmaId=320938&isSensitive=0&scene=pc"
#
# html = requests.get(url).text
# # print(html)
# html = html.encode("utf-8").decode("unicode_escape")
# js = json.loads(html, strict = False)
# pprint.pprint(js)

with open("test.txt", "r+") as fr:
    text = fr.read()

js = json.loads(text)
pprint.pprint(js)


import re
# name = '时\间<>的?沉:香 滇红/的故乡|美*名：凤庆""县'
# # name = '时间的沉香 滇红的故乡美名：凤庆县'
# name = re.sub(r"[\\/:*?\"<>|]", " ", name)
# print(name)
# path = './县/云南省/临沧市\\凤庆县'
# res = os.path.join(path, name + ".txt")
# with open(res, "w+") as f:
#     f.write("hello world")
# print(res)
# with open(r"E:\wyh\reptile\video\finished_links\省", "r+", encoding="utf-8") as fr:
#     pros = fr.read().split()
# with open("pro", "w+", encoding="utf-8") as fw:
#     for p in pros:
#         fw.write(p + "\t" + "./data2/省级行政区/\n")


