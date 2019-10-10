import pandas as pd
import numpy as np
import time
import math
pathIndex = ""

def createPoint(RawData, TradeFrame):
    TypeFrame = pd.DataFrame(RawData.客户类别,index = RawData.客户编号)

    UserList = TradeFrame.客户编号.unique()
    FundList = TradeFrame.基金编号.unique()
    # 计算中用户/商品数量
    FundNum = len(FundList)
    UserNum = len(UserList)
    # print("用户数量:%d 商品数量:%d" % (UserNum,FundNum))
    # 初始化评分矩阵
    PointUserList = []
    PointList = []
    PointFundList = []
    PointTypeList = []
    for i in range(UserNum):
        # # 进度条
        # progress = int(i*100/UserNum)
        # progerss_str = ('#'*progress)+"({}%/100%)".format(progress)
        # print("\rCreate Point Progress:{:<120}".format(progerss_str),end="")
        # 获取用户类型
        Type = TypeFrame.loc[UserList[i]].客户类别
        # 框选用户数据
        UserData = TradeFrame.ix[TradeFrame.客户编号 == UserList[i]]
        # 获得其投资总额
        InvestSum = sum(UserData.交易金额)
        # 获得其最晚活跃时间
        TimeList = []
        for x in UserData.交易时间:
            TimeList.append(time.mktime(time.strptime(x,'%Y-%m-%d  %H:%M:%S')))
        MaxTime = np.max(TimeList)
        # 框选其投资数据，计算评分要素
        for FundCode in UserData.基金编号.unique():
            InvestData = UserData.ix[UserData.基金编号 == FundCode]
            Invest = sum(InvestData.交易金额)
            t = 0
            for x in InvestData.交易时间:
                tx = time.mktime(time.strptime(x,'%Y-%m-%d  %H:%M:%S'))
                if tx >= t:
                    t = tx
            # 论文中给出的评分模型
            Point = (Invest/InvestSum)*math.log((1+t/MaxTime),2)+1
            PointFundList.append(FundCode)
            PointUserList.append(UserList[i])
            PointList.append(Point)
            PointTypeList.append(Type)
    PointCSV = pd.DataFrame({"User":PointUserList,"FundCode":PointFundList,"Point":PointList,"Type":PointTypeList})
    # PointCSV.to_csv('Point.csv',index=False)
    # print("PointCSV Created")
    return PointCSV


        


    































