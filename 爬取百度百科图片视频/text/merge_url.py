import os
import sys


def merge(item):
    # sys.path.append(f"./")
    # print(sys.path)
    path = f"text/{item}"
    txts = os.listdir(path)
    with open(f"text/{item}/total", "w+", encoding = "utf-8") as ft:
        for t in txts:
            with open(f"text/{item}/" + t, "r+", encoding = "utf-8") as fr:
                urls = fr.read().split()
            for l in urls:
                ft.write(l + "\n")


if __name__ == "__main__":
    item = "河北省"
    merge(item)



