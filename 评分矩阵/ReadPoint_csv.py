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
PointColumns =["User", "FundCode", "Point", "Type"]
# 将用户编码与类型形成映射
UserTypeList = []
ans = -1
for line in RawData.itertuples():
    temp = line.用户编码
    if ans != temp:
        UserTypeList.append(line.用户类型)


# 读取评分矩阵
PointFrame = pd.read_csv("Point.csv")
# 标准化
PointFrame = 评分矩阵.Standardization.Standardization_1(PointFrame)

# 将评分矩阵分为五类
FrameList = []  # 不同C类的DataFrame
for Category in UserCategory:
        FrameList.append(PointFrame.ix[PointFrame.Type == Category])
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
        UserIndexList.append(UserIndex)
        FundIndexList.append(np.where(FundList == line.FundCode)[0][0])
    Frame['UserIndex'] = UserIndexList
    Frame['FundIndex'] = FundIndexList

    ''' 调试代码
    # print(Frame)
    # for line in Frame.itertuples():
    #         if UserList[line.UserIndex] != line.User:
    #                 print(line)
    #                 print(UserList[line.UserIndex],line.UserIndex)
    #                 print("The UserList line has spmething wrong!")
    #         if FundList[line.FundIndex] != line.FundCode:
    #                 print("The FundList line has spmething wrong!")
    '''

    # 划分训练集与测试集
    TrainData, TestData = ms.train_test_split(Frame, test_size=0.25)
    TrainMatrix = np.zeros((UserNum, FundNum))
    TestMatrix = np.zeros((UserNum,FundNum))
    for line in TrainData.itertuples():
        TrainMatrix[line.UserIndex,line.FundIndex] = line.Point
    for line in TestData.itertuples():
        TestMatrix[line.UserIndex,line.FundIndex] = line.Point
