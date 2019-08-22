import matplotlib.pyplot as plt
import matplotlib as mpl
import sklearn
import pandas as pd
import numpy as np
import requests
import time
import random
import math

RawData = pd.read_csv("TrainData_2w.csv")
UserCategory = ["C1","C2","C3","C4","C5"]
# 将用户编码与基金代码按照不重合的规则重编码
UserList = RawData.用户编码.unique()
FundList = RawData.基金代码.unique()
# 计算中用户/商品数量
FundNum = FundList.shape[0]
UserNum = UserList.shape[0]
# 读取评分矩阵
JudgeMatrix = eval(open('Judge.txt').read())
# 注意，这里JudgeMatrix[i][j]指的是UserList中第i个用户对FundList中第j个基金的评分
# i != 用户编码，UserList[i] == 用户编码
# j != 基金代码, FundList[j] == 基金代码

# 事例
print(JudgeMatrix[0][0])