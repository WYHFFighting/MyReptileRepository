import pandas as pd


df = pd.read_csv(r"D:\CodeProjects\pycharmProjects\AI_Project_Work\video\crwal_video\text\县\凤庆县\total", names = ["url"])
print(len(df))
# print(df)
dup = df.duplicated()
print(len(dup))
# dup = dup.values
# print(dup)
index = []
cnt = 0
for i in range(len(dup)):
    if dup[i] == True:
        cnt += 1
        index.append(i)
        # print(i, end = " ")
# print()
print(cnt)

# for j in index:
#     print(df.iloc[j, :].values[0], "  ", j)



