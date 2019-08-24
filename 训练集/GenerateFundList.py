import pandas as pd

pathIndex = "../基金列表及属性/"
inpathFile = pathIndex + "基金属性_字符串.csv"

fundAttrs = pd.read_csv(inpathFile)
fundList = fundAttrs[["FundCode", "类型"]]
BondList = fundList.loc[fundList.类型 == "债券型"]
CurrList = fundList.loc[fundList.类型 == "货币型"]
AllocList = fundList.loc[fundList.类型 == "混合型"]
StockList = fundList.loc[fundList.类型 == "股票型"]
BondList.to_csv(pathIndex + "BondList.csv",encoding="utf_8_sig")
CurrList.to_csv(pathIndex + "CurrList.csv",encoding="utf_8_sig")
AllocList.to_csv(pathIndex + "AllocList.csv",encoding="utf_8_sig")
StockList.to_csv(pathIndex + "StockList.csv",encoding="utf_8_sig")
