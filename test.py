import investpy
from alpha_vantage.timeseries import TimeSeries
import config
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np

# ts = TimeSeries(key=config.API_alpha_vantage, output_format='pandas')
# data, meta_data = ts.get_intraday(symbol='T', interval='1min', outputsize='full')
# data.index = pd.DatetimeIndex(data.index) + timedelta(hours=3, minutes=58)




def main():
    high_data = []
    low_data = []
    current_date = str(date.today().day) + '/' + \
                        str(date.today().month) + '/' + str(date.today().year)
    a = date.today().month

    if a == 1:
        from_date = str(date.today().day) + '/' + str(12) + \
                         '/' + str(date.today().year - 1)
    else:
        from_date = str(date.today().day) + '/' + \
                         str(date.today().month - 1) + '/' + str(date.today().year)


    df = investpy.get_stock_historical_data(
        stock='ACNB', country=config.COUNTRY, from_date=from_date, to_date=current_date)

    open_data = [float(np.array(df['Open'][-5:][4])), float(np.array(df['Open'][-5:][3])),
                 float(np.array(df['Open'][-5:][2])), float(np.array(df['Open'][-5:][1]))]

    ts = TimeSeries(key=config.API_alpha_vantage, output_format='pandas')
    data, meta_data = ts.get_intraday(symbol='ACNB', interval='5min', outputsize='full')
    data.index = pd.DatetimeIndex(data.index) + timedelta(hours=3, minutes=58)

    # open = [29.86, 29.79, 29.89, 29.55]
    for index, value in enumerate(open_data):
        high, low = get_stock_intraday(ts=ts, open=value, interval=1, index=index, date=data)
        print(high)
        print(low)
        high_data.append(high)
        low_data.append(low)

    print(high_data)
    print(low_data)

def get_stock_intraday(ts, open, interval, index, date):
    data =date


    high_data = []
    low_data = []
    is_date = True


    # count = ct
    is_date_count = 0

    while is_date:
        last_current_date = (data.index[0] - timedelta(days=index)).date()
        # current_date = str((pd.Timestamp.now() - timedelta(days=1)).date())
        result_data = data.loc[str(last_current_date):str(last_current_date)]
        if len(result_data) == 0:
            # count += 1
            pass
        else:
            print(result_data)
            print(len(result_data))
            print(result_data.index[0])
            print(open)

            is_date_count += 1
            # count += 1
            percent_2 = open + (open * .02)
            percent_1_5 = open + (open * .015)
            percent_1 = open + (open * .01)
            percent_0_5 = open + (open * .005)
            percent_m_0_2 = open - (open * .002)
            percent_m_0_3 = open - (open * .003)
            percent_m_0_4 = open - (open * .004)
            percent_m_0_5 = open - (open * .005)


            print('up')
            print(percent_2)
            print(percent_1_5)
            print(percent_1)
            print(percent_0_5)
            print('low')
            print(percent_m_0_2)
            print(percent_m_0_3)
            print(percent_m_0_4)
            print(percent_m_0_5)



            open_percent_0_5 = len(
                result_data.where((result_data['2. high'] > open) & (result_data['2. high'] <= percent_0_5)).dropna())
            percent_0_5_percent_1 = len(
                result_data.where(
                    (result_data['2. high'] > percent_0_5) & (result_data['2. high'] <= percent_1)).dropna())
            percent_1_percent_1_5 = len(
                result_data.where(
                    (result_data['2. high'] > percent_1) & (result_data['2. high'] <= percent_1_5)).dropna())
            percent_1_5_percent_2 = len(
                result_data.where(
                    (result_data['2. high'] > percent_1_5) & (result_data['2. high'] <= percent_2)).dropna())
            percent_2_over = len(result_data.where(result_data['2. high'] > percent_2).dropna())

            open_percent_m_0_2 = len(
                result_data.where((result_data['3. low'] < open) & (result_data['3. low'] >= percent_m_0_2)).dropna())
            percent_m_0_2_percent_m_0_3 = len(
                result_data.where(
                    (result_data['3. low'] < percent_m_0_2) & (result_data['3. low'] >= percent_m_0_3)).dropna())
            percent_m_0_3_percent_m_0_4 = len(
                result_data.where(
                    (result_data['3. low'] < percent_m_0_3) & (result_data['3. low'] >= percent_m_0_4)).dropna())
            percent_m_0_4_percent_m_0_5 = len(
                result_data.where(
                    (result_data['3. low'] < percent_m_0_4) & (result_data['3. low'] >= percent_m_0_5)).dropna())
            percent_m_0_5_less = len(result_data.where(result_data['3. low'] <= percent_m_0_5).dropna())

            high = [open_percent_0_5, percent_0_5_percent_1, percent_1_percent_1_5, percent_1_5_percent_2,
                    percent_2_over]
            low = [open_percent_m_0_2, percent_m_0_2_percent_m_0_3, percent_m_0_3_percent_m_0_4,
                   percent_m_0_4_percent_m_0_5,
                   percent_m_0_5_less]
            high_data.append(high)
            low_data.append(low)
            print('high')
            print(open_percent_0_5, percent_0_5_percent_1, percent_1_percent_1_5, percent_1_5_percent_2, percent_2_over)
            print('low')
            print(open_percent_m_0_2, percent_m_0_2_percent_m_0_3, percent_m_0_3_percent_m_0_4,
                  percent_m_0_4_percent_m_0_5,
                  percent_m_0_5_less)

        if is_date_count == interval:
            is_date = False
    return high_data, low_data


if __name__ == '__main__':
    main()
