import re
import sys


def ded(item):
    # sys.path.append(f"./")
    clean_data = set()
    # print(sys.path)
    with open(f"text/{item}/total", "r+", encoding = "utf-8") as f:
        url_lists = f.read().split()
    for url in url_lists:
        clean_data.add(url)

    with open(f"text/{item}/clean_data", "w+", encoding = "utf-8") as f:
        for i in range(len(clean_data)):
            d = clean_data.pop()
            # print(d)
            d = re.sub(r"\\", "", d)
            # print(d)
            # break
            f.write(d + "\n")


if __name__ == "__main__":
    item = "河北省"
    ded(item)
