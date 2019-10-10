import pandas as pd
import time
pathIndex = ""

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
    # print(FinalPointFrame)
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
    # print(FinalPointFrame)
    return FinalPointFrame


def Standardization_3(PointFrame):
    # 标准化
    UserValueCounts = PointFrame["User"].value_counts()
    pointLength = len(UserValueCounts)
    for i in range(pointLength):
        PointFrame.loc[PointFrame.User == UserValueCounts.index[i], "Point"] = PointFrame.loc[PointFrame.User == UserValueCounts.index[i], "Point"] / PointFrame.loc[PointFrame.User == UserValueCounts.index[i], "Point"].sum()
    # print(PointFrame)
    return PointFrame


def Standardization_4(PointFrame):
    # print("开始标准化")
    UserList = PointFrame["User"].unique()
    lenOfUserList = len(UserList)
    # 结果列表
    FinalPointList = []
    for i in range(lenOfUserList):
        # print("\r当前进度：{:.2f}%".format(i * 100 / lenOfUserList), end="")  # 显示进度
        # 取出特定用户的评分
        SubPointFrame = PointFrame.loc[PointFrame.User == UserList[i]].copy()
        # 标准化
        sumOfPoints = SubPointFrame["Point"].sum()
        SubPointFrame.loc[:, "Point"] = SubPointFrame.loc[:, "Point"] / sumOfPoints
        # 添加子DataFrame
        FinalPointList.append(SubPointFrame)
    # 由列表构造
    FinalPointFrame = pd.concat(FinalPointList)
    # print("\nPoint标准化完毕")
    # FinalPointFrame.to_csv(pathIndex + "Point_Standardized.csv", encoding="utf-8")
    return FinalPointFrame
