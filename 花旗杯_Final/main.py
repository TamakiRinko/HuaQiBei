import pandas as pd
import pretreatment
import classifier
import Recommend
import OldRecommend as OR
import GenerateAttrs_Thread as GA_T
import CreatePoint_csv as CP
import ReadPoint_csv as RP
import Standardization as SD
import warnings
warnings.filterwarnings('ignore')
directory = ""
recommendFile = "recommendFile.csv"

'''
+-----------------------------PART ONE 用户聚类------------------------------+

'''
# 读取所有交易记录
records = pd.read_csv(directory + "交易记录.csv", encoding='utf_8', index_col=0)
# 计算聚类指标
index = pretreatment.calculate_index(records)
# 用户聚类
client = classifier.classify(index)
# 将用户信息写入文件
client.to_csv(directory + '用户记录.csv', encoding='utf_8')
'''
+-----------------------------PART TWO 新基金推荐------------------------------+

'''
# 文件读
fundOld = pd.read_csv("旧基金2.0.csv", encoding="utf-8")
fundNew = pd.read_csv("新基金2.0.csv", encoding="utf-8")
RawData = pd.read_csv("用户记录.csv", encoding='utf-8')
TradeFrame = pd.read_csv("交易记录.csv", encoding='utf-8')

# 爬取基金属性
eigenvectorOld = GA_T.main(fundOld)     # 旧基金属性
eigenvectorNew = GA_T.main(fundNew)     # 新基金属性
# eigenvectorOld.to_csv("基金属性_旧基金2.0.csv", encoding="utf-8", index=False)
# eigenvectorNew.to_csv("基金属性_新基金2.0.csv", encoding="utf-8", index=False)
# eigenvectorOld = pd.read_csv("基金属性_旧基金2.0.csv", encoding="utf-8")
# eigenvectorNew = pd.read_csv("基金属性_新基金2.0.csv", encoding="utf-8")

# 生成评分
PointCSV = CP.createPoint(RawData, TradeFrame)  # 评分
PointCSV = SD.Standardization_4(PointCSV)
PointCSV.to_csv(directory + 'Point.csv', encoding="utf-8", index=False)
# PointCSV = pd.read_csv(directory + "Point.csv", encoding="utf-8")

# 生成喜好向量
FavorFrame = RP.main(PointCSV, eigenvectorOld)  # 喜好向量
# FavorFrame.to_csv("FavorFrame.csv", encoding="utf-8", index=False)
# FavorFrame = pd.read_csv("FavorFrame.csv", encoding="utf-8")

# 生成新基金推荐列表
recommendFrame = Recommend.newFundRecommend(FavorFrame, eigenvectorNew)     # 新基金推荐列表
recommendFrame.to_csv(directory + recommendFile, encoding="utf-8", index=False)
# print("New Fund Recommend Success!")
'''
+-----------------------------PART Three 旧基金推荐------------------------------+

'''
# 读取评分矩阵
PointFrame = pd.read_csv('Point.csv')
# 生成旧基金推荐列表
OldFundFrame = OR.SVDPP(PointFrame)
OldFundFrame.to_csv("RecommendList.csv", encoding='utf-8',index=False)
# print("Old Fund Recommend Success!")
'''
+-----------------------------PART Four 新旧基金整合------------------------------+

'''
# 整合新旧基金
newFundFrame = pd.read_csv("recommendFile.csv",encoding='utf-8')
Frame = Recommend.FundRecommend(OldFundFrame,newFundFrame)
Frame.to_csv("RecommendRes.csv",encoding='utf-8',index=False)
# print("Over!")
