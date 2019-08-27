import pandas as pd


def merge():
    df = pd.read_csv("../基金列表及属性/旧基金.csv", encoding="gbk")
    List = df.loc[(df.类型 == "债券型") | (df.类型 == "货币型") | (df.类型 == "混合型")
                  | (df.类型 == "股票型") | (df.类型 == "股票指数") | (df.类型 == "债券指数")]
    partList = List[["基金编号(此值唯一)", "类型"]].copy()
    partList.rename(columns={"基金编号(此值唯一)": "FundCode", "类型": "type"}, inplace=True)
    partList.to_csv("../基金列表及属性/基金列表_四种类型.csv", encoding="utf_8_sig")


if __name__ == '__main__':
    merge()