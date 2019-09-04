import pandas as pd
import time
pathIndex = "../基金列表及属性/"

def Standardization_1(PointFrame):
    # 标准化
    FrameList = []
    # UserValueCounts = PointFrame["User"].value_counts()
    UserList = PointFrame["User"].unique()
    lenOfUserList = len(UserList)

    FinalPointList = []     # 结果列表
    for i in range(lenOfUserList):
        SubPointFrame = PointFrame[PointFrame["User"].isin([UserList[i]])].copy()  # 没有copy()则会报SettingWithCopyWarning
        sumOfPoints = SubPointFrame["Point"].sum()
        SubPointFrame.loc[:, "Point"] = SubPointFrame.loc[:, "Point"] / sumOfPoints
        FinalPointList.append(SubPointFrame)        # 添加子DataFrame
    FinalPointFrame = pd.concat(FinalPointList)     # 由列表构造
    print(FinalPointFrame)
    return FinalPointFrame
    # print(FinalPointFrame)


def Standardization_2(PointFrame):
    # 标准化
    # UserValueCounts = PointFrame["User"].value_counts()
    UserList = PointFrame["User"].unique()
    lenOfUserList = len(UserList)

    FinalPointFrame = pd.DataFrame()
    for i in range(lenOfUserList):
        SubPointFrame = PointFrame[PointFrame["User"].isin([UserList[i]])].copy()  # 没有copy()则会报SettingWithCopyWarning
        sumOfPoints = SubPointFrame["Point"].sum()
        SubPointFrame.loc[:, "Point"] = SubPointFrame.loc[:, "Point"] / sumOfPoints
        FinalPointFrame = FinalPointFrame.append(SubPointFrame)     # 直接append
    print(FinalPointFrame)
    return FinalPointFrame


def Standardization_3(PointFrame):
    # 标准化
    UserValueCounts = PointFrame["User"].value_counts()
    pointLength = len(UserValueCounts)
    for i in range(pointLength):
        PointFrame.loc[PointFrame.User == UserValueCounts.index[i], "Point"] = PointFrame.loc[PointFrame.User == UserValueCounts.index[i], "Point"] / PointFrame.loc[PointFrame.User == UserValueCounts.index[i], "Point"].sum()
    print(PointFrame)
    return PointFrame


def Standardization_4(PointFrame):
    UserList = PointFrame["User"].unique()
    lenOfUserList = len(UserList)
    # 结果列表
    FinalPointList = []
    for i in range(lenOfUserList):
        # 取出特定用户的评分
        SubPointFrame = PointFrame.loc[PointFrame.User == UserList[i]].copy()
        # 标准化
        sumOfPoints = SubPointFrame["Point"].sum()
        SubPointFrame.loc[:, "Point"] = SubPointFrame.loc[:, "Point"] / sumOfPoints
        # 添加子DataFrame
        FinalPointList.append(SubPointFrame)
    # 由列表构造
    FinalPointFrame = pd.concat(FinalPointList)
    # FinalPointFrame.to_csv(pathIndex + "Point_Standardized.csv", encoding="gbk")
    return FinalPointFrame


def main(PointFrame):
    start = time.process_time()
    Standardization_1(PointFrame)
    end = time.process_time()
    print(str(end - start))
    # start = time.process_time()
    # Standardization_2(PointFrame)
    # end = time.process_time()
    # print(str(end - start))
    # start = time.process_time()
    # Standardization_3(PointFrame)
    # end = time.process_time()
    # print(str(end - start))
    start = time.process_time()
    Standardization_4(PointFrame)      # Fastest
    end = time.process_time()
    print(str(end - start))


if __name__ == '__main__':
    PointFrame = pd.read_csv("../基金列表及属性/Point_2.csv")
    main(PointFrame)