import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import requests
import time
import random
# 分权随机函数
def WeightRand(weightlist):
    weight = random.randint(1,100)
    length = len(weightlist)
    for i in range(length):
        if weight <= weightlist[i]:
            return i
    return -1

# 读取基金列表
StockFrame = pd.read_csv("StockList.csv",dtype=str) 
AllocFrame = pd.read_csv("AllocList.csv",dtype=str)
BondFrame = pd.read_csv("BondList.csv",dtype=str)
CurrFrame = pd.read_csv("CurrList.csv",dtype=str)


UserNum = 2000
# 年龄
AgeStartList = [40,40,40,40,40]
AgeEndList = [44,43,46,60,50]
# 性别
SexWeightList = [61,68,64,60,61]
# 持有余额
RemainStartList = [40000,40000,80000,140000,70000]
RemainEndList = [60000,60000,100000,160000,90000]
# 消费者类型
TypeWeightList = [56,28,13,2,1]
# 开户时长
RegisterStartList = [23,31,31,8,25]
RegisterEndList = [27,35,35,12,29]
# 投资额度
InvestStartList = [2500,1500,4500,1500,7000]
InvestEndList = [5083,3739,9771,3718,14785]
# 投资频率
FrequencyStartList = [28,18,18,1,8]
FrequencyEndList = [32,22,22,1,12]
# 手续费
ChargeStartList = [600,300,400,900,800]
ChargeEndList = [1200,900,1200,2700,2600]
# 股票
StockWeightList = [95,28,35,2,10]
# 配置
AllocWeightList = [4,69,64,1,7]
# 债券
BondWeightList = [0,0,0,25,100]
# 货币
CurrWeightList = [0,1,0,2,0]
# 四种总和
FundWeightList = [StockWeightList,AllocWeightList,BondWeightList,CurrWeightList]
# 认购
RgWeightList = [41,3,92,99,14]
# 申购
SgWeightList = [25,30,4,1,50]
# 定投
DtWeightList = [22,37,4,0,17]
# 三种总和
WayWeightList = [RgWeightList,SgWeightList,DtWeightList]
# 两个月不行，有些用户根本没买，换成九个月！用户数量削减
StartDate = (2018,1,1,0,0,0,0,0,0)             
EndDate = (2018,8,31,23,59,59,0,0,0)    

start=time.mktime(StartDate)    #生成开始时间戳
end=time.mktime(EndDate)        #生成结束时间戳

StockCodeList = StockFrame["FundCode"].to_list()[0:-200] # 选择购买基金显示方式：可以修改name为你选定数据源的任意属性
AllocCodeList = AllocFrame["FundCode"].to_list()[0:-3000]
BondCodeList = BondFrame["FundCode"].to_list()[0:-1500]
CurrCodeList = CurrFrame["FundCode"].to_list()[0:-400]
FundCodeList = [StockCodeList,AllocCodeList,BondCodeList,CurrCodeList]

TypeCategory = ["C1","C3","C2","C5","C4"]
SexCategory = ["男","女"]
FundCategory = ["股票型","混合型","债券型","货币型"]
WayCategory = ["认购","申购","定投"]



UserList = []
AgeList = []
SexList = []
RegisterList = []
RemainList = []
TypeList = []
BuyList = []
CategoryList = []
WayList = []
TimeList = []
MoneyList = []
ChargeList = []

for UserCode in range(UserNum):  #UserNum
    weight = random.randint(1,100)  # 随机权重
    InvestNum = 1 
    weightlist = [sum(TypeWeightList[0:i+1]) for i in range(5)]
    Type = WeightRand(weightlist)
    InvestNum = random.randint(FrequencyStartList[Type],FrequencyEndList[Type])
    weightlist = [SexWeightList[Type],100]
    Sex = WeightRand(weightlist)
    Age = random.randint(AgeStartList[Type],AgeEndList[Type])
    Remain = random.randint(RemainStartList[Type],RemainEndList[Type])
    Register = random.randint(RegisterStartList[Type],RegisterEndList[Type])
    for i in range (1,InvestNum+1):
        UserList.append(UserCode)
        AgeList.append(Age)
        SexList.append(SexCategory[Sex])
        RegisterList.append(Register)
        RemainList.append(Remain)
        TypeList.append(TypeCategory[Type])
        # 手续费
        Charge = random.randint(ChargeStartList[Type],ChargeEndList[Type])
        ChargeList.append(Charge)
        # 随机基金种类
        weightlist=[]
        ans=0
        for j in range (4):
            ans = ans + FundWeightList[j][Type]
            weightlist.append(ans)
        CategoryIndex = WeightRand(weightlist)
        if CategoryIndex == -1:
            CategoryList.append("其他")
        else:
            CategoryList.append(FundCategory[CategoryIndex])
        index = random.randint(0,len(FundCodeList[CategoryIndex])-1)    
        FundCode =  FundCodeList[CategoryIndex][index]
        BuyList.append(FundCode)
        # 随机时间
        t=random.randint(start,end)    
        date_touple=time.localtime(t)          
        date=time.strftime("%Y-%m-%d",date_touple)
        TimeList.append(str(date))
        # 随机投资金额
        Money = random.randint(InvestStartList[Type],InvestEndList[Type])
        MoneyList.append(Money)
        # 投资方式
        weightlist = []
        ans = 0
        for j in range (3):
            ans = ans + WayWeightList[j][Type]
            weightlist.append(ans)
        index = WeightRand(weightlist)
        if index == -1:
            WayList.append("其他")
        else:
            WayList.append(WayCategory[index])


TrainData = pd.DataFrame({"用户编码":UserList,"用户类型":TypeList,"性别":SexList,"开户时长":RegisterList,"帐户余额":RemainList,"年龄":AgeList,"基金代码":BuyList,"基金类型":CategoryList,"投资时间":TimeList,"投资金额":MoneyList,"投资方式":WayList,"手续费":ChargeList})
List = TrainData.loc[(TrainData.基金类型 == "债券型") | (TrainData.基金类型 == "货币型") | (TrainData.基金类型 == "混合型") | (TrainData.基金类型 == "股票型")]
List.to_csv("TrainData.csv",encoding="utf_8_sig")





