import numpy as np
from sklearn.cluster import KMeans


def classify(df):
    array = np.array(df)
    clf = KMeans(n_clusters=5)
    res = clf.fit_predict(array[:, 1:])
    df['客户类别'] = res
    return df
