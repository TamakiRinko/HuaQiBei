import pandas as pd
import time

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


def main(PointFrame):
    start = time.process_time()
    Standardization_1(PointFrame)      # Fastest
    end = time.process_time()
    print(str(end - start))
    start = time.process_time()
    Standardization_2(PointFrame)
    end = time.process_time()
    print(str(end - start))
    start = time.process_time()
    Standardization_3(PointFrame)
    end = time.process_time()
    print(str(end - start))

