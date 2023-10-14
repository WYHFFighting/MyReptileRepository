import os
import requests
from bs4 import BeautifulSoup
import re
import webbrowser
import time
from vfc import open_url
from config import headers


# 递归得到文件
def recursive_listdir(path):
    book = []
    name = []
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        book.append(file_path)
        name.append(file)
    return book


def set_url(path):
    first_catlog = recursive_listdir(path)
    # print(len(first_catlog))
    for fir in first_catlog:
        second_catlog = recursive_listdir(fir)
        for sec in second_catlog:
            print(sec)
        # print(second_catlog)
    return None
    second_catlog = []
    for fir in first_catlog:
        second_catlog.append(fir)
def get_url(item):
    url = "https://baike.baidu.com/item/" + item
    responese = requests.get(url = url, headers = headers)
    # with open("test.txt", "w+", encoding = "utf-8") as f:
    #     f.write(responese.text)
    # print(responese.text)
    # print(type(responese.text))
    # :"https:\/\/baikevideo.cdn.bcebos.com\/media\/mda-Xt7KVGwqTr85eado\/cf857958d287ca7878781513a1bbaee1.mp4"
    # "playUrl":{"mp4":"
    # html_data = re.findall(r"\"mp4\":\"(https:.+?\.mp4)\"", responese.text)  # 18
    # html_data = re.findall(r"\"h265Mp4\":\"(https:.+?\.mp4)\"", responese.text)  # 6
    # html_data = re.findall(r"\"playMp4Url\":\"(https:.+?\.mp4)\"", responese.text)  # 6
    # print(len(html_data))
    # print(html_data)


    save_path = f"text/{item}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # item = "mp4"
    html_data = re.findall(r"\"mp4\":\"(https:.+?\.mp4)\"", responese.text)  # 18
    # print(len(html_data))
    with open(f"text/{item}/mp4.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            f.write(d + "\n")
            # print(d)
        # webbrowser.open(d)

    html_data = re.findall(r"\"h265Mp4\":\"(https:.+?\.mp4)\"", responese.text)  # 6
    # print(len(html_data))
    with open(f"text/{item}/h265Mp4.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            f.write(d + "\n")
            # print(d)
        # webbrowser.open(d)

    html_data = re.findall(r"\"playMp4Url\":\"(https:.+?\.mp4)\"", responese.text)  # 6
    # print(len(html_data))
    with open(f"text/{item}/playMp4Url.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            f.write(d + "\n")
            # print(d)
        # webbrowser.open(d)

    # https:\/\/baikevideo.cdn.bcebos.com\/media\/mda-OxO1nmeZEwxyMv5u\/6fabc7702e4bdaa38657f4b1fb779b2d.m3u8","playMp4Url":"https:\/\/baikevideo.cdn.bcebos.com\/media\/mda-OxO1nmeZEwxyMv5u\/04ad8dbb608e9f1e87500a0910f1e2dd.mp4
    html_data = re.findall(r"\"playUrl\":\"(https:.+?\.mp4)\"", responese.text)  # 6
    renew = []
    with open(f"text/{item}/playUrl.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            if "," in d:
                continue
            renew.append(d)
            f.write(d + "\n")
            # print(d)
        # webbrowser.open(d)
    # print(len(renew))


if __name__ == "__main__":
    # set_url(path="../link")
    # get_url()
    pass

