import regex as re

ptn_del_sqr_bkt = re.compile(r".*?(\[.+?\]).*?")  # 提取中括号[]中的内容
