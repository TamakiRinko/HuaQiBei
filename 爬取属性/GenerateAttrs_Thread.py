import requests
from bs4 import BeautifulSoup
import traceback
import re
import threading
from multiprocessing.dummy import Pool as ThreadPool
import pandas as pd
import 爬取属性.GenerateEigen
import 爬取属性.Merge

outpathFile = "../基金列表及属性/基金属性.csv"
outpathFileString = "../基金列表及属性/基金属性_字符串.csv"
inpathFile = "../基金列表及属性/基金列表_四种类型.csv"
stock_info_url = "http://fund.eastmoney.com/"
outEncoding = "utf_8_sig"
inEncoding = "utf_8_sig"
infoList = []
counts = 0
Length = 0
# threads = []
threadLock = threading.Lock()


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
    # fundName = fundList.name
    fundType = fundList.type
    print("lenOfFundCode: %d" % len(fundCode))
    for i in range(len(fundCode)):
        lst.append([str(fundCode[i]).zfill(6), fundType[i]])    # 基金fundCode补全为6位


def getStockInfo(stock):
    global counts   # 使用全局变量counts
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
                         stock[0],
                         stock[1],
                         str(earningMonth.string),      # NavigableString强转成str，否则极占内存
                         str(earningYear.string),
                         str(earningThreeYear.string),
                         riskLevelStr,
                         re.search(r'[0-9].*(亿元)', scaleOfFund.string).group(0)])
        counts = counts + 1
        print("\r当前进度：{:.2f}%".format(counts * 100 / Length), end="")   # 显示进度
        threadLock.release()
    except:
        threadLock.acquire()
        counts = counts + 1
        print("\r当前进度：{:.2f}%".format(counts * 100 / Length), end="")
        threadLock.release()
        # traceback.print_exc()
        return


# 控制线程数
def threadGetStockInfo(lst):
    pool = ThreadPool(10)
    pool.map(getStockInfo, lst)
    pool.close()
    pool.join()


def main():
    global Length
    # fundList = pd.read_csv(inpathFile, encoding=inEncoding)
    fundList = 爬取属性.Merge.merge()
    print(fundList)
    slist = []
    getStockList(slist, fundList)
    Length = len(slist)
    threadGetStockInfo(slist)
    FundFrame = pd.DataFrame(infoList, columns=["FundCode", "类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"])
    # FundFrame.sort_values("FundCode", inplace=True)     # 按FundCode排序
    # FundFrame.reset_index(drop=True, inplace=True)      # 行号换回0~n
    FundFrame.to_csv(outpathFileString, encoding=outEncoding, index=False)   # 初始文件保留
    爬取属性.GenerateEigen.EigenVector(FundFrame, outEncoding, outpathFile)


if __name__ == '__main__':
    main()
