from vfc import open_url, judge_multiple_meaning, deal_transfer_page, pass_verification, judge_verification
from config import headers
from bs4 import BeautifulSoup
import requests


def validate(verify, url):
    global transfer_num
    global fail_verify_num
    # html = open_url(path, header)
    html = requests.get(url, headers = headers)
    soup = BeautifulSoup(html.text, "lxml")

    if judge_verification(soup):
        html, soup = pass_verification(url, headers)

    transfer_flag = judge_multiple_meaning(soup)
    if transfer_flag:
        print(url, "transfer")
        transfer_num += 1
        with open("backups/log/transfer_url", "a+", encoding ="utf-8") as fw:
            fw.write(url + "\n")
    else:
        head = soup.find("h1")
        if verify in head.text:
            print(head.text)
        else:
            print(url, "verify error")
            fail_verify_num += 1
    # transfer_condition = deal_transfer_page(soup, addtion, False)
    # if transfer_condition == False:
    #     print("transfer error!!!!!")
    #     with open("transfer_problem_log.txt", "a+", encoding = "utf-8") as f:
    #         f.write(url + "\n")
    #     return 1
    # else:
    #     pre_video_urls(transfer_condition, save_path, addtion)
    #     return None


if __name__ == "__main__":
    path = "../finished_links/县"
    transfer_num = 0
    fail_verify_num = 0
    with open(path, "r+", encoding = "utf-8") as fr:
        url_lists = fr.read().split()
    t = 0
    for url in url_lists:
        # if t:
        #     t -= 1
        #     continue

        print(url)
        # url = "https://baike.baidu.com/item/%E5%87%A4%E5%BA%86%E5%8E%BF"
        validate("县", url)
    print("transfer_num: ", transfer_num)
    print("fail_verify_num: ", fail_verify_num)
