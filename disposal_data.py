import os


def recursive_listdir(path, file_lists, labels):
    files = os.listdir(path)
    for f in files:
        p = os.path.join(path, f)
        if os.path.isfile(p):
            file_lists.append(p)
        elif os.path.isdir(p):
            labels.append(f)
            recursive_listdir(p, file_lists, labels)
    return file_lists, labels


def traversal_dir(path):
    files = os.listdir(path)
    sub_dirs = []
    for f in files:
        p = os.path.join(path, f)
        # sub_dirs = os.listdir(p)
        sub_dirs.append(p)
    return sub_dirs, files


# def traversal_videos(path):
#     files = os.listdir(path)
#     sub_dirs = []
#     for f in files:
#         p = os.path.join(path, f)
#         # sub_dirs = os.listdir(p)
#         sub_dirs.append(p)
#     return sub_dirs, files

def province(path, load, index0):
    with open(load, "a+", encoding="utf-8") as fw:
        first_dirs, first_labels = traversal_dir(path)
        for i in range(len(first_dirs)):
            dir = first_dirs[i]
            lb = first_labels[i]
            index1 = index0 + "," + lb
            files = os.listdir(dir)
            cnt = len(files)
            fw.write(index1 + "," + str(cnt) + "\n")

if __name__ == "__main__":
    # path = r"E:\wyh\reptile\video\crwal_video\data2"
    # files = os.listdir(path)
    # for f in files:
    #     print('"' + f, end='",')
    province("./data2/省级行政区", "data2/test.csv", "省级行政区")
    # exit()

    # names = ["县", "县级市", "地区", "地级市", "市辖区", "旗", "林区", "特区", "盟", "省级行政区", "自治县", "自治州", "自治旗"]
    names = ["县", "县级市", "地区", "地级市", "市辖区", "旗", "林区", "特区", "盟", "自治县", "自治州", "自治旗"]
    base_path = "./data2/"
    with open("data2/summarize.csv", "w+", encoding="utf-8") as fw:
        for item in names:
            path = os.path.join(base_path, item)
            first_dirs, first_labels = traversal_dir(path)
            index0 = item
            for i in range(len(first_dirs)):
                dir = first_dirs[i]
                lb = first_labels[i]
                index1 = index0 + "," + lb
                second_dirs, second_labels = traversal_dir(dir)
                for j in range(len(second_dirs)):
                    sec_dir = second_dirs[j]
                    sec_lb = second_labels[j]
                    index2 = index1 + "," + sec_lb
                    third_dirs, third_labels = traversal_dir(sec_dir)
                    for k in range(len(third_labels)):
                        third_dir = third_dirs[k]
                        third_lb = third_labels[k]
                        files = os.listdir(third_dir)
                        cnt = len(files)
                        index3 = index2 + "," + third_lb
                        fw.write(index3 + "," + str(cnt) + "\n")
                        # break

    province("./data2/省级行政区", "data2/summarize.csv", "省级行政区")

                # print(second_dirs)
                # print(second_labels)

    # for fir_dir, fir_lb in first_dirs, first_labels:
    #     print(fir_dir, fir_lb)
    #
    # print(first_dirs)
    # print(first_labels)
    # labels.append(first_dirs)
    # for fir in first_dirs:
    #     second_dirs


