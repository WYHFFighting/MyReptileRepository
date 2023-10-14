import requests
from bs4 import BeautifulSoup
import regex as re
import time
import os
from config import headers
import pprint
import json
from regular import ptn_del_sqr_bkt


def write_log(path, cont, mode):
    with open(path, mode = mode, encoding="utf-8") as f:
        f.write(cont + "\n")

# 打开链接
def open_url(url, headers, where, proxies = False):
    requests.packages.urllib3.disable_warnings()
    max_try = 200
    now_try = 0
    output_sign = False
    while True:
        try:
            if proxies:
                html = requests.get(url = url, headers = headers, verify=False, timeout=(50, 50), proxies = proxies)
            else:
                html = requests.get(url, verify = False, timeout = (50, 50), headers = headers)
            break
        except:
            now_try += 1
            if not os.path.exists("./log"):
                os.makedirs("./log")
            if not re.search("^http", url):
                write_log("./log/wrong_urls.txt", url, "a+")
                return None
            if now_try > max_try:
                print(url, "url opening attempts exceeded the maximum error")
                write_log("./log/open_url_problem_log.txt", url, "a+")
                return None
            if not output_sign:
                print(url, "-----{} open url sleep-----".format(where))
                output_sign = True
            time.sleep(0.1)

    return html


# 判断链接是否正确打开
def html_get(url, html):
    if not html:
        print(url, "#html data get errer#")
        with open("./log/html_get_problem_log2.txt", "a+", encoding ="utf-8") as fw:
            fw.write(url + "\n")
        return False
    return True


# 获取页面数据
def get_content(url, header, proxies):
    html = open_url(url, header, "func: get_content", proxies)
    if not html_get(url, html):
        return None
    try:
        content = html.content
    except:
        if not os.path.exists("./log"):
            os.makedirs("./log")
        print(url, "#get content error#")
        with open("./log/content_get_problem_log.txt", "a+", encoding ="utf-8") as fw:
            fw.write(url +"\n")
        return None

    return content


# 判断是否是多义词
def judge_multiple_meaning(soup):
    sign = soup.find("div", {"class": "lemmaWgt-subLemmaListTitle"})
    if sign != None:
        # print(sign.text)
        if "这是一个多义词" in sign.text:
            return True
    return False


# 判断是否进入验证界面
def judge_verification(soup, header = None):
    try:
        soup.find("h1").text
        return False
    except:
        return True


# 跳过百度的验证码界面
def pass_verification(url, header, proxies):
    html = open_url(url, header, "func: pass_verification", proxies)
    if not html_get(url, html):
        return None, None
    soup = BeautifulSoup(html.text, "lxml")
    while True:
        try:
            soup.find("h1").text
            break
        except:
            time.sleep(0.5)
            print("-----pass verification sleep-----")
            html = open_url(url, header, "func: pass_verification", proxies)
            soup = BeautifulSoup(html.text, "lxml")

    return html, soup


# 处理中转页面
def deal_transfer_page(soup, addition, sign):
    base_url = "https://baike.baidu.com"
    # 是否要进行二次正则
    if sign:
        try:
            std = re.search(r"\\(.+)（", addition)[1]
        except:
            std = re.search(r"\\(.+)\(", addition)[1]
    else:
        std = addition

    data = soup.find_all("li", {"class": "list-dot list-dot-paddingleft"})
    for item in data:
        cs = item.find_all("a")
        for c in cs:
            if std in c.text:
                return base_url + c.get("href")

    return False


