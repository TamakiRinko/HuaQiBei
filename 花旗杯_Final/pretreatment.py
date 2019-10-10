import pandas as pd
import datetime


def calculate_index(df):
    # 按客户编号排序
    df = df.sort_values(by=['客户编号'])
    df.reset_index(drop=True, inplace=True)
    # 获得交易记录总数
    row_n = df.shape[0]

    UserCodeList = []
    TradeFrequencyList = []
    MaxAmountList = []
    MixedFundProportionList = []
    BondFundProportionList = []
    CurrFundProportionList = []
    StockFundProportionList = []
    ExtraFundProportionList = []

    # 客户编码
    usercode = -1
    # 时长
    time_max = datetime.datetime.strptime('0001-1-1 00:00:00', '%Y-%m-%d %H:%M:%S')
    time_min = datetime.datetime.strptime('9999-12-31 23:59:59', '%Y-%m-%d %H:%M:%S')
    period = -1
    # 交易数
    trade_num = 0
    amount_max = -1
    # 股票型
    stock_n = 0
    # 混合型
    mixed_n = 0
    # 债券型
    bond_n = 0
    # 货币型
    curr_n = 0
    # 其他基金型
    extra_n = 0

    for index in range(row_n):
        if usercode != df['客户编号'][index]:
            if usercode >= 0:
                # 客户编号
                UserCodeList.append(usercode)
                # 交易频率
                period = (time_max - time_min).days + 1
                TradeFrequencyList.append(trade_num / period)
                # 最大交易额
                MaxAmountList.append(amount_max)
                # 混合型基金占比
                MixedFundProportionList.append(mixed_n / trade_num)
                # 债券型基金占比
                BondFundProportionList.append(bond_n / trade_num)
                # 货币型基金占比
                CurrFundProportionList.append(curr_n / trade_num)
                # 股票型基金占比
                StockFundProportionList.append(stock_n / trade_num)
                # 其他类型基金占比
                ExtraFundProportionList.append(extra_n / trade_num)
            usercode = df['客户编号'][index]
            time_max = datetime.datetime.strptime('0001-1-1 00:00:00', '%Y-%m-%d %H:%M:%S')
            time_min = datetime.datetime.strptime('9999-12-31 23:59:59', '%Y-%m-%d %H:%M:%S')
            amount_max = -1

            # 混合型
            mixed_n = 0
            # 债券型
            bond_n = 0
            # 货币型
            curr_n = 0
            # 股票型
            stock_n = 0
            # 其他基金型
            extra_n = 0
            # 交易数
            trade_num = 0

        temp = datetime.datetime.strptime(df['交易时间'][index], '%Y-%m-%d %H:%M:%S')
        if temp > time_max:
            time_max = temp
        elif temp < time_min:
            time_min = temp

        if amount_max < df['交易金额'][index]:
            amount_max = df['交易金额'][index]

        if ("股票型" == df['基金类型'][index]) | ("股票指数" == df['基金类型'][index]):
            stock_n = stock_n + 1
        elif "混合型" == df['基金类型'][index]:
            mixed_n = mixed_n + 1
        elif ("债券型" == df['基金类型'][index]) | ("债券指数" == df['基金类型'][index]):
            bond_n = bond_n + 1
        elif "货币型" == df['基金类型'][index]:
            curr_n = curr_n + 1
        else:
            extra_n = extra_n + 1
        trade_num = trade_num + 1

    UserCodeList.append(usercode)
    period = (time_max - time_min).days + 1
    TradeFrequencyList.append(trade_num / period)
    MaxAmountList.append(amount_max)
    StockFundProportionList.append(stock_n / trade_num)
    MixedFundProportionList.append(mixed_n / trade_num)
    BondFundProportionList.append(bond_n / trade_num)
    CurrFundProportionList.append(curr_n / trade_num)
    ExtraFundProportionList.append(extra_n / trade_num)

    data = pd.DataFrame({"客户编号": UserCodeList, "基金交易频率": TradeFrequencyList, "最大交易金额": MaxAmountList,
                         "混合型占比": MixedFundProportionList, "债券指数或债券型占比": BondFundProportionList,
                         "货币型占比": CurrFundProportionList, "股票指数或股票型占比": StockFundProportionList,
                         "其他型占比": ExtraFundProportionList})
    return data
