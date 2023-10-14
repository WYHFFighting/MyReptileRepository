import os
import requests
from bs4 import BeautifulSoup
import re
from learn import get_url
from text.merge_url import merge
from text.deduplicate import ded
import multiprocessing as mp
import sys
import time
import vfc
from config import headers


# def open_url(url, header):
#     while True:
#         try:
#             html = requests.get(url = url, headers = header)
#             break
#         except:
#             print("---------------------open url sleep---------------------")
#             time.sleep(0.1)
#
#     return html


# def crawl(url, header):
#     html = vfc.open_url(url, header)
#     try:
#         content = html.content
#     except:
#         print(url, "###get content error###")
#         return None

    # return content


def crawl_video(get_path, header, item, save_path):
    with open(get_path, "r+", encoding = "utf-8") as f:
        urlss = f.read().split()

    id = 1
    print("**********************{}开始爬取***********************".format(item))
    # print(item)
    for url in urlss:
        video_content = vfc.get_content(url, header)
        if not video_content:
            continue
        print("------------------{}爬取中---------------------------".format(item))
        print(url, "downloading...")

        with open(os.path.join(save_path, f'{id}.mp4'), mode = 'ab') as f:
                f.write(video_content)
        print(f"{item}", id, "success!")
        id += 1


def improve_crawl_videos(urlss, video_names, item, save_path, l):
    print("**********************{}开始爬取***********************".format(item))
    for i in range(len(urlss)):
        url = urlss[i]
        title = video_names[i]
        title = re.sub(r"[\\/:*?\"<>|]", " ", title)
        title = re.sub(r"\n", " ", title)
        video_content = vfc.get_content(url, headers)
        if not video_content:
            continue
        print("-----{}-{}爬取中-----\n".format(item, title), url, "downloading...")

        try:
            with open(os.path.join(save_path, f'{title}.mp4'), mode='wb') as f:
                f.write(video_content)
                print(f"-----{item}-{title}-----", "success!")
        except:
                with open("log/load_video_problem.txt", "a+", encoding="utf-8") as fw:
                    fw.write(url + "\t" + item + "\t" + title + "\n")
                print(f"#####{item}-{title}#####", "failed!")




# 执行
def sequential(c, level):
    if c == "":
        return None
    url, save_path = c.split("\t")
    save_path = re.sub("data", "data2", save_path)
    addition = re.search(r"\\(.+?)\\(.+?)\\", save_path)[2]
    # addition = "省"

    # 获取视频链接，标题
    videos, title = vfc.pre_video_urls(url, save_path, headers, addition, level)

    if videos:
        save_path = os.path.join(save_path, f"{title}")
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        # save_path: ./data\县\云南省\临沧市
        crawl_video(videos, headers, title, save_path)

    return 1


def improve_sequential(c, level, l = None):
    if c == "":
        return None
    url, save_path = c.split("\t")
    save_path = re.sub("data", "data2", save_path)
    # addition = re.search(r"/{}/(.+?)/".format(level), save_path)[1]
    # ./data/县/云南省/临沧市
    addition = "省"

    vfc.fcatalogue(url, addition, l)
    # 获取视频链接，标题
    # title, videos, video_names = vfc.pre_video_urls(url, save_path, addition, level, l)
    #
    # if videos:
    #     save_path = os.path.join(save_path, f"{title}")
    #     if not os.path.exists(save_path):
    #         os.makedirs(save_path)
    #
    #     # save_path: ./data\县\云南省\临沧市
    #     improve_crawl_videos(videos, video_names, title, save_path, l)

    return 1


if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()

    # level_lists = ["县", "县级市", "地区", "地级市", "市辖区", "旗", "林区", "特区", "盟", "自治县", "自治州", "自治旗"]
    # level_lists = ["旗", "林区", "特区", "盟", "自治县", "自治州", "自治旗"]
    # level_lists = ["省"]

    # pool = mp.Pool(20)
    # for level in level_lists:
    #     with open(f"../finished_links/{level}", "r+", encoding = "utf-8") as fr:
    #         couples = fr.read().split("\n")

        # 多进程
        # 指定pool进程数
        # 注意函数里要更改addition
        # res = [pool.apply_async(sequential, args = (c, level)) for c in couples]
        # [j.get() for j in res]

        # 单进程
        # for c in couples:
        #     # c = "https://baike.baidu.com/item/%E4%BA%91%E5%8E%BF?fromModule=lemma_search-box\t./data\县\云南省\临沧市"
        #     c = "https://baike.baidu.com/item/%E4%BA%91%E5%8E%BF/61451344?fromModule=lemma-qiyi_sense-lemma\t./data\县\云南省\临沧市"
        #     sequential(c)
        #     break

    # 单独爬
    # c = "https://baike.baidu.com/item/%E9%94%99%E9%82%A3%E5%B8%82/62848294	./data\县级市\西藏自治区\山南市"
    # sequential(c, "县级市")

    # 爬特定链接
    # with open("log/no_videos_log.txt", "r+", encoding="utf-8") as fr:
    #     url_lists = fr.read().split()

    # improve try
    # level_lists = ["县", "县级市", "地区", "地级市", "市辖区", "旗", "林区", "特区", "盟", "自治县", "自治州", "自治旗"]
    # level_lists = ["县", "县级市", "地区", "地级市", "市辖区", "旗", "林区", "特区", "盟", "自治县", "自治州", "自治旗"]
    level_lists = ["pro"]

    pool = mp.Pool(36)
    l = mp.Manager().Lock()
    for level in level_lists:
        with open(f"../finished_links/{level}", "r+", encoding = "utf-8") as fr:
            couples = fr.read().split("\n")

        # 多进程
        # 指定pool进程数
        # 注意函数里要更改addition
        # c = "https://baike.baidu.com/item/%E5%87%A4%E5%BA%86%E5%8E%BF?fromModule=lemma_search-box\t./test/县/云南省/临沧市"
        # improve_sequential(c, level, None)
        # exit()
        res = [pool.apply_async(improve_sequential, args = (c, level, l)) for c in couples]
        [j.get() for j in res]


