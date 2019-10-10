import pandas as pd
import numpy as np
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from surprise import SVDpp
from surprise import Dataset
from surprise import Reader
from surprise.model_selection import cross_validate


# 评分矩阵生成线程函数
def CPThreadFuc(Dir):
    TradeFrame = Dir['TradeFrame']
    TypeFrame = Dir['TypeFrame']
    UserList = TradeFrame.客户编号.unique()
    # 计算中用户数量
    UserNum = len(UserList)
    # 初始化评分矩阵
    PointUserList = []
    PointList = []
    PointFundList = []
    PointTypeList = []
    for i in range(UserNum):
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
    
    return PointCSV
    
# 生成用户评分矩阵的多线程改良版,由于python的多线程是假的多线程，所以这里的函数并未采用，只是提供思路
def CPThread(TradeFrame,TypeFrame,ThreadNum = 4):
    UserList = TradeFrame.客户编号.unique()
    # 计算中用户/商品数量
    UserNum = len(UserList)
    SplitList = [x/ThreadNum * UserNum for x in range(ThreadNum)]
    DirList = []
    CPResList = []
    for i in range (ThreadNum):
        if i == ThreadNum - 1:
            Frame1 = TradeFrame[TradeFrame.客户编号 >= SplitList[i]]
            Frame2 = TypeFrame[TypeFrame.index >= SplitList[i]]
            DirList.append({'TradeFrame':Frame1,'TypeFrame':Frame2})
        else:
            Frame1 = TradeFrame.ix[(TradeFrame.客户编号 >= SplitList[i]) & (TradeFrame.客户编号 < SplitList[i+1])]
            Frame2 = TypeFrame.ix[(TypeFrame.index >= SplitList[i]) & (TypeFrame.index < SplitList[i+1])]
            DirList.append({'TradeFrame':Frame1,'TypeFrame':Frame2})
    Executor = ThreadPoolExecutor(max_workers=ThreadNum) 
    AllTask = [Executor.submit(CPThreadFuc, (Dir)) for Dir in DirList]
    for future in as_completed(AllTask):
        CPRes = future.result()
        CPResList.append(CPRes)
    OutFrame = pd.concat(CPResList)
    OutFrame.to_csv('Point.csv',index=False)
    return OutFrame

# 基于聚类改良的SVDpp推荐算法，默认推荐数量为10,默认用户类型数量为5
def SVDPP(PointFrame,RecommendNum = 10,TypeNum = 5):
    OutUserList = []
    OutFundList = []
    PointFrameList = []
    UserType = 0
    # 拆分评分矩阵为5类：
    for Type in range(5):
        PointFrameList.append(PointFrame.ix[PointFrame.Type == Type])
    # 对每一类用户分别评分：
    for Frame in PointFrameList:
        Frame = Frame.loc[:,'User':'Point']
        UserList = Frame.User.unique()
        FundList = Frame.FundCode.unique()  
        UserType = UserType + 1
        reader = Reader(rating_scale=(0,2))
        data = Dataset.load_from_df(Frame, reader=reader).build_full_trainset()
        if UserType == 4:
            model = SVDpp(n_factors=5)
        else:
            model = SVDpp()
        model.fit(data)
        for User in UserList:
            UserPointList = []
            for Fund in FundList:
                UserPointList.append(model.predict(User,Fund).est)
            RecommendList = np.argsort(UserPointList)[::-1][0:RecommendNum]
            for FundIndex in RecommendList:
                OutUserList.append(User)
                OutFundList.append(FundList[FundIndex])
    OutFrame = pd.DataFrame({"User":OutUserList,"RecommendFundCode":OutFundList})
    return OutFrame

# SVDPP线程函数
def SVDPPThreadFuc(Frame):
    OutUserList = []
    OutFundList = []
    Frame = Frame.loc[:,'User':'Point']
    UserList = Frame.User.unique()
    FundList = Frame.FundCode.unique()  
    reader = Reader(rating_scale=(0,2))
    data = Dataset.load_from_df(Frame, reader=reader).build_full_trainset()
    model = SVDpp()
    model.fit(data)
    for User in UserList:
        UserPointList = []
        for Fund in FundList:
            UserPointList.append(model.predict(User,Fund).est)
        RecommendList = np.argsort(UserPointList)[::-1][0:10]
        for FundIndex in RecommendList:
            OutUserList.append(User)
            OutFundList.append(FundList[FundIndex])
    OutFrame = pd.DataFrame({"User":OutUserList,"RecommendFundCode":OutFundList})
    return OutFrame

# SVDpp多线程改良版,由于python的多线程是假的多线程，所以这里的函数并未采用，只是提供思路
def SVDPPThread(PointFrame,TypeNum = 5,ThreadNum = 4):
    PointFrameList = []
    SVDResList = []
    # 拆分评分矩阵为5类：
    for Type in range(5):
        PointFrameList.append(PointFrame.ix[PointFrame.Type == Type])
    # 运用多线程技术对每一类用户分别评分：
    Executor = ThreadPoolExecutor(max_workers=ThreadNum) 
    AllTask = [Executor.submit(SVDPPThreadFuc, (Frame)) for Frame in PointFrameList]
    
    for future in as_completed(AllTask):
        SVDRes = future.result()
        SVDResList.append(SVDRes)
    OutFrame = pd.concat(SVDResList)
    return OutFrame





        


    































