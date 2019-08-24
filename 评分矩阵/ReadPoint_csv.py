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

pathIndex = "../基金列表及属性/"
UserCategory = ["C1", "C2", "C3", "C4", "C5"]
PointColumns = ["User", "FundCode", "Point", "Type"]

def GenerateFavor(PointMatrix, EigenvectorFrame, AllFundList, FundList, index):
    # print(PointMatrix)
    FavorFrame = pd.DataFrame()
    [rows, cols] = PointMatrix.shape
    # print(rows, cols)
    for i in range(rows):
        tempSeries = pd.Series([0, 0, 0, 0, 0, 0], index=["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"])
        for j in range(cols):
            if PointMatrix[i, j] != 0:
                # 累加获得用户喜好向量
                tempSeries = tempSeries + (PointMatrix[i, j] * EigenvectorFrame.loc[AllFundList.index(FundList[j]), :])
        FavorFrame = FavorFrame.append(tempSeries, ignore_index=True)
    # 得到用户喜好向量文件
    FavorFrame.to_csv(pathIndex + "FavorAttr_" + UserCategory[index] + ".csv", encoding="utf_8_sig")


def main():
    # 训练集
    RawData = pd.read_csv(pathIndex + "TrainData.csv")
    # 基金属性向量和全部基金编号的ndarray
    EigenvectorFrame = pd.read_csv(pathIndex + "基金属性.csv")
    AllFundList = list(EigenvectorFrame.FundCode)
    EigenvectorFrame = EigenvectorFrame[["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"]]

    # # 将用户编码与类型形成映射，UserTypeList中为依次的类型
    # UserTypeList = []
    # ans = -1
    # for line in RawData.itertuples():
    #     temp = line.用户编码
    #     if ans != temp:
    #         UserTypeList.append(line.用户类型)

    # 读取评分csv文件
    PointFrame = pd.read_csv(pathIndex + "Point.csv")
    # 标准化
    PointFrame = 评分矩阵.Standardization.Standardization_1(PointFrame)

    # 将用户分为五类
    FrameList = []  # 不同C类的DataFrame
    for Category in UserCategory:
        FrameList.append(PointFrame.loc[PointFrame.Type == Category].copy())    # 每个Frame指定为拷贝

    index = 0   # 表明种类
    # 对每一类用户分别预测
    for Frame in FrameList:
        # 按不重合的方式对用户/商品重编码
        UserList = Frame.User.unique()
        FundList = Frame.FundCode.unique()
        UserNum = UserList.shape[0]
        FundNum = FundList.shape[0]
        # print("UserNum:%d FundNum:%d" % (UserNum, FundNum))
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
        # print(Frame)

        ''' 调试代码
        print(Frame)
        for line in Frame.itertuples():
            if UserList[line.UserIndex] != line.User:
                print(line)
                print(UserList[line.UserIndex],line.UserIndex)
                print("The UserList line has spmething wrong!")
            if FundList[line.FundIndex] != line.FundCode:
                print("The FundList line has spmething wrong!")
        '''

        '''
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

        # 暂时不考虑训练集与测试集
        PointMatrix = np.zeros((UserNum, FundNum))  # 评分矩阵
        for line in Frame.itertuples():
            PointMatrix[line.UserIndex, line.FundIndex] = line.Point
        GenerateFavor(PointMatrix, EigenvectorFrame, AllFundList, FundList, index)
        index = index + 1


main()
