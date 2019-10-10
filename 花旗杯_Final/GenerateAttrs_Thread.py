import requests
from bs4 import BeautifulSoup
import re
import threading
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import GenerateEigen
import Merge

pathIndex = ""
outpathFile = "基金属性"
# outpathFileString = "../基金列表及属性/基金属性_字符串"
# inpathFile = "../基金列表及属性/基金列表_四种类型.csv"
stock_info_url = "http://fund.eastmoney.com/"
outEncoding = "utf-8"
infoList = []
counts = 0
Length = 0
threadLock = threading.Lock()
# 没有属性的基金
# wrongFundList = []


def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url, timeout=2)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""


# 获得基金列表，后续使用
def getStockList(lst, fundList):
    fundCode = fundList.FundCode
    fundType = fundList.type
    # print("lenOfFundCode: %d" % len(fundCode))
    for i in range(len(fundCode)):
        lst.append([str(fundCode[i]).zfill(6), fundType[i]])    # 基金fundCode补全为6位


def getStockInfo(stock):
    global counts   # 使用全局变量counts
    global infoList
    # global wrongFundList
    url = stock_info_url + stock[0] + ".html"
    html = getHTMLText(url)
    # print(url)
    try:
        if html == "":
            return
        soup = BeautifulSoup(html, "html.parser")
        # 考虑的属性：
        #     类型
        #     近1月收益
        #     近1年收益
        #     近3年收益
        #     风险等级
        #     基金规模
        stockInfo = soup.find("div", attrs={"class": "fundInfoItem"})
        earningMonth = (stockInfo.find("span", string="近1月：")).next_sibling
        earningYear = (stockInfo.find("span", string="近1年：")).next_sibling
        earningThreeYear = (stockInfo.find("span", string="近3年：")).next_sibling
        kindOfFund = stockInfo.find("td")
        riskLevel = kindOfFund.a.next_sibling
        if riskLevel == None:
            riskLevelStr = "无"
        else:
            riskLevelStr = re.search(r'[中低高][高低]*(风险)', riskLevel.string).group(0)
        scaleOfFund = kindOfFund.next_sibling.a.next_sibling
        threadLock.acquire()
        infoList.append([
                         int(stock[0]),
                         stock[1],
                         str(earningMonth.string),      # NavigableString强转成str，否则极占内存
                         str(earningYear.string),
                         str(earningThreeYear.string),
                         riskLevelStr,
                         re.search(r'[0-9].*(亿元)', scaleOfFund.string).group(0)])
        counts = counts + 1
        # print("\r当前进度：{:.2f}%".format(counts * 100 / Length), end="")   # 显示进度
        threadLock.release()
    except:
        threadLock.acquire()
        # wrongFundList.append(stock[0])  # 无法获取属性的基金
        counts = counts + 1
        # print("\r当前进度：{:.2f}%".format(counts * 100 / Length), end="")
        threadLock.release()
        return


# 控制线程数
def threadGetStockInfo(lst):
    # print("爬取属性")
    pool = ThreadPool(16)
    pool.map(getStockInfo, lst)
    pool.close()
    pool.join()


def main(fundRecordFrame):
    global Length
    global infoList
    global counts
    # global wrongFundList
    fundList = Merge.merge(fundRecordFrame)
    # 最终能够拿到属性的基金列表
    # fundFrameFinal = pd.read_csv(pathIndex + inPath[0:-4] + "_2.csv", encoding=inEncode)
    # 基金编号及类型List
    slist = []
    getStockList(slist, fundList)
    Length = len(slist)
    # 多线程爬取
    threadGetStockInfo(slist)
    # 将获得不到属性的基金删除
    # for stock in wrongFundList:
    #     print(float(stock))
    #     fundFrameFinal = fundFrameFinal.drop(fundFrameFinal.loc[fundFrameFinal.FundCode == float(stock)].index[0], axis=0)
    # fundFrameFinal.rename(columns={"FundCode": "基金编号(此值唯一)", "type": "类型"}, inplace=True)
    # fundFrameFinal.to_csv(pathIndex + inPath[0:-4] + "_2.csv", encoding="utf-8", index=False)
    FundFrame = pd.DataFrame(infoList, columns=["FundCode", "类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"])
    # FundFrame.sort_values("FundCode", inplace=True)     # 按FundCode排序
    # FundFrame.reset_index(drop=True, inplace=True)      # 行号换回0~n

    # 数值化并z-score标准化
    fundListFinal = GenerateEigen.EigenVector(FundFrame)
    infoList = []
    # wrongFundList = []
    counts = 0
    Length = 0
    return fundListFinal
