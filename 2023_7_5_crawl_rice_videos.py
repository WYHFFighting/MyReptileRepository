import re
import vfc
import requests
from config import headers
import os
from bs4 import BeautifulSoup

# def run():
#     link


def run(url, base_link, save_path):
    html = vfc.open_url(url, headers, None)
    if not html:
        print(url, "#html data get errer#")
        with open("rice_videos_log/html_get_problem.txt", "a+", encoding = "utf-8") as fw:
            fw.write(url + "\n")
        return None

    soup = BeautifulSoup(html.text, "lxml")
    content = soup.find("ul", {"class": "list clear"})
    links = content.find_all("a")
    for l in links:
        link_prefix = l.get('href')
        overall_link = base_link + link_prefix
        name = l.find("p").text
        video_content = vfc.get_content(overall_link, headers)
        if not video_content:
            print(url, "#video content get errer#")
            with open("rice_videos_log/video_content_get_problem.txt", "a+", encoding = "utf-8") as fw:
                fw.write(overall_link + "\n")
            continue
        print("------------------{}爬取中---------------------------".format(name))
        print(url, "downloading...")
        with open(os.path.join(save_path, f'{name}.mp4'), mode = "ab") as f:
            f.write(video_content)
        print(f"{name}", "success!")



if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    base_link = "https://v.ahnw.cn"
    for i in range(2, 7):
        link = f"https://v.ahnw.cn/Home/Search?page={i}&key=%E6%B0%B4%E7%A8%BB"
        run(link, base_link, "./data/rice_videos_new")
