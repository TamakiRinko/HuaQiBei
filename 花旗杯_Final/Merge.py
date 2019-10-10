pathIndex = ""

def merge(fundRecordFrame):
    List = fundRecordFrame.loc[(fundRecordFrame.类型 == "债券型") | (fundRecordFrame.类型 == "货币型") | (fundRecordFrame.类型 == "混合型")
                  | (fundRecordFrame.类型 == "股票型") | (fundRecordFrame.类型 == "股票指数") | (fundRecordFrame.类型 == "债券指数")]
    partList = List[["基金编号(此值唯一)", "类型"]].copy()

    # 保存一份副本: 旧基金2.0_2.csv用于作为最后的可用基金
    # df2 = fundRecordFrame.copy()
    # df2.rename(columns={"基金编号(此值唯一)": "FundCode", "类型": "type"}, inplace=True)
    # df2.to_csv(pathIndex + inPath[0:-4] + "_2.csv", encoding=inEncode, index=False)

    partList.reset_index(inplace=True, drop=True)
    partList.rename(columns={"基金编号(此值唯一)": "FundCode", "类型": "type"}, inplace=True)
    partList["FundCode"] = partList["FundCode"].astype(int)     # FundCode为int
    return partList


if __name__ == '__main__':
    merge("旧基金2.0.csv", "utf-8")
    merge("新基金2.0.csv", "utf-8")
