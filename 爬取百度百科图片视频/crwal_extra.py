import requests
from bs4 import BeautifulSoup
import regex as re
import vfc
from config import headers, match_mp4
import json
import pprint



if __name__ == "__main__":
    # url = "https://baike.baidu.com/item/%E6%96%B0%E6%B3%B0%E5%B8%82"
    # html = vfc.open_url(url, headers).text
    # id = re.search(r"lemmaId=\"(\d+?)\".+", html)
    # print(id[1])
    suburl = "https://baike.baidu.com/api/second/video/list?lemmaId=126069&isSensitive=0&scene=pc_top&filterId=73536065&rn=12"
    html = vfc.open_url(suburl, headers).text
    html = html.encode("utf-8").decode("unicode_escape")
    # print(html)
    data = json.loads(html, strict=False)
    data = data['data']['list']
    print(len(data))
    for item in data:
        pprint.pprint(item)
        break
    # title = data['title']
    # url = data['playUrl']['mp4']
    # print(title)
    # print(url)
    # pprint.pprint(data)
    exit()
    soup = BeautifulSoup(html, "lxml")

    name = soup.find("h1").text
    print(html)
    exit()
    title = soup.find("div", {"class": "second-video-item-title position-video-bottom"})
    try:
        title = title.text
    except:
        print(url, "no extra videos")
        with open("backups/log/no_extravs.txt", "w+", encoding="utf-8") as fw:
            fw.write(url + "\t" + name + "\n")

    video_links = match_mp4.findall(html)
    one = video_links[0]
    print(one)