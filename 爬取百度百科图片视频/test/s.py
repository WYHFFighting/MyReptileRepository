import json
import pprint
import requests

# json 字符串
# employee_string = '{"first_name": "Michael", "last_name": "Rodgers", "department": "Marketing"}'
#
# # type 检查对象类型
# print(type(employee_string))
#
# # 字符串转为对象
# json_object = json.loads(employee_string)
# pprint.pprint(json_object)
#
# # 检测类型
# print(type(json_object))
#
# # 输出
# # <class 'dict'>

# url = "https://baike.baidu.com/item/%E6%B1%9F%E8%8B%8F%E7%9C%81/320938?fromtitle=%E6%B1%9F%E8%8B%8F&fromid=154268"
url = "https://baike.baidu.com/api/second/video/list?secondId=74983221&lemmaId=8763158&isSensitive=0&scene=pc"
html = requests.get(url).text
text = html.encode("utf-8").decode("unicode_escape")
# jsonStr = '{}'.format(html)
# print(type(html))
# with open("test2.txt", "w+", encoding="utf-8") as fw:
#     fw.write(html)
# print(html)
js = json.loads(text, strict = False)
pprint.pprint(js)


