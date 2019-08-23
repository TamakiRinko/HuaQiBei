import matplotlib.pyplot as plt
import matplotlib as mpl

import sklearn
from sklearn import model_selection as ms
import scipy.sparse as sp
from scipy.sparse.linalg import svds
from sklearn.metrics import mean_squared_error
from math import sqrt

import pandas as pd
import numpy as np
import math
import 评分矩阵.Standardization

RawData = pd.read_csv("TrainData.csv")
UserCategory = ["C1", "C2", "C3", "C4", "C5"]
PointColumns = ["User", "FundCode", "Point", "Type"]

# 将用户编码与类型形成映射，UserTypeList中为依次的类型
UserTypeList = []
ans = -1
for line in RawData.itertuples():
    temp = line.用户编码
    if ans != temp:
        UserTypeList.append(line.用户类型)

# 读取评分矩阵
PointFrame = pd.read_csv("Point_2.csv")
# 标准化
PointFrame = 评分矩阵.Standardization.Standardization_1(PointFrame)

# 将评分矩阵分为五类
FrameList = []  # 不同C类的DataFrame
for Category in UserCategory:
    FrameList.append(PointFrame.loc[PointFrame.Type == Category].copy())    # 每个Frame指定为拷贝


UserList = PointFrame.User.unique()
FundList = PointFrame.FundCode.unique()
UserNum = UserList.shape[0]
FundNum = FundList.shape[0]
print("UserNum:%d FundNum:%d" % (UserNum, FundNum))
Num2 = RawData.基金代码.unique().shape[0]
print("Num2:%d" % Num2)

FundListAll = pd.read_csv("基金列表_Final.csv")
FundList2 = FundListAll.FundCode.unique()
SubPointFrame = PointFrame[PointFrame["FundCode"].isin(FundList2)].copy()
print(len(SubPointFrame), len(PointFrame))

'''
# 对每一类用户分别预测
for Frame in FrameList:
    # 按不重合的方式对用户/商品重编码
    UserList = Frame.User.unique()
    FundList = Frame.FundCode.unique()
    UserNum = UserList.shape[0]
    FundNum = FundList.shape[0]
    print("UserNum:%d FundNum:%d" % (UserNum, FundNum))
    FundIndex = 0
    UserIndex = 0
    FundIndexList = []
    UserIndexList = []
    # 对Frame添加重编码的码号
    for line in Frame.itertuples():
        if UserList[UserIndex] != line.User:
            UserIndex = UserIndex + 1
        UserIndexList.append(UserIndex)     # 将原本的User编号转化为从0开始，数量不变
        # np.where(FundList == line.FundCode)为FundList中与line.FundCode相同的坐标
        # 将FundCode编号转化为从0开始
        FundIndexList.append(np.where(FundList == line.FundCode)[0][0])
    Frame.loc[:, 'UserIndex'] = UserIndexList
    Frame.loc[:, 'FundIndex'] = FundIndexList
    print(Frame)


    # 划分训练集与测试集
    TrainData, TestData = ms.train_test_split(Frame, test_size=0.25)
    TrainMatrix = np.zeros((UserNum, FundNum))
    TestMatrix = np.zeros((UserNum, FundNum))
    # 两个数组并不是满的
    # 注意，这里TrainMatrix[i][j]和TestMatrix[i][j]指的是UserList中第i个用户对FundList中第j个基金的评分
    # i != 用户编码，UserList[i] == 用户编码
    # j != 基金代码, FundList[j] == 基金代码
    for line in TrainData.itertuples():
        TrainMatrix[line.UserIndex, line.FundIndex] = line.Point
    for line in TestData.itertuples():
        TestMatrix[line.UserIndex, line.FundIndex] = line.Point

'''