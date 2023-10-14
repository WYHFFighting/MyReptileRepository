import re

import requests
from bs4 import BeautifulSoup
import func
from func import open_url
import os
import multiprocessing as mp


# 递归得到文件
def recursive_listdir(path):
    book = []
    name = []
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        book.append(file_path)
        name.append(file)
    return book, name


# 爬取图片
def crawl_pic(path, base_save_path):
    prov_path, prov_name = recursive_listdir(path)
    for pro in prov_path:
        files, x = recursive_listdir(pro)
        for f in files:
            # 在这里更改正则表达式
            prefix = re.search(r"\\(.+)\.txt$", f)[1]
            save_path = os.path.join(base_save_path, prefix)
            prefix = re.search(r"^(.+)\\", prefix)[1]
            # print(prefix)
            # return None
            with open(f, "r+", encoding = "utf-8") as fw:
                urls = fw.read().split()

            print(
                "****************************************************************************************************************")
            print(prefix)
            print(
                "****************************************************************************************************************")

            # 多进程
            pool = mp.Pool(4)
            res = [pool.apply_async(func.crawl_image, args = (url, save_path, prefix, False)) for url in urls]
            [t.get() for t in res]

            # 单进程
            # for url in urls:
            #     print("-------------------------------------------------------------")
            #     print(url)
            #
            #     func.crawl_image(url, save_path, prefix, False)

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    item = "自治县"
    path = f"../text/{item}"
    base_save_path = f"C:/Users/86183/Desktop/work/data/{item}"
    # 更改正则表达式
    crawl_pic(path, base_save_path)
