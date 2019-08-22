def Str2Float(length, fundList, colunmName):
    for i in range(length):
        str1 = fundList.loc[i, colunmName].strip("%")
        if str1 == "--":
            continue
        monthFloat = float(str1) / 100
        monthFloat_2 = round(monthFloat, 4)
        fundList.loc[i, colunmName] = monthFloat_2


def EigenVector(fundList, outEncoding, outpathFile):
    print("\n生成中……")
    length = len(fundList)
    # 类型：
    # 股票型：1
    # 债券型：2
    # 货币型：3
    # 混合型：4
    fundList.loc[fundList.类型 == "混合型", "类型"] = 4
    fundList.loc[fundList.类型 == "货币型", "类型"] = 3
    fundList.loc[fundList.类型 == "债券型", "类型"] = 2
    fundList.loc[fundList.类型 == "股票型", "类型"] = 1

    # 收益转为float型
    Str2Float(length, fundList, "近1月收益")
    Str2Float(length, fundList, "近1年收益")
    Str2Float(length, fundList, "近3年收益")
    # 风险等级
    # 无：1
    # 低：2
    # 中：3
    # 高：4
    # 中高：5
    # 中底：6
    fundList.loc[fundList.风险等级 == "低风险", "风险等级"] = 2
    fundList.loc[fundList.风险等级 == "中风险", "风险等级"] = 3
    fundList.loc[fundList.风险等级 == "高风险", "风险等级"] = 4
    fundList.loc[fundList.风险等级 == "中高风险", "风险等级"] = 5
    fundList.loc[fundList.风险等级 == "中低风险", "风险等级"] = 6
    fundList.loc[fundList.风险等级 == "无", "风险等级"] = 1

    # 基金规模转为float，单位为亿元
    fundScaleFloat = fundList["基金规模"].str.strip("亿元").astype(float)
    fundList["基金规模"] = fundScaleFloat
    fundList.to_csv(outpathFile, encoding=outEncoding)
