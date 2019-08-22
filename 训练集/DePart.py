import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import requests

df = pd.read_csv("基金列表_Final.csv",dtype=str)
BondList = df.ix[df.type == "债券型"]
CurrList = df.ix[df.type == "货币型"]
AllocList = df.ix[df.type == "混合型"]
StockList = df.ix[df.type == "股票型"]
BondList.to_csv("BondList.csv",encoding="utf_8_sig")
CurrList.to_csv("CurrList.csv",encoding="utf_8_sig")
AllocList.to_csv("AllocList.csv",encoding="utf_8_sig")
StockList.to_csv("StockList.csv",encoding="utf_8_sig")

