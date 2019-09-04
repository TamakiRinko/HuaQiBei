import matplotlib.pyplot as plt
import matplotlib as mpl
import sklearn
import pandas as pd
import numpy as np
import requests
import time
import random
import math
import 训练集.CreateData_GX
import 爬取属性.GenerateAttrs_Thread
pathIndex = "../基金列表及属性/"
# pathIndex2 = "../用户画像/数据/"


def Train(data):
    pass


# 以7.1为标准，计算时间戳
def Time(t):
    pass


def createPoint():
    # 生成基金属性
    爬取属性.GenerateAttrs_Thread.main("旧基金2.0.csv", "gbk")
    爬取属性.GenerateAttrs_Thread.main("新基金2.0.csv", "utf-8")
    # 生成训练集
    训练集.CreateData_GX.createData()

    RawData = pd.read_csv(pathIndex + "交易记录.csv", encoding="gbk")
    UserRecord = pd.read_csv(pathIndex + "用户记录.csv", encoding="gbk")

    # 得到用户评分矩阵
    # 将用户编码与基金代码按照不重合的规则重编码
    UserList = RawData.客户编号.unique()
    # 破案，有人这两个月没买！现已修改为每个人都会买！
    FundList = RawData.基金编号.unique()
    # 计算中用户/商品数量
    FundNum = len(FundList)
    UserNum = len(UserList)
    print("用户数量:%d 商品数量:%d" % (UserNum,FundNum))
    # 初始化评分矩阵
    PointUserList = []
    PointList = []
    PointFundList = []
    PointTypeList = []
    for i in range(UserNum):
        print(UserList[i])
        # 框选用户数据
        UserData = RawData.ix[RawData.客户编号 == UserList[i]]
        # 获得其投资总额
        InvestSum = sum(UserData.交易金额)
        # 获得其最晚活跃时间
        TimeList = []
        for x in UserData.交易时间:
            TimeList.append(time.mktime(time.strptime(x,'%Y-%m-%d %H:%M:%S')))
        MaxTime = np.max(TimeList)
        # 框选其投资数据，计算评分要素
        for FundCode in UserData.基金编号.unique():
            InvestData = UserData.ix[UserData.基金编号 == FundCode]
            Invest = sum(InvestData.交易金额)
            j = np.where(FundList == FundCode)
            t = 0
            for x in InvestData.交易时间:
                tx = time.mktime(time.strptime(x,'%Y-%m-%d %H:%M:%S'))
                if tx >= t:
                    t = tx
            # 评分模型
            Point = (Invest/InvestSum)*math.log(1+t/MaxTime)+1
            PointFundList.append(FundCode)
            PointUserList.append(UserList[i])
            PointList.append(Point)
            # PointTypeList.append(UserData.iat[0,2])
            # print("C" + str(UserRecord.iat[UserList[i], 9] + 1))
            PointTypeList.append("C" + str(UserRecord.iat[UserList[i], 9] + 1))

    PointCSV = pd.DataFrame({"User":PointUserList,"FundCode":PointFundList,"Point":PointList,'Type':PointTypeList})
    # PointCSV.to_csv(pathIndex + "Point_2.csv")
    return PointCSV


if __name__ == '__main__':
    createPoint()



'''
for Frame in TrainList:
    # 重编码
    UserList = Frame.用户编码.unique()
    FundList = Frame.基金代码.unique()
    # 计算一类中用户/商品数量
    FundNum = FundList.shape[0]
    UserNum = UserList.shape[0]
    # 初始化评分矩阵
    Matrix = np.zeros((UserNum, FundNum))
    for i in range(UserNum):
        # 框选用户数据
        UserData = Frame.ix[Frame.用户编码 == UserList[i]]
        InvestSum = sum(UserData.投资金额)
        # 获得其最晚活跃时间
        TimeList = []
        for x in UserData.投资时间:
            TimeList.append(time.mktime(time.strptime(x,'%Y-%m-%d')))
        MaxTime = np.max(TimeList)
        # 框选其投资数据，计算评分要素
        for FundCode in UserData.基金代码:
            InvestData = UserData.ix[UserData.基金代码 == FundCode]
            Invest = sum(InvestData.投资金额)
            j = np.where(FundList == FundCode)
            t = 0
            for x in InvestData.投资时间:
                tx = time.mktime(time.strptime(x,'%Y-%m-%d'))
                if tx >= t:
                    t = tx
            # 评分模型
            Matrix[i][j] = (Invest/InvestSum)*math.log(1+t/MaxTime)+1
    MatrixList.append(Matrix)

# 评分矩阵已经构建完毕，下面进入协同过滤阶段
'''
            

        


    































