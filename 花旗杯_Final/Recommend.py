import pandas as pd
import heapq
import math
from sklearn.metrics.pairwise import cosine_similarity

def newFundRecommend(FavorAttr, newFundAttr):
    heap = []
    # 推荐数
    recommendNum = 10
    # 列表
    UserList = []
    FundList = []
    # 标识用户代号
    customer = 0
    # 已推荐个数
    recommended = 0
    # 进度
    k = 0
    length = len(newFundAttr)
    # print("生成推荐列表")

    for lineNew in newFundAttr.itertuples():
        # print("\r当前进度：{:.2f}%".format(k * 100 / length), end="")  # 显示进度
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
        for i in range(recommended):
            FundList.append(lineNew.FundCode)
            UserList.append(heap[i][0])
        heap = []
        customer = 0
        recommended = 0
        k = k + 1
    recommendFrame = pd.DataFrame({'User':UserList,'RecommendFundCode':FundList})
    # recommendFrame.to_csv(pathIndex + recommendFile, encoding="utf-8",index=False)
    # print("\n推荐列表生成完毕!")
    return recommendFrame

def FundRecommend(OldFrame,NewFrame):
    MergeFrame = pd.concat([OldFrame,NewFrame])
    MergeFrame = MergeFrame.sort_values(by=['User'])
    return MergeFrame

