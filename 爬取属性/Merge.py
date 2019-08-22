import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import requests

df = pd.read_csv("../基金列表及属性/基金列表.csv",dtype=str)
List = df.loc[(df.type == "债券型") | (df.type == "货币型") | (df.type == "混合型") | (df.type == "股票型")]
List.to_csv("../基金列表及属性/基金列表_四种类型.csv", encoding="utf_8_sig")