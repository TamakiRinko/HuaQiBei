import matplotlib.pyplot as plt
import matplotlib as mpl
import sklearn
import pandas as pd
import numpy as np
import requests
import time
import random
import math

def Train(data):
    pass

# 以7.1为标准，计算时间戳
def Time(t):

    pass

# 首先将5个类别的数据分离开来
RawData = pd.read_csv("TrainData.csv")
UserCategory = ["C1","C2","C3","C4","C5"]
TrainList = []
for Category in UserCategory:
    List = RawData.ix[RawData.用户类型 == Category]
    TrainList.append(List)

# 得到用户评分矩阵
# 将用户编码与基金代码按照不重合的规则重编码
UserList = RawData.用户编码.unique()
# 破案，有人这两个月没买！现已修改为每个人都会买！
FundList = RawData.基金代码.unique()
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
    # 框选用户数据
    UserData = RawData.ix[RawData.用户编码 == UserList[i]]
    # 获得其投资总额
    InvestSum = sum(UserData.投资金额)
    # 获得其最晚活跃时间
    TimeList = []
    for x in UserData.投资时间:
        TimeList.append(time.mktime(time.strptime(x,'%Y-%m-%d')))
    MaxTime = np.max(TimeList)
    # 框选其投资数据，计算评分要素
    for FundCode in UserData.基金代码.unique():
        InvestData = UserData.ix[UserData.基金代码 == FundCode]
        Invest = sum(InvestData.投资金额)
        j = np.where(FundList == FundCode)
        t = 0
        for x in InvestData.投资时间:
            tx = time.mktime(time.strptime(x,'%Y-%m-%d'))
            if tx >= t:
                t = tx
        # 评分模型
        Point = (Invest/InvestSum)*math.log(1+t/MaxTime)+1
        PointFundList.append(FundCode)
        PointUserList.append(UserList[i])
        PointList.append(Point)
        PointTypeList.append(UserData.iat[0,2])

PointCSV = pd.DataFrame({"User":PointUserList,"FundCode":PointFundList,"Point":PointList,'Type':PointTypeList})
PointCSV.to_csv("Point_2.csv")



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
            

        


    































