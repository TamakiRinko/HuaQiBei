import pandas as pd
import random

# 定义文件地址
# directory = "/Users/xiao/Desktop/数据集_结合软院/"
# directory = "REPLACE THE VALUE"
directory = "../数据/"
FundListPath = directory + "旧基金2.0.csv"
TradeInfoPath = directory + "交易记录.csv"
ClassInfoPath = [directory + "C1.csv",
                 directory + "C2.csv",
                 directory + "C3.csv",
                 directory + "C4.csv",
                 directory + "C5.csv"]
# 定义编码格式，系统默认情况下，gbk for Windows utf-8 for macOS
Encoding = 'gbk'
# 读取文件
fund_df = pd.read_csv(FundListPath, encoding=Encoding)
# 清除空数据
fund_df = fund_df.dropna(axis=0, how="all")
row_n = fund_df.shape[0]

# 客户总数
ClientNum = 10000
# 客户编号
ClientCode = -1
# 占比 = 每类的客户数量/总客户数
ClientNumSize = [0.556, 0.2756, 0.1305, 0.0323, 0.0056]
# 交易时间
TradeTime = ["2016-04-07 10:25:09", "2016-04-27 10:25:09"]
TradePeriod = 20
# 交易频率
TradeFrequency = [2.81, 1.88, 1.93, 0.3, 0.74]
# 交易最大金额
MaxAmount = [5084, 3740, 9771, 3718, 14786]
# 基金占比
FundProp = [
    [95, 99, 0, 0, 100],
    [28, 97, 0, 98, 100],
    [35, 99, 0, 0, 100],
    [2, 3, 28, 30, 100],
    [10, 17, 77, 0, 100]
]


FundType = list(fund_df['类型'].unique())

# 客户编码列表
ClientCodeList = []
# 开户时长列表
TradePeriodList = []
# 交易金额列表
TradeAmountList = []
# 基金类型列表
FundTypeList = []
# 基金编码列表
FundCodeList = []

# print(fund_df['类型'].value_counts())
# 混合型基金
MixedFund = fund_df[fund_df['类型'] == '混合型']
# 债券指数或债券型基金
BondFund = fund_df[(fund_df['类型'] == '债券指数') | (fund_df['类型'] == '债券型')]
# 货币型基金
CurrFund = fund_df[fund_df['类型'] == '货币型']
# 股票指数或股票型基金
StockFund = fund_df[(fund_df['类型'] == '股票指数') | (fund_df['类型'] == '股票型')]
# 其他基金
ExtraFund = fund_df
ExtraFund = ExtraFund.drop(labels=MixedFund.axes[0])
ExtraFund = ExtraFund.drop(labels=BondFund.axes[0])
ExtraFund = ExtraFund.drop(labels=CurrFund.axes[0])
ExtraFund = ExtraFund.drop(labels=StockFund.axes[0])

FundCode = [
    list(MixedFund['基金编号(此值唯一)']),
    list(BondFund['基金编号(此值唯一)']),
    list(CurrFund['基金编号(此值唯一)']),
    list(StockFund['基金编号(此值唯一)']),
    list(ExtraFund['基金编号(此值唯一)'])
]

FundType = [
    list(MixedFund['类型']),
    list(BondFund['类型']),
    list(CurrFund['类型']),
    list(StockFund['类型']),
    list(ExtraFund['类型'])
]


AllData = pd.DataFrame({"客户编号": [], "交易时间": [], "交易金额": [], "基金类型": [], "基金编号": []})
AllData[['客户编号']] = AllData[['客户编号']].astype(int)

# print(ExtraFund['类型'].value_counts())

for i in range(5):
    client_n = int(ClientNum*ClientNumSize[i]*(1+random.uniform(-0.05, 0.05)))
    ClientCodeList.clear()
    TradePeriodList.clear()
    TradeAmountList.clear()
    FundTypeList.clear()
    FundCodeList.clear()
    # print("用户数:"+str(client_n))
    for j in range(client_n):
        TradeNum = int(TradePeriod*TradeFrequency[i]*(1+random.uniform(-0.05, 0.05)))
        ClientCode = ClientCode + 1
        # print("用户"+str(ClientCode)+":"+str(TradeNum))
        for k in range(TradeNum):
            ClientCodeList.append(ClientCode)
            TradePeriodList.append(TradeTime[random.randint(0, 1)])
            TradeAmountList.append(int(MaxAmount[i]*(1+random.uniform(-0.1, 0.1))))
            RandNum = random.randint(1, 100)
            if RandNum <= FundProp[i][0]:
                RandFund = random.randint(0, MixedFund.shape[0]-1)
                FundTypeList.append('混合型')
                FundCodeList.append(FundCode[0][RandFund])
                # FundCodeList.append(list(MixedFund['基金编号(此值唯一)'])[RandFund])
            elif RandNum <= FundProp[i][1]:
                RandFund = random.randint(0, BondFund.shape[0] - 1)
                FundTypeList.append(FundType[1][RandFund])
                FundCodeList.append(FundCode[1][RandFund])
                # FundCodeList.append(list(BondFund['基金编号(此值唯一)'])[RandFund])
            elif RandNum <= FundProp[i][2]:
                RandFund = random.randint(0, CurrFund.shape[0] - 1)
                FundTypeList.append(FundType[2][RandFund])
                FundCodeList.append(FundCode[2][RandFund])
                # FundCodeList.append(list(CurrFund['基金编号(此值唯一)'])[RandFund])
            elif RandNum <= FundProp[i][3]:
                RandFund = random.randint(0, StockFund.shape[0] - 1)
                FundTypeList.append(FundType[3][RandFund])
                FundCodeList.append(FundCode[3][RandFund])
                # FundCodeList.append(list(StockFund['基金编号(此值唯一)'])[RandFund])
            else:
                RandFund = random.randint(0, ExtraFund.shape[0] - 1)
                FundTypeList.append(FundType[4][RandFund])
                FundCodeList.append(FundCode[4][RandFund])
                # FundCodeList.append(list(ExtraFund['基金编号(此值唯一)'])[RandFund])

        # if ClientCode == 0:
        #     temp = pd.DataFrame({"客户编号": ClientCodeList, "交易时间": TradePeriodList, "交易金额": TradeAmountList,
        #                          "基金类型": FundTypeList, "基金编号": FundCodeList})
        #     temp.to_csv(directory + "当前用户交易记录.csv", encoding="gbk")

    Data = pd.DataFrame({"客户编号": ClientCodeList, "交易时间": TradePeriodList, "交易金额": TradeAmountList,
                         "基金类型": FundTypeList, "基金编号": FundCodeList})

    Data.to_csv(ClassInfoPath[i], encoding=Encoding)
    AllData = AllData.append(Data, ignore_index=True)
    # if i == 4:
    #     temp = pd.read_csv(ClassInfoPath[i], encoding=Encoding, index_col=0)
    #     print(temp['客户编号'])


AllData.to_csv(TradeInfoPath, encoding=Encoding)
