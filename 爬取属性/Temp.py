import pandas as pd
from sklearn import preprocessing
import numpy as np
pathIndex = "../基金列表及属性/"

# df = pd.DataFrame({
# 'p_str': ['10.33%','23.22%','56%','35.786%','99.0009%']
# })
# print(df)
# p_float = df['p_str'].str.strip("%").astype(float)/100
# print(p_float)
# print(type(p_float))
#
# print(float("0.028"))

# df = pd.read_csv(pathIndex + "基金属性.csv")
# print(df.loc[1, :])
# df = df[["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"]]
# print(df.loc[1, :] * 0.1 + [1, 1, 1, 1, 1, 1])
# print(type(df.loc[1, :] * 0.1 + [1, 1, 1, 1, 1, 1]))
# print(df.loc[1, :] * 0.1 + df.loc[1, :])

# df = pd.Series([7, 8, 9])
# print(df)
# list1 = [1, 2, 3]
# list2 = [3, 4.5, 6]
# print(list1 + list2)
# list2 = [list2[i] + list1[i] for i in range(len(list1))]
# print(list2)
# print(df + list1)
# Data = pd.DataFrame()
# tempList = pd.Series([1, 1, 1, 1, 1, 1], index=["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"])
# print(tempList)
# Data = Data.append(tempList + df.loc[1, :] * 0.1, ignore_index=True)
# Data = Data.append(tempList + df.loc[1, :] * 0.1, ignore_index=True)
# print(Data)


X = pd.DataFrame([ [1.0, 3.0, 2.0],
               [2.0, 2.0, 0],
               [0, 1.0, -1.0]])
print(X)
ser = pd.Series(["asd", 1, "bbb"])
X.insert(0, "mydata", ser)
print(X)
# print(X)
# print(type(X))
# X = preprocessing.scale(X)
# print(X)
# print(type(X))
# # 处理后数据的均值和方差
# print(X.mean(axis=0))
# print(X.std(axis=0))

