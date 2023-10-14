from fake_useragent import UserAgent
import regex as re

# headers = {
#         "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
#         "Cookie": "__bid_n=187a72fcb7d92eab334207; BAIDU_WISE_UID=wapp_1682257090618_405; ZFY=rbfu:Ag3OMLIy6i4II46:Bpey8uvkVrJ0dpPTPR3LE6wk:C; BIDUPSID=9618AC08BF6FC9CA2F528D314B4F8BCA; PSTM=1682496239; jsdk-uuid=822ccd43-2be4-4131-a37e-df9f4fc14ad8; BDUSS=FRPZkE0UkN0flBTbkNLN3BoSnkwLTFQNzFZSXZQdEZOSzBubGFqMjFJbFQySEJrRVFBQUFBJCQAAAAAAAAAAAEAAAB2SXcz0LDG38nZeNTCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFNLSWRTS0lkN; BDUSS_BFESS=FRPZkE0UkN0flBTbkNLN3BoSnkwLTFQNzFZSXZQdEZOSzBubGFqMjFJbFQySEJrRVFBQUFBJCQAAAAAAAAAAAEAAAB2SXcz0LDG38nZeNTCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFNLSWRTS0lkN; BAIDUID=3444D05B6761FB31130554823D36327B:FG=1; BAIDUID_BFESS=3444D05B6761FB31130554823D36327B:FG=1; FPTOKEN=zA4NPXlUyYcaxU1fQH1j8lRCMafbi9j36FAIWyFszI/aMl4MCz+4qC8DVk1qILMNluMslpCWWEIu9cAwMzOIuIDemp+3WF8BvJJ1C7UwAtW013OnfbX57d/nFCA7pvagm36PbDgbAFvGy/3ByL3QbGpUJ9WomBSPyJHvLA+BXO4wK/IdBX0UyzNKffgv9DYvAG8nHVqOUMiJVoRp6fOvURM7XMHUAAxhPhGED01sXzfIG0pmb5Hbha4iYzFOWu/0yNXai6Sy/VJKQowMUExyTlcf2N2oe0k4vZhFtX/ypdS+4BNjiLWSfO0AjwqWDUpNvXvknyt1hG69Siz3NfJP6+XtnYSDJ34tJiF/A1Wjn/DADFKah02KX7f6vdZyqj44uX0fywTqHcANNfF0w4GiNg==|ljq+wH6DCSJGLY1HivTZD64enugBMo4fraoGM56NstI=|10|c355ca79d1fb860b2ff0823e28c5be2a; ab_sr=1.0.1_NDRkOTg0N2ExODA4MWI3ZmFkNjQxZGYxZDhjMzUwNGNmMDA0NWMwODBmMWNkZTIxZGUwM2M3YTQ0OGJjYzY3NTljNDNlMjg4MGIyZmYxMjQwZmFmMGVlMjMzN2QwYmQwZDBkZTFjNTNmZmVmYWU3ZjYxODljOTZlYjZjN2QxYTA4ODNkYTdmZDFkMGU0NDcyMjU5NTQyZjY0MjE0ZjQ2Y2NjNWYzYjcwNzA0NjRjZDMxZjU3ODVlMTQ0ZDllOGRi; RT=\"z=1&dm=baidu.com&si=f91730ca-7b7a-487a-900b-2f00039fd43a&ss=lhqghg1t&sl=l&tt=kpo&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=t6mu",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42"
# }

# header = {
#         \"user-agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.42\"
# }


