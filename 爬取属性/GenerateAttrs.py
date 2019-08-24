import requests
from bs4 import BeautifulSoup
import traceback
import re
import pandas as pd
import 爬取属性.GenerateEigen

outpathFile = "../基金列表及属性/基金属性.csv"
inpathFile = "../基金列表及属性/基金列表_四种类型.csv"
outEncoding = "utf_8_sig"
inEncoding = "utf_8_sig"


def getHTMLText(url, code="utf-8"):
    try:
        r = requests.get(url, timeout=2)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except:
        return ""


def getStockList(lst, fundList):
    fundCode = fundList.FundCode
    fundName = fundList.name
    fundType = fundList.type
    # print(len(fundCode))
    for i in range(len(fundCode)):
        lst.append([str(fundCode[i]).zfill(6), fundName[i], fundType[i]])


def getStockInfo(lst, stockURL):
    count = 0
    infoList = []
    for stock in lst:
        url = stockURL + stock[0] + ".html"
        html = getHTMLText(url)
        # print(url)
        try:
            if html == "":
                continue
            soup = BeautifulSoup(html, "html.parser")

            stockInfo = soup.find("div", attrs={"class": "fundInfoItem"})
            # netWorth = stockInfo.find("span", id="gz_gsz")
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
            infoList.append([
                             stock[0],
                             stock[1],
                             stock[2],
                             # netWorth.string,
                             earningMonth.string,
                             earningYear.string,
                             earningThreeYear.string,
                             riskLevelStr,
                             re.search(r'[0-9].*(亿元)', scaleOfFund.string).group(0)])
            count = count + 1
            print("\r当前进度：{:.2f}%".format(count * 100 / len(lst)), end="")
        except:
            count = count + 1
            print("\r当前进度：{:.2f}%".format(count * 100 / len(lst)), end="")
            # traceback.print_exc()
            continue
    FundFrame = pd.DataFrame(infoList, columns=["FundCode", "名称", "类型", "近1月收益", "近1年收益", "近3年收益", "风险等级", "基金规模"])
    return FundFrame


def main():
    stock_info_url = "http://fund.eastmoney.com/"
    fundList = pd.read_csv(inpathFile, encoding=inEncoding)
    slist = []
    getStockList(slist, fundList)
    FundFrame = getStockInfo(slist, stock_info_url)
    爬取属性.GenerateEigen.EigenVector(FundFrame, outEncoding, outpathFile)


main()
