import regex as re

ptn_del_sqr_bkt = re.compile(r".*?(\[.+?\]).*?")  # 查找所有包含在中括号【】中的内容