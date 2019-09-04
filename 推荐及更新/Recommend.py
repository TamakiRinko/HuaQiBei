import pandas as pd
import heapq
import math
import 评分矩阵.ReadPoint_csv
from sklearn.metrics.pairwise import cosine_similarity
pathIndex = "../基金列表及属性/"
recommendFile = "recommendFile.csv"

# 获得喜好向量
FavorAttr = 评分矩阵.ReadPoint_csv.main()
# 获得属性向量
newFundAttr = pd.read_csv(pathIndex + "基金属性_新基金2.0.csv", encoding="gbk")
heap = []
# 推荐数
recommendNum = 10
# 总推荐列表
recommendList = []
# 一个新基金的推荐列表
OneList = []
# 标识用户代号
customer = 0
# 已推荐个数
recommended = 0

for lineNew in newFundAttr.itertuples():
    for lineOld in FavorAttr.itertuples():
        list = []
        AttrNew = [lineNew.类型, lineNew.近1月收益, lineNew.近1年收益, lineNew.近3年收益, lineNew.风险等级, lineNew.基金规模]
        AttrOld = [lineOld.类型, lineOld.近1月收益, lineOld.近1年收益, lineOld.近3年收益, lineOld.风险等级, lineOld.基金规模]
        # 出现nan则不考虑该属性
        if math.isnan(lineNew.近1月收益) or math.isnan(lineOld.近1月收益):
            AttrNew.pop(-5)
            AttrOld.pop(-5)
        if math.isnan(lineNew.近1年收益) or math.isnan(lineOld.近1年收益):
            AttrNew.pop(-4)
            AttrOld.pop(-4)
        if math.isnan(lineNew.近3年收益) or math.isnan(lineOld.近3年收益):
            AttrNew.pop(-3)
            AttrOld.pop(-3)
        if math.isnan(lineNew.风险等级) or math.isnan(lineOld.风险等级):
            AttrNew.pop(-2)
            AttrOld.pop(-2)
        list.append(AttrNew)
        list.append(AttrOld)
        cosineSimilarity = cosine_similarity(list)[0][1]
        # 维护大小为10的最小堆，表示最大的10个相似度
        if recommended < recommendNum:
            heapq.heappush(heap, (customer, cosineSimilarity))
            recommended = recommended + 1
        elif heap[0][1] < cosineSimilarity:
            heapq.heapreplace(heap, (customer, cosineSimilarity))
        customer = customer + 1
    OneList.append(lineNew.FundCode)
    print(str(lineNew.FundCode) + "号基金被推荐给：")
    for i in range(recommended):
        print(str(heap[i][0]) + "号顾客！")
        OneList.append(str(heap[i][0]))
    recommendList.append(OneList)
    heap = []
    OneList = []
    customer = 0
    recommended = 0

recommendFrame = pd.DataFrame(recommendList)
recommendFrame.rename(columns={0:"FundCode"}, inplace=True)
recommendFrame.to_csv(pathIndex + recommendFile, encoding="gbk")
