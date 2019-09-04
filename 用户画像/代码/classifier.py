import pandas as pd
import datetime
import numpy as np
from sklearn.cluster import KMeans
import 用户画像.代码.pretreatment
import 用户画像.代码.discriminateAlg

# directory = "REPLACE THIS VALUE"
# directory = "/Users/xiao/Desktop/数据集_结合软院/"
directory = "../../基金列表及属性/"
'''
+-----------------------------PART ONE------------------------------+

'''

# 1.读取当前用户交易记录
records_path = "当前用户交易记录.csv"
records = pd.read_csv(directory + records_path, encoding='gbk', index_col=0)
# 2.通过判别公式计算得其所属组号
index = 用户画像.代码.pretreatment.calculate_index(records)
grp_num = 用户画像.代码.discriminateAlg.discriminate(directory, index)

'''
+-----------------------------PART TWO------------------------------+

'''
# 1.将当前用户的信息保存至 用户记录.csv

# temp = pd.DataFrame({"客户编号": [], "基金交易频率": [], "最大交易金额": [],
#                      "混合型占比": [], "债券指数或债券型占比": [],
#                      "货币型占比": [], "股票指数或股票型占比": [],
#                      "其他型占比": [], "客户类别": []})
# temp.to_csv(directory+"用户记录.csv", encoding='gbk')
users_info = pd.read_csv(directory + "用户记录.csv", encoding='gbk', index_col=0)
user_cur = users_info[users_info['客户编号'] == index['客户编号'][0]]
if user_cur.empty:
    index['客户类别'] = grp_num
    users_info = users_info.append(index, ignore_index=True)
    users_info.to_csv(directory + '用户记录.csv', encoding='gbk')
else:
    index['客户类别'] = grp_num
    users_info.loc[users_info['客户编号'] == index['客户编号'][0]] = index.loc[0:1]
    users_info.to_csv(directory + '用户记录.csv', encoding='gbk')

# 2.将当前用户的交易记录加入其对应类别的交易记录(.csv)
classified = pd.read_csv(directory + "C" + str(1+int(grp_num)) + '.csv', encoding='gbk', index_col=0)
classified = classified.append(records, ignore_index=True)
classified.to_csv(directory + "C" + str(1+grp_num) + '.csv', encoding='gbk')

# 3.将当前用户的交易记录加入总交易记录中(.csv)
all_rcds = pd.read_csv(directory + "交易记录.csv", encoding='gbk', index_col=0)
all_rcds = all_rcds.append(records, ignore_index=True)
all_rcds.to_csv(directory + "交易记录.csv", encoding='gbk')

'''
+-----------------------------PART THREE------------------------------+

'''
# 当到达预定阈值（如一天，一周等）后重新进行聚类，此处为展示效果每次有新交易记录后都聚类
'''
client = pretreatment.calculate_index(all_rcds)
array = np.array(client)
clf = KMeans(n_clusters=5)
res = clf.fit_predict(array[:, 1:])
client['客户类别'] = res
client.to_csv(directory + '用户记录.csv', encoding='gbk')
'''
# 重新聚类后需计算判别公式参数
'''
discriminateAlg.renew(directory)
'''
