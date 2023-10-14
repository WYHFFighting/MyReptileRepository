import os
import re
import shutil

# def recursive_listdir(path):
#     book = []
#     name = []
#     files = os.listdir(path)
#     for file in files:
#         file_path = os.path.join(path, file)
#         book.append(file_path)
#         name.append(file)
#     return book
def recursive_listdir(path):
    book = []
    name = []
    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        book.append(file_path)
        name.append(file)

    return book, name

# deal 1
# path = "地级市"
# ptn = re.compile(r"\\地级市(.+)\.txt$")
# files, names = recursive_listdir(path)
# for file in files:
#     print(file)
#     dir = ptn.search(file)[1]
#     p = os.path.join(path, dir)
#     if not os.path.exists(p):
#         os.makedirs(p)
#     shutil.move(file, p)

# deal 2
path = "../link/县"
files, names = recursive_listdir(path)
os.chdir(path)
ptn = re.compile(r"^(.+?)（")
for file in names:
    print(file)
    try:
        dir = ptn.search(file)[1]
    except:
        continue
    print(dir)
    # print(os.getcwd())
    os.rename(file, dir)
    # p = os.path.join(path, dir)
    # if not os.path.exists(p):
    #     os.makedirs(p)
    # shutil.move(file, p)

# with open("path", "r+", encoding="utf-8") as f:
#     list
