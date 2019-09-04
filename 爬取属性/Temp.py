import matplotlib.pyplot as plt
import matplotlib as mpl

import pandas as pd
import numpy as np
import math
import 评分矩阵.Standardization
import 评分矩阵.CreatePoint_csv

pathIndex = "../基金列表及属性/"
UserCategory = ["C1", "C2", "C3", "C4", "C5"]
PointColumns = ["User", "FundCode", "Point", "Type"]

def GenerateFavor(PointMatrix, EigenvectorFrame, AllFundList, FundList):
    FavorFrame = pd.DataFrame()
    [rows, cols] = PointMatrix.shape
    for i in range(rows):
        tempSeries = pd.Series([0, 0, 0, 0, 0, 0], index=["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"])
        for j in range(cols):
            if PointMatrix[i, j] != 0:
                # 累加获得用户喜好向量
                tempSeries = tempSeries + (PointMatrix[i, j] * EigenvectorFrame.loc[AllFundList.index(FundList[j]), :])
        FavorFrame = FavorFrame.append(tempSeries, ignore_index=True)
    # 得到用户喜好向量文件
    # FavorFrame.to_csv(pathIndex + "FavorAttrNew.csv", encoding="gbk")
    return FavorFrame


def main():
    # 获得Point
    # PointFrame = 评分矩阵.CreatePoint_csv.createPoint()
    # PointFrame = pd.read_csv(pathIndex + "Point_2.csv", encoding="gbk")
    # 标准化
    # PointFrame = 评分矩阵.Standardization.Standardization_4(PointFrame)
    PointFrame = pd.read_csv(pathIndex + "Point_Standardized.csv", encoding="gbk")
    print("Point标准化完毕")

    # 基金属性向量和全部基金编号的list
    EigenvectorFrame = pd.read_csv(pathIndex + "基金属性_旧基金2.0.csv", encoding="gbk")
    AllFundList = list(EigenvectorFrame.FundCode)
    EigenvectorFrame = EigenvectorFrame[["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"]]

    UserList = PointFrame.User.unique()
    FundList = PointFrame.FundCode.unique()
    UserNum = UserList.shape[0]
    FundNum = FundList.shape[0]
    # print("UserNum:%d FundNum:%d" % (UserNum, FundNum))
    UserIndex = 0
    FundIndexList = []
    UserIndexList = []
    # 对Frame添加重编码的码号
    for line in PointFrame.itertuples():
        if UserList[UserIndex] != line.User:
            UserIndex = UserIndex + 1
        UserIndexList.append(UserIndex)     # 将原本的User编号转化为从0开始，数量不变
        # np.where(FundList == line.FundCode)为FundList中与line.FundCode相同的坐标
        # 将FundCode编号转化为从0开始
        FundIndexList.append(np.where(FundList == line.FundCode)[0][0])
    PointFrame.loc[:, 'UserIndex'] = UserIndexList
    PointFrame.loc[:, 'FundIndex'] = FundIndexList

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
    for line in PointFrame.itertuples():
        PointMatrix[line.UserIndex, line.FundIndex] = line.Point
    # 生成偏好向量
    print("开始生成偏好向量")
    FavorFrame = GenerateFavor(PointMatrix, EigenvectorFrame, AllFundList, FundList)
    return FavorFrame


if __name__ == '__main__':
    main()
