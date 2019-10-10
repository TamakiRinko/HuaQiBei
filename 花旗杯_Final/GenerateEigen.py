from sklearn import preprocessing
import pandas as pd

def Str2Float(length, fundList, colunmName):
    for i in range(length):
        str1 = fundList.loc[i, colunmName].strip("%")
        if str1 == "--":
            fundList.loc[i, colunmName] = None      # 到Pandas中变为nan
            continue
        monthFloat = float(str1) / 100
        monthFloat_2 = round(monthFloat, 4)
        fundList.loc[i, colunmName] = monthFloat_2
    fundList[colunmName] = fundList[colunmName].astype(float)

def EigenVector(fundList):
    length = len(fundList)

    # 类型：
    # 股票指数，股票型：1
    # 债券指数，债券型：2
    # 货币型：3
    # 混合型：4
    fundList.loc[fundList.类型 == "混合型", "类型"] = 4.0
    fundList.loc[fundList.类型 == "货币型", "类型"] = 3.0
    fundList.loc[fundList.类型 == "债券型", "类型"] = 2.0
    fundList.loc[fundList.类型 == "股票型", "类型"] = 1.0
    fundList.loc[fundList.类型 == "债券指数", "类型"] = 2.0
    fundList.loc[fundList.类型 == "股票指数", "类型"] = 1.0

    # 收益转为float型
    Str2Float(length, fundList, "近1月收益")
    Str2Float(length, fundList, "近1年收益")
    Str2Float(length, fundList, "近3年收益")

    # 风险等级
    # 无：None
    # 低：2
    # 中：3
    # 高：4
    # 中高：5
    # 中底：6
    fundList.loc[fundList.风险等级 == "低风险", "风险等级"] = 2.0
    fundList.loc[fundList.风险等级 == "中风险", "风险等级"] = 3.0
    fundList.loc[fundList.风险等级 == "高风险", "风险等级"] = 4.0
    fundList.loc[fundList.风险等级 == "中高风险", "风险等级"] = 5.0
    fundList.loc[fundList.风险等级 == "中低风险", "风险等级"] = 6.0
    fundList.loc[fundList.风险等级 == "无", "风险等级"] = None

    # 基金规模转为float，单位为亿元
    fundScaleFloat = fundList["基金规模"].str.strip("亿元").astype(float)
    fundList["基金规模"] = fundScaleFloat

    # fundList.to_csv(outpathFile, encoding=outEncoding)

    # Z-score标准化
    fundList_2 = fundList[["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"]]
    fundList_2 = preprocessing.scale(fundList_2)
    fundList_2 = pd.DataFrame(fundList_2, columns=["类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"])
    fundList_2.insert(0, "FundCode", fundList["FundCode"])
    # print("\n股票属性生成完毕")
    return fundList_2