# 获取视频下载链接
def get_video_url(html, title, level):
    save_path = f"video_text/{level}/{title}"
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # item = "mp4"
    html_data = re.findall(r"\"mp4\":\"(https:.+?\.mp4)\"", html.text)  # 18
    # print(len(html_data))
    with open(f"video_text/{level}/{title}/mp4.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            f.write(d + "\n")
            # print(d)
        # webbrowser.open(d)

    html_data = re.findall(r"\"h265Mp4\":\"(https:.+?\.mp4)\"", html.text)  # 6
    # print(len(html_data))
    with open(f"video_text/{level}/{title}/h265Mp4.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            f.write(d + "\n")
            # print(d)
        # webbrowser.open(d)

    html_data = re.findall(r"\"playMp4Url\":\"(https:.+?\.mp4)\"", html.text)  # 6
    # print(len(html_data))
    with open(f"video_text/{level}/{title}/playMp4Url.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            f.write(d + "\n")
            # print(d)
        # webbrowser.open(d)

    # https:\/\/baikevideo.cdn.bcebos.com\/media\/mda-OxO1nmeZEwxyMv5u\/6fabc7702e4bdaa38657f4b1fb779b2d.m3u8","playMp4Url":"https:\/\/baikevideo.cdn.bcebos.com\/media\/mda-OxO1nmeZEwxyMv5u\/04ad8dbb608e9f1e87500a0910f1e2dd.mp4
    html_data = re.findall(r"\"playUrl\":\"(https:.+?\.mp4)\"", html.text)  # 6
    renew = []
    with open(f"video_text/{level}/{title}/playUrl.txt", "w+", encoding = "utf-8") as f:
        for d in html_data:
            if "," in d:
                continue
            renew.append(d)
            f.write(d + "\n")
            # print(d)

    return save_path
        # webbrowser.open(d)
    # print(len(renew))

# 合并得到的所有视频下载链接
def merge(path):
    txts = os.listdir(path)
    save_file = "total"
    with open(os.path.join(path, save_file), "w+", encoding = "utf-8") as ft:
        for t in txts:
            with open(os.path.join(path, t), "r+", encoding = "utf-8") as fr:
                urls = fr.read().split()
            for l in urls:
                ft.write(l + "\n")
    return save_file


# 去除重复的视频下载链接
def ded(path, prefix):
    # sys.path.append(f"./")
    clean_data = set()
    # print(sys.path)
    with open(os.path.join(path, prefix), "r+", encoding = "utf-8") as f:
        url_lists = f.read().split()
    for url in url_lists:
        clean_data.add(url)

    save_file = "clean_data"
    with open(os.path.join(path, save_file), "w+", encoding = "utf-8") as f:
        for i in range(len(clean_data)):
            d = clean_data.pop()
            # print(d)
            d = re.sub(r"\\", "", d)
            # print(d)
            # break
            f.write(d + "\n")
    return os.path.join(path, save_file)

def improve_get_video_url(url, html):
    html = html.text
    try:
        lemmaid = re.search(r"data-lemmaid=\"(\d+)\"", html)[1]
        # print(lemmaid)
        filterID = re.search(r"secondId\":(\d+)", html)[1]
    except:
        write_log("log/getID_problem", url)
        return None, None
    # print(filterID)
    vum = "https://baike.baidu.com/api/second/video/list?secondId={}&lemmaId={}&isSensitive=0&scene=pc".format(filterID, lemmaid)
    # vum = "https://baike.baidu.com/api/second/video/list?lemmaId={}&isSensitive=0&scene=pc_top&filterId={}&rn=12".format(lemmaid, filterID)
    html = open_url(vum, headers, "improve_get_video_url")
    if not html_get(url, html):
        return None, None

    text = html.text.encode("utf-8").decode("unicode_escape")
    json_get_flag = False
    try:
        json_data = json.loads(text, strict = False)
        json_get_flag = True
    except:
        pass
        # write_log("log/json_get_problem.txt", vum + "\t" + url, "a+")
        # return None, None
    if not json_get_flag:
        try:
            json_data = json.loads(html.text, strict = False)
        except:
            write_log("log/json_get_problem.txt", vum + "\t" + url, "a+")
            return None, None

    # pprint.pprint(json_data)
    video_data = json_data['data']['list']
    video_urls = []
    video_names = []
    for item in video_data:
        # print("**********************************************")
        # pprint.pprint(item)
        item = item['content']
        url_source = item['playUrl']['mp4']
        title = item['title']
        # print(title, url_source)
        video_urls.append(url_source)
        video_names.append(title)

    return video_urls, video_names



# 准备视频下载链接
def pre_video_urls(url, save_path, addtion, level, l):
    print("*********************************************\n", url, "start open.....")
    base_url = "https://baike.baidu.com"
    error_count = 0

    html = open_url(url, headers, "func: pre_video_urls")
    if not html_get(url, html):
        return None, None, None
    soup = BeautifulSoup(html.text, "lxml")
    # 跳过验证界面
    times = 0
    while True:
        try:
            times += 1
            title = soup.find("h1").text
            break
        except:
            time.sleep(0.3)
            print(url, times, "--pass verification sleep--")
            html = open_url(url, headers, "loop: pass_verification")
            soup = BeautifulSoup(html.text, "lxml")

    transfer_flag = judge_multiple_meaning(soup)
    if transfer_flag:
        # 页面中转情况
        print("#################################################################\n", url, "transfer!", "\n#################################################################")
        transfer_condition = deal_transfer_page(soup, addtion, False)
        if transfer_condition == False:
            print("transfer error!!!!!")
            with open("log/transfer_problem_log.txt", "a+", encoding ="utf-8") as f:
                f.write(url + "\n")
            return None, None, None
        else:
            pre_video_urls(transfer_condition, save_path, headers, addtion, level)
            return None, None, None

    # 没有秒懂百科视频的情况
    video_sign = soup.find("img", {"class": "miaodong-logo"})
    if video_sign == None:
        print(url, "not have videos")
        with open("log/no_videos_log.txt", "a+", encoding ="utf-8") as f:
            f.write(url + "\t" + save_path + "\n")
        return None, None, None

    video_urls, video_names = improve_get_video_url(url, html)
    # video_save_path = get_video_url(html, title, level)
    # prefix = merge(video_save_path)
    # video_urls = ded(video_save_path, prefix)

    return title, video_urls, video_names


def delete_illegal_named_symbol(sur):
    sur = re.sub(r"[\\/:*?\"<>|]", " ", sur)
    sur = re.sub(r"\n", " ", sur)
    return sur

def fcatalogue(url, addtion, lock):
    print("*********************************************\n", url, "start open.....")
    base_url = "https://baike.baidu.com"
    error_count = 0

    html = open_url(url, headers, "func: pre_video_urls")
    if not html_get(url, html):
        return None, None, None
    soup = BeautifulSoup(html.text, "lxml")
    # 跳过验证界面
    times = 0
    while True:
        try:
            times += 1
            title = soup.find("h1").text
            break
        except:
            time.sleep(0.3)
            print(url, times, "--pass verification sleep--")
            html = open_url(url, headers, "loop: pass_verification")
            soup = BeautifulSoup(html.text, "lxml")

    transfer_flag = judge_multiple_meaning(soup)
    if transfer_flag:
        # 页面中转情况
        print("#################################################################\n", url, "transfer!",
              "\n#################################################################")
        transfer_condition = deal_transfer_page(soup, addtion, False)
        if transfer_condition == False:
            print("transfer error!!!!!")
            with open("log/transfer_problem_log.txt", "a+", encoding="utf-8") as f:
                f.write(url + "\n")
            return
        else:
            fcatalogue(transfer_condition, addtion, lock)
            return
    try:
        second_title = soup.find("div", {"class": "lemma-desc"}).text
    except:
        print("###find second_title error###", title, url)
        write_log("log2/find_second_title_problem.txt", title + "\n" + url, "a+")
        return
    content = soup.find("div", {"class": "catalog-list column-4"})
    try:
        content = content.find_all("ol")
    except:
        print("###find ol error###", second_title + title, url)
        write_log("log2/find_ol_problem.txt", second_title + title + "\n" + url, "a+")
        return
    cas = []
    for ol in content:
        li = ol.find_all("li", {"class": "level1"})
        for sc in li:
            c = sc.find("span", {"class": "text"})
            cas.append(c.text)

    # 设置正则匹配模式
    def pattern(s):
        return f"{title}{s}\n编辑\n\n播报"

    end = "词条图册\n\n更多图册"
    tx = soup.text.replace(u"\xa0", "")
    tx = ptn_del_sqr_bkt.sub("", tx)
    # print(tx)

    for i in range(len(cas)):
        if i == len(cas) - 1:
            sp = pattern(cas[i]) + "(.+?)" + end
            ptn = re.compile(r"%s" % sp, flags = re.S)
            try:
                res = ptn.search(tx)[1]
            except:
                print("###get_content_error### {}-{}".format(second_title, title), url)
                write_log("log2/get_content_problem.txt", url + "\t" + second_title + title, "a+")
                return
        else:
            sp = pattern(cas[i]) + "(.+?)" + pattern(cas[i + 1])
            ptn = re.compile(r"%s" % sp, flags = re.S)
            # ptn = re.compile(r'河北省历史沿革\n编辑\n\n播报.*河北省行政区划\n编辑\n\n播报')
            # ptn = re.compile(r'河北省历史沿革\n编辑\n\n播报(.+)河北省行政区划\n编辑\n\n播报')
            try:
                res = ptn.search(tx)[1]
            except:
                print("###get_content_error### {}-{}".format(second_title, title), url)
                write_log("log2/get_content_problem.txt", url + "\t" + second_title + title, "a+")
                return
        res = re.sub("\s", " ", res)
        name = second_title + title
        name = delete_illegal_named_symbol(name)
        lock.acquire()
        try:
            with open(f"./data3/cata/{cas[i]}.tsv", "a+", encoding = "utf-8") as f:
                f.write(name + "\t" + cas[i] + "\t" + res + "\n")
        except:
            print("###write_content_error### {}-{}".format(second_title, title), url)
            write_log("log2/write_content_problem.txt", url + "\t" + second_title + title, "a+")
            # print(second_title + title, "success!")
        lock.release()


if __name__ == "__main__":
    # url = "https://baike.baidu.com/item/%E5%A7%9C%E7%BB%B4?force=1"
    # url = "https://baike.baidu.com/item/%E5%A7%9C%E7%BB%B4/8901?fromModule=lemma-qiyi_sense-lemma"
    # html = open_url(url, header)
    # soup = BeautifulSoup(html.text, "lxml")
    # print(judge_multiple_meaning(soup))

    # level = "县"
    # with open(f"../finished_links/{level}", "r+", encoding = "utf-8") as fr:
    #     couples = fr.read().split("\n")
    #     # print(couples)
    #     for c in couples:
    #         if c == "":
    #             continue
    #         url, save_path = c.split("\t")
    #         # save_path = re.sub("", "/", save_path)
    #         addition = re.search(r"\\(.+?)\\(.+?)\\", save_path)[2]
    #         # print(save_path, addition)
    #         print(url, save_path)
    #         videos = pre_video_urls(url, save_path, header, addition, level)
    #         print(videos)
    #         break

    # import multiprocessing as mp
    #
    # l = mp.Lock()
    # url = "https://baike.baidu.com/item/%E6%B8%85%E9%95%87%E5%B8%82"
    # html = requests.get(url)
    # title = "清镇市"
    # level = "市"
    # video_urls = improve_get_video_url(html, title, level, l)
    # print("---------------------")
    # print(video_urls)
    pass
    # fcatalogue("https://baike.baidu.com/item/%E9%A9%AC%E9%9E%8D%E5%B1%B1%E5%B8%82?fromModule=lemma_search-box", "")