ua = UserAgent()
headers = {
        # "Accept": "image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        # "Cookie": "__bid_n=187a72fcb7d92eab334207; BAIDU_WISE_UID=wapp_1682257090618_405; ZFY=rbfu:Ag3OMLIy6i4II46:Bpey8uvkVrJ0dpPTPR3LE6wk:C; BIDUPSID=9618AC08BF6FC9CA2F528D314B4F8BCA; PSTM=1682496239; jsdk-uuid=822ccd43-2be4-4131-a37e-df9f4fc14ad8; BDUSS=FRPZkE0UkN0flBTbkNLN3BoSnkwLTFQNzFZSXZQdEZOSzBubGFqMjFJbFQySEJrRVFBQUFBJCQAAAAAAAAAAAEAAAB2SXcz0LDG38nZeNTCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFNLSWRTS0lkN; BDUSS_BFESS=FRPZkE0UkN0flBTbkNLN3BoSnkwLTFQNzFZSXZQdEZOSzBubGFqMjFJbFQySEJrRVFBQUFBJCQAAAAAAAAAAAEAAAB2SXcz0LDG38nZeNTCAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFNLSWRTS0lkN; BAIDUID=3444D05B6761FB31130554823D36327B:FG=1; BAIDUID_BFESS=3444D05B6761FB31130554823D36327B:FG=1; FPTOKEN=zA4NPXlUyYcaxU1fQH1j8lRCMafbi9j36FAIWyFszI/aMl4MCz+4qC8DVk1qILMNluMslpCWWEIu9cAwMzOIuIDemp+3WF8BvJJ1C7UwAtW013OnfbX57d/nFCA7pvagm36PbDgbAFvGy/3ByL3QbGpUJ9WomBSPyJHvLA+BXO4wK/IdBX0UyzNKffgv9DYvAG8nHVqOUMiJVoRp6fOvURM7XMHUAAxhPhGED01sXzfIG0pmb5Hbha4iYzFOWu/0yNXai6Sy/VJKQowMUExyTlcf2N2oe0k4vZhFtX/ypdS+4BNjiLWSfO0AjwqWDUpNvXvknyt1hG69Siz3NfJP6+XtnYSDJ34tJiF/A1Wjn/DADFKah02KX7f6vdZyqj44uX0fywTqHcANNfF0w4GiNg==|ljq+wH6DCSJGLY1HivTZD64enugBMo4fraoGM56NstI=|10|c355ca79d1fb860b2ff0823e28c5be2a; ab_sr=1.0.1_MDQ2NzNjMjkzZjA3YjY3ZDAwNjNmOWU0NTc2ODQ0NzU1NzQ1ZDdlOWY4NjEzMGI0Yzg0MjM2Mjk5MjI5NjQ4NTdkOGNkYTIzYTllMTQ4OWE2MzM3NDk5Yzk1ZDkxZmVhNjEzNjdhMjJkODZlMjRhZGEzMWVhZmI0OWZiZWU4NTY5YWI2YzQzNGIyMmE0Y2QyODk4ZDIyZDg4NTkxNGJlMTA5OTZiY2YxNWRmYTA0YjEyOGU0YjA2YWZlZjcyYmVl; RT=\"z=1&dm=baidu.com&si=f91730ca-7b7a-487a-900b-2f00039fd43a&ss=lhqghg1t&sl=p&tt=od8&bcn=https://fclog.baidu.com/log/weirwood?type=perf&ld=yvei",
        "User-Agent": ua.random
}

tunnel = "your tunnel"
username = "your user name"
password = "your password"
proxies = {
    "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
    "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
}

# 白名单方式（需提前设置白名单）
# proxies = {
#     "http": "http://%(proxy)s/" % {"proxy": tunnel},
#     "https": "http://%(proxy)s/" % {"proxy": tunnel}
# }


match_mp4 = re.compile(r"(?r)http.+?\.mp4")
# match_mp4 = re.compile(r"http.+?\.mp4")
video_url_model = "https://baike.baidu.com/api/second/video/list?lemmaId=526353&isSensitive=0&scene=pc_top&filterId=72944325&rn=12"
vum = "https://baike.baidu.com/api/second/video/list?lemmaId=3852481&isSensitive=0&scene=pc_top&filterId=74083311&rn=12"


if __name__ == "__main__":
        res = match_mp4.findall("httphttps://eoaigioaeg.mp4")
        print(res)
