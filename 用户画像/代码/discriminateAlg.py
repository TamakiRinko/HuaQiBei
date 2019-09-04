import pandas as pd
import numpy as np
import random
import sys
from sklearn import discriminant_analysis


def discriminate(directory, df):
    path = directory + "判别公式参数.csv"
    para = pd.read_csv(path, encoding='gbk', index_col=0)
    para = para.values.tolist()
    index = df.drop(['客户编号', '其他型占比'], axis=1)
    index = index.values.tolist()[0]
    # print(para)
    # print(index)
    # grp = np.dot(para, index)
    grp = -1
    delta = sys.maxsize
    for i in range(5):
        current = np.dot(index, para[i][1:7])
        current = current + para[i][7]
        if abs(current - para[i][0]) < delta:
            delta = abs(current - para[i][0])
            grp = para[i][0]

    if grp == -1:
        grp = random.randint(0, 4)
    # print(grp)
    return grp


def renew(directory):
    # path = directory + "判别公式参数.csv"
    # df = pd.DataFrame({"基金交易频率": [0], "最大交易金额": [0],
    #                    "混合型占比": [0], "债券指数或债券型占比": [0],
    #                    "货币型占比": [0], "股票指数或股票型占比": [0], "其他型占比": [0]})
    # df.to_csv(path, encoding='gbk')
    client = pd.read_csv(directory + '用户记录.csv', encoding='gbk', index_col=0)
    # x中不要加入其他型占比
    x = client[["基金交易频率", "最大交易金额", "混合型占比", "债券指数或债券型占比", "货币型占比", "股票指数或股票型占比"]]
    y = client['客户类别']
    lda = discriminant_analysis.LinearDiscriminantAnalysis()
    lda.fit(x, y)
    # print(x)
    # print(y)
    # print(lda.coef_)
    df = pd.DataFrame(data=lda.coef_, columns=["基金交易频率", "最大交易金额", "混合型占比", "债券指数或债券型占比", "货币型占比", "股票指数或股票型占比"])
    df['截距'] = lda.intercept_
    df.insert(0, '客户类别', lda.classes_)
    df.to_csv(directory + "判别公式参数.csv", encoding='gbk')
    return
