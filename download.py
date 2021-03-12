import investpy
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
import time
from alpha_vantage.timeseries import TimeSeries

import requests
from fake_useragent import UserAgent
from lxml import html
from tqdm import tqdm


class Parser:
    """
    provider ticker stocks exchange
    """

    def __init__(self, country, min_buy, max_buy, config_a_vil):
        self.config_a_vil = config_a_vil
        self.max_buy = max_buy
        self.min_buy = min_buy
        self.country = country

        self.current_date = str(date.today().day) + '/' + \
                            str(date.today().month) + '/' + str(date.today().year)
        a = date.today().month

        if a == 1:
            self.from_date = str(date.today().day) + '/' + str(12) + \
                             '/' + str(date.today().year - 1)
        else:
            self.from_date = str(date.today().day) + '/' + \
                             str(date.today().month - 1) + '/' + str(date.today().year)

        self.ts = TimeSeries(key=self.config_a_vil, output_format='pandas')

    def create_data_ticker_min_max_by_close(self):
        data = pd.DataFrame(columns=['TICKER', 'CLOSE'])
        stocks = investpy.stocks.get_stocks(country=self.country)['symbol']

        for stock in tqdm(stocks, desc=f'create data tickers for all data {self.country} stocks exchange: '):
            try:
                df = investpy.get_stock_historical_data(
                    stock=stock, country=self.country, from_date=self.from_date, to_date=self.current_date)
                data = data.append({
                    'TICKER': stock,
                    'CLOSE': df['Close'][-1]
                }, ignore_index=True)
            except:
                continue
                # print(f'stock: {stock}, information unavailable or not found.')
            # time.sleep(2)
        data.to_excel('data.xlsx', index=True, header=True)

    def search_relevant_ticker(self):
        data_stocks = pd.read_excel('data.xlsx', index_col=False)[['TICKER', 'CLOSE']]
        stocks = data_stocks.where(
            (data_stocks['CLOSE'] >= self.min_buy) & (data_stocks['CLOSE'] <= self.max_buy)).dropna()

        data_ticker = pd.DataFrame(columns=[
            'TICKER', 'Tech_buy', 'Tech_sell', 'SMA_buy', 'SMA_sell', 'SMA_20', 'SMA_100', 'EMA_buy', 'EMA_sell',
            'EMA_20',
            'EMA_100', 'CLOSE_prev',
            'Percentage_1', 'p1_Op_0,5_up', 'p1_0,5_1.0_up', 'p1_1,0_1,5_up', 'p1_1,5_2,0_up', 'p1_2,0_over_up',
            'p1_Op_0,2_dwn', 'p1_0,2_0,3_dwn', 'p1_0,3_0,4_dwn', 'p1_0,4_0,5_dwn', 'p1_0,5_dwn,less',
            'Percentage_2', 'p2_Op_0,5_up', 'p2_0,5_1.0_up', 'p2_1,0_1,5_up', 'p2_1,5_2,0_up', 'p2_2,0_over_up',
            'p2_Op_0,2_dwn', 'p2_0,2_0,3_dwn', 'p2_0,3_0,4_dwn', 'p2_0,4_0,5_dwn', 'p2_0,5_dwn,less',
            'Percentage_3', 'p3_Op_0,5_up', 'p3_0,5_1.0_up', 'p3_1,0_1,5_up', 'p3_1,5_2,0_up', 'p3_2,0_over_up',
            'p3_Op_0,2_dwn', 'p3_0,2_0,3_dwn', 'p3_0,3_0,4_dwn', 'p3_0,4_0,5_dwn', 'p3_0,5_dwn,less',
            'Percentage_4', 'p4_Op_0,5_up', 'p4_0,5_1.0_up', 'p4_1,0_1,5_up', 'p4_1,5_2,0_up', 'p4_2,0_over_up',
            'p4_Op_0,2_dwn', 'p4_0,2_0,3_dwn', 'p4_0,3_0,4_dwn', 'p4_0,4_0,5_dwn', 'p4_0,5_dwn,less',
            'Open_point', 'High_point', 'Exchange'
        ])
        counter = 0
        index = 1
        good_stocks = []

        for stock in tqdm(stocks['TICKER'], desc=f'search relevant ticker by tech analise of data tickers where close '
                                                 f'price {self.min_buy} vs {self.max_buy}: '):
            if counter == 10:
                time.sleep(10)
                counter = 0
            try:
                df = investpy.get_stock_historical_data(
                    stock=stock, country=self.country, from_date=self.from_date, to_date=self.current_date)
                # stock='REZI', country=self.country, from_date=self.from_date, to_date=self.current_date)

                time.sleep(5)
                technical_indicators = investpy.technical.technical_indicators(
                    stock, self.country, 'stock', interval='daily')
                country = self.country
            except:
                continue
            tech_buy, tech_sell = self.get_tech_idicator_sell_buy(technical_indicators)

            time.sleep(2)
            moving_averages, moving_sma_buy, moving_sma_sell = self.get_sma_sell_buy(country, stock)
            moving_ema_buy, moving_ema_sell = self.get_ema_sell(moving_averages)

            if tech_buy < 9 or tech_sell > 2 or moving_sma_buy < 5 or moving_ema_buy < 5:
                continue
            ema_100, ema_20, sma_100, sma_20 = self.get_sma_ema_20_100(moving_averages)

            print(str(index) + ') ' + 'STOCK =', stock)
            print(f'Tech sell indicators: to buy = {tech_buy} of 12;  to sell = {tech_sell} of 12')
            print(f'SMA moving averages: to buy = {moving_sma_buy} of 6;  to sell = {moving_sma_sell} of 6')
            print(f'EMA moving averages: to buy = {moving_ema_buy} of 6;  to sell = {moving_ema_sell} of 6')
            print(f'SMA_20 = {sma_20} ; SMA_100 = {sma_100} ; EMA_20 = {ema_20} ; EMA_100 = {ema_100}')
            print(
                f"Prices Last Five days of  {stock} = {np.array(df['Close'][-5:][0])} ; {np.array(df['Close'][-5:][1])} ;"
                f" {np.array(df['Close'][-5:][2])} ; {np.array(df['Close'][-5:][3])} ; {np.array(df['Close'][-5:][4])}")

            # TODO доделать реализацию добавив сроки в формат данных и сохранить полученный результат
            # TODO сначало проверить текущие данные
            open_data = [float(np.array(df['Open'][-5:][4])), float(np.array(df['Open'][-5:][3])),
                         float(np.array(df['Open'][-5:][2])), float(np.array(df['Open'][-5:][1]))]
            data, meta_data = self.ts.get_intraday(symbol=stock, interval='1min', outputsize='full')
            data.index = pd.DatetimeIndex(data.index) + timedelta(hours=3, minutes=58)
            # print(df)

            high_data = []
            low_data = []

            for index, value in enumerate(open_data):
                high, low = self.get_stock_intraday(open=value, interval=1, index=index, data=data)
                high_data.append(high)
                low_data.append(low)
                # print(index)
                # print(value)
                # print(open_data[index])
                # print(stock)
                # print(high)
                # print(low)

            # print(high_data)
            # print(low_data)
            #
            # exit()

            pp_1, pp_2, pp_3, pp_4 = self.get_percentage_for_four_day_ago(df)

            print('Percentage +/- of ' + stock + ' =', pp_1,
                  ';', pp_2, ';', pp_3, ';', pp_4, )
            print()

            index += 1
            counter += 1
            good_stocks.append(stock)
            time.sleep(2)

            name_stock_exchange = self.get_name_stock_exchange(stock)

            data_ticker = data_ticker.append({
                'TICKER': stock,
                'Tech_buy': tech_buy,
                'Tech_sell': tech_sell,
                'SMA_buy': moving_sma_buy,
                'SMA_sell': moving_sma_sell,
                'SMA_20': sma_20,
                'SMA_100': sma_100,
                'EMA_buy': moving_ema_buy,
                'EMA_sell': moving_ema_sell,
                'EMA_20': ema_20,
                'EMA_100': ema_100,
                'CLOSE_prev': np.array(df['Close'][-5:][4]),
                'Percentage_1': pp_1,
                'p1_Op_0,5_up': high_data[3][0],
                'p1_0,5_1.0_up': high_data[3][1],
                'p1_1,0_1,5_up': high_data[3][2],
                'p1_1,5_2,0_up': high_data[3][3],
                'p1_2,0_over_up': high_data[3][4],
                'p1_Op_0,2_dwn': low_data[3][0],
                'p1_0,2_0,3_dwn': low_data[3][1],
                'p1_0,3_0,4_dwn': low_data[3][2],
                'p1_0,4_0,5_dwn': low_data[3][3],
                'p1_0,5_dwn,less': low_data[3][4],
                'Percentage_2': pp_2,
                'p2_Op_0,5_up': high_data[2][0],
                'p2_0,5_1.0_up': high_data[2][1],
                'p2_1,0_1,5_up': high_data[2][2],
                'p2_1,5_2,0_up': high_data[2][3],
                'p2_2,0_over_up': high_data[2][4],
                'p2_Op_0,2_dwn': low_data[2][0],
                'p2_0,2_0,3_dwn': low_data[2][1],
                'p2_0,3_0,4_dwn': low_data[2][2],
                'p2_0,4_0,5_dwn': low_data[2][3],
                'p2_0,5_dwn,less': low_data[2][4],
                'Percentage_3': pp_3,
                'p3_Op_0,5_up': high_data[1][0],
                'p3_0,5_1.0_up': high_data[1][1],
                'p3_1,0_1,5_up': high_data[1][2],
                'p3_1,5_2,0_up': high_data[1][3],
                'p3_2,0_over_up': high_data[1][4],
                'p3_Op_0,2_dwn': low_data[1][0],
                'p3_0,2_0,3_dwn': low_data[1][1],
                'p3_0,3_0,4_dwn': low_data[1][2],
                'p3_0,4_0,5_dwn': low_data[1][3],
                'p3_0,5_dwn,less': low_data[1][4],
                'Percentage_4': pp_4,
                'p4_Op_0,5_up': high_data[0][0],
                'p4_0,5_1.0_up': high_data[0][1],
                'p4_1,0_1,5_up': high_data[0][2],
                'p4_1,5_2,0_up': high_data[0][3],
                'p4_2,0_over_up': high_data[0][4],
                'p4_Op_0,2_dwn': low_data[0][0],
                'p4_0,2_0,3_dwn': low_data[0][1],
                'p4_0,3_0,4_dwn': low_data[0][2],
                'p4_0,4_0,5_dwn': low_data[0][3],
                'p4_0,5_dwn,less': low_data[0][4],
                'Exchange': name_stock_exchange
            }, ignore_index=True)

            # data_ticker.to_excel('data_ticker.xlsx', index=True, header=True)
            # exit()

        data_ticker.to_excel('data_ticker.xlsx', index=True, header=True)

    def get_stock_intraday(self, open, interval, index, data):
        high_data = []
        low_data = []
        is_date = True
        is_date_count = 0

        while is_date:
            last_current_date = (data.index[0] - timedelta(days=index)).date()
            # current_date = str((pd.Timestamp.now() - timedelta(days=1)).date())
            result_data = data.loc[str(last_current_date):str(last_current_date)]
            if len(result_data) == 0:
                # count += 1
                pass
            else:
                # print(result_data)
                # print(len(result_data))
                # print(result_data.index[0])
                # print(last_current_date)
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

                open_percent_0_5 = len(
                    result_data.where(
                        (result_data['2. high'] > open) & (result_data['2. high'] <= percent_0_5)).dropna())
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
                    result_data.where(
                        (result_data['3. low'] < open) & (result_data['3. low'] >= percent_m_0_2)).dropna())
                percent_m_0_2_percent_m_0_3 = len(
                    result_data.where(
                        (result_data['3. low'] < percent_m_0_2) & (result_data['3. low'] >= percent_m_0_3)).dropna())
                percent_m_0_3_percent_m_0_4 = len(
                    result_data.where(
                        (result_data['3. low'] < percent_m_0_3) & (result_data['3. low'] >= percent_m_0_4)).dropna())
                percent_m_0_4_percent_m_0_5 = len(
                    result_data.where(
                        (result_data['3. low'] < percent_m_0_4) & (result_data['3. low'] >= percent_m_0_5)).dropna())
                percent_m_0_5_less = len(result_data.where(result_data['3. low'] < percent_m_0_5).dropna())

                low_data = [open_percent_0_5, percent_0_5_percent_1, percent_1_percent_1_5, percent_1_5_percent_2,
                            percent_2_over]
                high_data = [open_percent_m_0_2, percent_m_0_2_percent_m_0_3, percent_m_0_3_percent_m_0_4,
                             percent_m_0_4_percent_m_0_5,
                             percent_m_0_5_less]
                # high_data.append(high)
                # low_data.append(low)

                # print('high')
                # print(open_percent_0_5, percent_0_5_percent_1, percent_1_percent_1_5, percent_1_5_percent_2,
                #       percent_2_over)
                # print('low')
                # print(open_percent_m_0_2, percent_m_0_2_percent_m_0_3, percent_m_0_3_percent_m_0_4,
                #       percent_m_0_4_percent_m_0_5,
                #       percent_m_0_5_less)

            if is_date_count == interval:
                is_date = False
        return high_data, low_data

    def addition_main_data_ticker(self):
        data = pd.read_excel('data_ticker.xlsx')
        for name in tqdm(data['TICKER']):
            time.sleep(3)
            df = investpy.get_stock_historical_data(
                stock=name, country=self.country, from_date=self.from_date, to_date=self.current_date)
            cr_m = df.index[-1:].tolist()[0].month
            cr_d = df.index[-1:].tolist()[0].day
            cr_y = df.index[-1:].tolist()[0].year
            current_d = str(cr_d) + '/' + str(cr_m) + '/' + str(cr_y)
            # TODO доделать реализацию добавив реализацию и сроки в формат данных и обновить данные
            # TODO сначало проверить текщие данные
            try:
                if self.current_date == current_d:
                    pass
                else:
                    data.loc[data.TICKER[data.TICKER == name].index.tolist()[0], 'Open_point'] = np.array(
                        df['Open'][-5:][4])
                    data.loc[data.TICKER[data.TICKER == name].index.tolist()[0], 'High_point'] = np.array(
                        df['High'][-5:][4])
            except:
                print()
                print(f'ticker: {name} not available data')
                continue

            # data.to_excel('data_ticker.xlsx', index=False, header=True)
            # exit()

        data.to_excel('data_ticker.xlsx', index=False, header=True)

    def get_percentage_for_four_day_ago(self, df):
        p_1 = abs(1 - df['Close'][-5:][1] / df['Close'][-5:][0])
        if df['Close'][-5:][1] >= df['Close'][-5:][0]:
            pp_1 = '+' + str(round(p_1 * 100, 2)) + '%'
        else:
            pp_1 = '-' + str(round(p_1 * 100, 2)) + '%'
        p_2 = abs(1 - df['Close'][-5:][2] / df['Close'][-5:][1])
        if df['Close'][-5:][2] >= df['Close'][-5:][1]:
            pp_2 = '+' + str(round(p_2 * 100, 2)) + '%'
        else:
            pp_2 = '-' + str(round(p_2 * 100, 2)) + '%'
        p_3 = abs(1 - df['Close'][-5:][3] / df['Close'][-5:][2])
        if df['Close'][-5:][3] >= df['Close'][-5:][2]:
            pp_3 = '+' + str(round(p_3 * 100, 2)) + '%'
        else:
            pp_3 = '-' + str(round(p_3 * 100, 2)) + '%'
        p_4 = abs(1 - df['Close'][-5:][4] / df['Close'][-5:][3])
        if df['Close'][-5:][4] >= df['Close'][-5:][3]:
            pp_4 = '+' + str(round(p_4 * 100, 2)) + '%'
        else:
            pp_4 = '-' + str(round(p_4 * 100, 2)) + '%'
        return pp_1, pp_2, pp_3, pp_4

    def get_name_stock_exchange(self, stock):
        ua = UserAgent()
        headers = {'User-Agent': str(ua.chrome)}
        url_ticker = investpy.get_stock_company_profile(stock, self.country)['url']
        time.sleep(3)
        r = requests.get(url_ticker, headers=headers)
        tree = html.fromstring(r.content)
        name_stock_exchange = tree.xpath('//*[@id="DropdownBtn"]/i/text()')[0]
        return name_stock_exchange

    def get_sma_ema_20_100(self, moving_averages):
        sma_20 = moving_averages['sma_signal'][2]
        sma_100 = moving_averages['sma_signal'][4]
        ema_20 = moving_averages['ema_signal'][2]
        ema_100 = moving_averages['ema_signal'][4]
        return ema_100, ema_20, sma_100, sma_20

    def get_ema_sell(self, moving_averages):
        moving_ema_sell = len(moving_averages[moving_averages['ema_signal'] == 'sell'])
        moving_ema_buy = len(moving_averages[moving_averages['ema_signal'] == 'buy'])
        return moving_ema_buy, moving_ema_sell

    def get_sma_sell_buy(self, country, stock):
        moving_averages = investpy.technical.moving_averages(stock, country, 'stock', interval='daily')
        moving_sma_sell = len(moving_averages[moving_averages['sma_signal'] == 'sell'])
        moving_sma_buy = len(moving_averages[moving_averages['sma_signal'] == 'buy'])
        return moving_averages, moving_sma_buy, moving_sma_sell

    def get_tech_idicator_sell_buy(self, technical_indicators):
        tech_sell = len(technical_indicators[technical_indicators['signal'] == 'sell'])
        tech_buy = len(technical_indicators[technical_indicators['signal'] == 'buy'])
        return tech_buy, tech_sell
