import sys

from bs4 import BeautifulSoup
import requests
import re
# from decorators import access_url
# from regular_expression import ptn_del_sqr_bkt
import time
import os


def open_url(url):
    requests.packages.urllib3.disable_warnings()
    while True :
        try:
            html = requests.get(url, verify = False)
            break
        except:
            time.sleep(1)
            print("-----sleep-----")
    html.encoding = "utf-8"
    soup = BeautifulSoup(html.text, "lxml")

    return soup



def find_intro(url, path):
    soup = open_url(url)

    title = soup.find("h1").text

    content = soup.find("div", {"class": "lemma-summary J-summary", "label-module": "lemmaSummary"})
    content = content.text
    content = ptn_del_sqr_bkt.sub("", content)
    content = content.replace(u"\xa0", "")
    content = "".join(re.split("\s", content))

    with open(path, "a+", encoding = "utf-8") as f:
        f.write(title + "\t" + content + "\n")

    return title, content


def ftable(url):
    soup = open_url(url)

    # content = soup.find("div", {"class": "basic-info J-basic-info cmn-clearfix"})
    # if content == None:

    label = soup.find_all("dt", {"class": "basicInfo-item name"})
    labels = [re.sub("\s", "", x.text) for x in label]
    # labels = [x.text.replace("\xa0", "") for x in label]

    # content = soup.find("dl", {"class": "basicInfo-block basicInfo-right"})
    # label = content.find_all("dt", {"class": "basicInfo-item name"})
    # for item in label:
    #     text = item.text
    #     v = ptn_del_sqr_bkt.sub("", text)
    #     v = re.sub('\s', "", v)
    #     labels.append(v)
    # print(labels)
    ct = soup.find_all("dd", {"class": "basicInfo-item value"})
    values = []
    for item in ct:
        text = item.text
        v = ptn_del_sqr_bkt.sub("", text)
        v = re.sub('\s', "", v)
        values.append(v)

    return labels, values
    # content = ptn_del_sqr_bkt.sub("", content.text).replace(u"\xa0", "")
    # content = content.replace("\n", " ")


def fcatalogue(url, title):
    soup = open_url(url)

    content = soup.find("div", {"class": "catalog-list column-4"})
    content = content.find_all("ol")
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
            sp = pattern(cas[i]) + "(.+)" + end
            ptn = re.compile(r"%s" % sp, flags = re.S)
            res = ptn.search(tx)[1]
        else:
            sp = pattern(cas[i]) + "(.+)" + pattern(cas[i + 1])
            ptn = re.compile(r"%s" % sp, flags = re.S)
            # ptn = re.compile(r'河北省历史沿革\n编辑\n\n播报.*河北省行政区划\n编辑\n\n播报')
            # ptn = re.compile(r'河北省历史沿革\n编辑\n\n播报(.+)河北省行政区划\n编辑\n\n播报')
            res = ptn.search(tx)[1]
        res = re.sub("\s", "", res)
        with open(f"../data/catalog/{cas[i]}.txt", "a+", encoding = "utf-8") as f:
            f.write(title + "\t" + cas[i] + "\t" + res + "\n")


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

def crawl_image(url, save_path, addtion, sign):
    print("-------------------------------------------------------------")
    print(url)
    print("start.....")
    base_url = "https://baike.baidu.com"
    error_count = 0


    soup = open_url(url)
    while True:
        try:
            title = soup.find("h1").text
            break
        except:
            time.sleep(0.1)
            print("-----sleep-----")
            soup = open_url(url)

    try:
        pic_album = soup.find("a", {"class": "more-link"}).get('href')
    except:
        # 页面无图的情况
        judge = soup.find("div", {"class": "edit-prompt"})
        if judge != None:
            if "缺少" in judge.text:
                print(
                    "************************************************************************************************************************************************")
                print(url, "无图!")
                print(
                    "************************************************************************************************************************************************")
                with open("problem_log.txt", "a+", encoding = "utf-8") as f:
                    f.write(url + "  无图!" + "\n")
                return -1

        # 页面中转情况
        print("************************************************************************************************************************************************")
        print(url, "transfer!")
        print("************************************************************************************************************************************************")
        transfered_url = deal_transfer_page(soup, addtion, sign)
        if transfered_url == False:
            print("transfer error!!!!!")
            with open("problem_log.txt", "a+", encoding = "utf-8") as f:
                f.write(url + "  transfer error!" + "\n")
            return 1
        else:
            crawl_image(transfered_url, save_path, addtion, sign)
            return None

    url = base_url + pic_album

    soup = open_url(url)

    content = soup.find_all("div", {"id": "album-list", "class": "album-list"})
    # print(content)
    for ct in content:
        pics = ct.find_all("div", {"class": "pic-list"})
        for p in pics:
            # print(p)
            ats = p.find_all("a")
            # print(ats)
            cnt = 1
            for l in ats:
                l = base_url + l.get('href')
                soup = open_url(l)
                last_url = soup.find("img", {"id": "imgPicture"})
                try:
                    path = last_url.get("src")
                except:
                    print("last_url error!")
                    print(last_url)
                    with open("problem_log.txt", "a+", encoding = "utf-8") as f:
                        f.write(url + "  last_url error!" + "\n")
                    continue
                print(path)
                imgname = soup.find("span", {"class": "text"}).text
                if imgname == "":
                    imgname = soup.find("span", {"class": "album-desc"}).text
                try:
                    imgdata = requests.get(path).content
                except:
                    print("imgdata get error!")
                    continue
                # path = f"../data/image/{title}"
                path = os.path.join(save_path, title)
                if not os.path.exists(path):
                    os.makedirs(path)

                imgpath = path + "/" + imgname + ".png"
                if os.path.exists(imgpath):
                    cnt += 1
                    imgpath = path + "/" + imgname + str(cnt) + ".png"
                times = 10
                while True:
                    try:
                        with open(imgpath, "wb+") as f:
                            f.write(imgdata)
                            print(imgname, "success!")
                        break
                    except:
                        time.sleep(0.5)
                        if times:
                            times -= 1
                        else:
                            error_count += 1
                            print("save error %d" % error_count)
                            break

    # with open("test2.txt", "w+", encoding = "utf-8") as f:
    #     tx = soup.text.replace(u"\xa0", "")
        # tx = ptn_del_sqr_bkt.sub("", tx)
        # print(re.search("河北省历史沿革\n编辑\n\n播报", tx))
        # f.write(tx)
        # f.write(ptn_del_sqr_bkt.sub("", re.sub("\s", "", soup.text)))

def crawl_video(url, save_path, addtion):
    print("-------------------------------------------------------------")
    print(url)
    print("start.....")
    base_url = "https://baike.baidu.com"
    error_count = 0




if __name__ == "__main__":
    # url = "https://baike.baidu.com/item/%E6%B2%B3%E5%8C%97/65777"
    # title, s = find_intro(url)
    # print(title)
    # fcatalogue(url, "河北省")
    crawl_image("https://baike.baidu.com/item/%E9%BE%99%E5%B1%B1%E5%8C%BA", "", "吉林省", False)

