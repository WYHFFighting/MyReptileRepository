import os
import re


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


def set_url(path, save):
    first_catlog = recursive_listdir(path)
    # print(len(first_catlog))
    for fir in first_catlog:  # ../ link\县
        level = re.search(r"\\(.+?)$", fir)[1]  # 县
        second_catlog = recursive_listdir(fir)
        with open(os.path.join(save, level), "w+", encoding = "utf-8") as fw:
            for sec in second_catlog:  # ../link\县\云南省
                files = recursive_listdir(sec)
                for fe in files:  # ../link\县\云南省\临沧市.txt
                    # print(fe)
                    save_path = re.search(r"link\\(.+?)\.txt", fe)[1]
                    save_path = os.path.join("./data", save_path)
                    print(save_path)
                    # continue
                    with open(fe, "r+", encoding = "utf-8") as fr:
                        tfs = fr.read().split()
                        for t in tfs:
                            t = t + "\t" + save_path + "\n"
                            # t = t + "\n"
                            fw.write(t)
        #     thirdcatalog = recursive_listdir(sec)
            # for third in thirdcatalog:
            #     print(third)
        # print(second_catlog)

def count(path):
    pro_in_xian = recursive_listdir(path)
    for pro in pro_in_xian:
        # print(pro)
        shi_clu_xian = recursive_listdir(pro)
        pro_cnt = 0
        for shi in shi_clu_xian:
            # print(shi)
            # break
            with open(shi, "r+", encoding = "utf-8") as fr:
                num = len(fr.read().split())
                pro_cnt += num
        print(pro, pro_cnt)

#
def add_savepath(filepath, savepath):
    with open(filepath, "r+", encoding="utf-8") as fr:
        urls = fr.read().split()
    for ur in urls:
        with open(filepath, "a+", encoding="utf-8") as fw:
            fw.write(ur + "\t" + savepath + "\n")


if __name__ == "__main__":
    # set_url(path = "../link", save = "../finished_links")
    # count("../link/县")
    add_savepath("省", "./data/省")
