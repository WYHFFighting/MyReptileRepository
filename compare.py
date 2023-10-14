import re


def ptn(html):
    html_data = re.findall(r"\"mp4\":\"(https:.+?\.mp4)\"", html.text)  # 18
    html_data = re.findall(r"\"h265Mp4\":\"(https:.+?\.mp4)\"", html.text)  # 6
    html_data = re.findall(r"\"playMp4Url\":\"(https:.+?\.mp4)\"", html.text)  # 6
    # https:\/\/baikevideo.cdn.bcebos.com\/media\/mda-OxO1nmeZEwxyMv5u\/6fabc7702e4bdaa38657f4b1fb779b2d.m3u8","playMp4Url":"https:\/\/baikevideo.cdn.bcebos.com\/media\/mda-OxO1nmeZEwxyMv5u\/04ad8dbb608e9f1e87500a0910f1e2dd.mp4
    html_data = re.findall(r"\"playUrl\":\"(https:.+?\.mp4)\"", html.text)  # 6
