import investpy
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, date
import time
from alpha_vantage.timeseries import TimeSeries
import yfinance as yf
import traceback
from selenium import webdriver
import requests
from fake_useragent import UserAgent
from lxml import html
from tqdm import tqdm

import config
import logging

from logger_bot import TGBOT

logging.basicConfig(level=logging.ERROR)


class Parser(object):
    """
    provider ticker stocks exchange
    """

    def __init__(self, country, min_buy, max_buy, config_a_vil, file_name, bot):
        # self.data = data
        self.config_a_vil = config_a_vil
        self.max_buy = max_buy
        self.min_buy = min_buy
        self.country = country
        self.bot = bot

        # print(self.bot)

        # self.bot.wl('asdasdas')

        self.file_name = file_name
        # op = webdriver.ChromeOptions()
        # op.add_argument('headless')
        # self.driver = webdriver.Chrome(options=op)

        self.good_stocks = []

        self.current_date = str(date.today().day) + '/' + str(date.today().month) + '/' + str(date.today().year)
        self.current_date_y = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day)

        a = date.today().month

        if a == 1:
            self.from_date = str(date.today().day) + '/' + str(12) + '/' + str(date.today().year - 1)
            self.from_date_y = str(date.today().year - 1) + '-' + str(12) + '-' + str(date.today().day)
        else:
            # TODO change  str(date.today().month - 2 to str(date.today().month - 1 or add check febr
            self.from_date = str(date.today().day) + '/' + str(date.today().month - 1) + '/' + str(date.today().year)
            self.from_date_y = str(date.today().year) + '-' + str(date.today().month - 1) + '-' + str(date.today().day)

        self.ts = TimeSeries(key=self.config_a_vil, output_format='pandas')

    def create_data_ticker_min_max_by_close(self):
        data = pd.DataFrame(columns=['TICKER', 'CLOSE'])
        stocks = investpy.stocks.get_stocks(country=self.country)['symbol']

        for stock in tqdm(stocks, desc=f'create data tickers for all data {self.country} stocks exchange: '):
            try:
                # df = investpy.get_stock_historical_data(
                #     stock=stock, country=self.country, from_date=self.from_date, to_date=self.current_date)
                df = yf.download(tickers=stock, start=self.from_date_y, end=self.current_date_y)
                data = data.append({
                    'TICKER': stock,
                    'CLOSE': df['Close'][-1]
                }, ignore_index=True)
            except:
                print()
                print(f' {stock}, information unavailable or not found.')
                continue
            # time.sleep(2)
        data.to_excel(self.file_name, index=True, header=True)

    def search_relevant_ticker(self):
        data_stocks = pd.read_excel(self.file_name, index_col=False)[['TICKER', 'CLOSE']]
        stocks = data_stocks.where(
            (data_stocks['CLOSE'] >= self.min_buy) & (data_stocks['CLOSE'] <= self.max_buy)).dropna()

        data_ticker = pd.DataFrame(columns=[
            'TICKER', 'Tech_buy', 'Tech_sell', 'SMA_buy', 'SMA_sell', 'SMA_20', 'SMA_100', 'EMA_buy', 'EMA_sell',
            'EMA_20', 'EMA_100',
            'p1_Op_0,5_up', 'p1_0,5_1.0_up', 'p1_1,0_1,5_up', 'p1_1,5_2,0_up', 'p1_2,0_over_up',
            'p1_c_h_l_o_1', 'p1_c_mt_h_l_o_1', 'p1_c_h_l_o_2', 'p1_c_mt_h_l_o_2',
            'p1_Op_0,2_dwn', 'p1_0,2_0,3_dwn', 'p1_0,3_0,4_dwn', 'p1_0,4_0,5_dwn', 'p1_0,5_less_dwn', 'p1_c_l_h_o_1',
            'p1_c_mt_l_h_o_1', 'p1_c_l_h_o_2', 'p1_c_mt_l_h_o_2',
            'p1_c_mt_h_l_m_05___1', 'p1_c_mt_h_l_m_05___1_5',
            'p1_c_mt_l_h_m_05___1', 'p1_c_mt_l_h_m_05___1_5',
            'p1_c_h_l_m_05___1', 'p1_c_h_l_m_05___1_5',
            'p1_c_l_h_m_05___1', 'p1_c_l_h_m_05___1_5',
            'p1_c_mt_h_l_m_1___1', 'p1_c_mt_h_l_m_1___1_5',
            'p1_c_mt_l_h_m_1___1', 'p1_c_mt_l_h_m_1___1_5',
            'p1_c_h_l_m_1___1', 'p1_c_h_l_m_1___1_5',
            'p1_c_l_h_m_1___1', 'p1_c_l_h_m_1___1_5',
            'Percentage_1',
            '1_CLOSE_prev',
            '1_Open_point',
            '1_High_point',
            '1_Low_point',
            '1_Close_point',
            '1_C-O',
            '1_O-H',
            '1_O-L',
            '1_L-C',

            'p2_Op_0,5_up', 'p2_0,5_1.0_up', 'p2_1,0_1,5_up', 'p2_1,5_2,0_up', 'p2_2,0_over_up',
            'p2_c_h_l_o_1', 'p2_c_mt_h_l_o_1', 'p2_c_h_l_o_2', 'p2_c_mt_h_l_o_2',
            'p2_Op_0,2_dwn', 'p2_0,2_0,3_dwn', 'p2_0,3_0,4_dwn', 'p2_0,4_0,5_dwn', 'p2_0,5_less_dwn', 'p2_c_l_h_o_1',
            'p2_c_mt_l_h_o_1', 'p2_c_l_h_o_2', 'p2_c_mt_l_h_o_2',
            'p2_c_mt_h_l_m_05___1', 'p2_c_mt_h_l_m_05___1_5',
            'p2_c_mt_l_h_m_05___1', 'p2_c_mt_l_h_m_05___1_5',
            'p2_c_h_l_m_05___1', 'p2_c_h_l_m_05___1_5',
            'p2_c_l_h_m_05___1', 'p2_c_l_h_m_05___1_5',
            'p2_c_mt_h_l_m_1___1', 'p2_c_mt_h_l_m_1___1_5',
            'p2_c_mt_l_h_m_1___1', 'p2_c_mt_l_h_m_1___1_5',
            'p2_c_h_l_m_1___1', 'p2_c_h_l_m_1___1_5',
            'p2_c_l_h_m_1___1', 'p2_c_l_h_m_1___1_5',

            'Percentage_2',
            '2_CLOSE_prev',
            '2_Open_point',
            '2_High_point',
            '2_Low_point',
            '2_Close_point',
            '2_C-O',
            '2_O-H',
            '2_O-L',
            '2_L-C',

            'p3_Op_0,5_up', 'p3_0,5_1.0_up', 'p3_1,0_1,5_up', 'p3_1,5_2,0_up', 'p3_2,0_over_up',
            'p3_c_h_l_o_1', 'p3_c_mt_h_l_o_1', 'p3_c_h_l_o_2', 'p3_c_mt_h_l_o_2',
            'p3_Op_0,2_dwn', 'p3_0,2_0,3_dwn', 'p3_0,3_0,4_dwn', 'p3_0,4_0,5_dwn', 'p3_0,5_less_dwn', 'p3_c_l_h_o_1',
            'p3_c_mt_l_h_o_1', 'p3_c_l_h_o_2', 'p3_c_mt_l_h_o_2',
            'p3_c_mt_h_l_m_05___1', 'p3_c_mt_h_l_m_05___1_5',
            'p3_c_mt_l_h_m_05___1', 'p3_c_mt_l_h_m_05___1_5',
            'p3_c_h_l_m_05___1', 'p3_c_h_l_m_05___1_5',
            'p3_c_l_h_m_05___1', 'p3_c_l_h_m_05___1_5',
            'p3_c_mt_h_l_m_1___1', 'p3_c_mt_h_l_m_1___1_5',
            'p3_c_mt_l_h_m_1___1', 'p3_c_mt_l_h_m_1___1_5',
            'p3_c_h_l_m_1___1', 'p3_c_h_l_m_1___1_5',
            'p3_c_l_h_m_1___1', 'p3_c_l_h_m_1___1_5',
            'Percentage_3',
            '3_CLOSE_prev',
            '3_Open_point',
            '3_High_point',
            '3_Low_point',
            '3_Close_point',
            '3_C-O',
            '3_O-H',
            '3_O-L',
            '3_L-C',

            'p4_Op_0,5_up', 'p4_0,5_1.0_up', 'p4_1,0_1,5_up', 'p4_1,5_2,0_up', 'p4_2,0_over_up',
            'p4_c_h_l_o_1', 'p4_c_mt_h_l_o_1', 'p4_c_h_l_o_2', 'p4_c_mt_h_l_o_2',
            'p4_Op_0,2_dwn', 'p4_0,2_0,3_dwn', 'p4_0,3_0,4_dwn', 'p4_0,4_0,5_dwn', 'p4_0,5_less_dwn', 'p4_c_l_h_o_1',
            'p4_c_mt_l_h_o_1', 'p4_c_l_h_o_2', 'p4_c_mt_l_h_o_2',
            'p4_c_mt_h_l_m_05___1', 'p4_c_mt_h_l_m_05___1_5',
            'p4_c_mt_l_h_m_05___1', 'p4_c_mt_l_h_m_05___1_5',
            'p4_c_h_l_m_05___1', 'p4_c_h_l_m_05___1_5',
            'p4_c_l_h_m_05___1', 'p4_c_l_h_m_05___1_5',
            'p4_c_mt_h_l_m_1___1', 'p4_c_mt_h_l_m_1___1_5',
            'p4_c_mt_l_h_m_1___1', 'p4_c_mt_l_h_m_1___1_5',
            'p4_c_h_l_m_1___1', 'p4_c_h_l_m_1___1_5',
            'p4_c_l_h_m_1___1', 'p4_c_l_h_m_1___1_5',
            'Percentage_4',
            '4_CLOSE_prev',
            '4_Open_point',
            '4_High_point',
            '4_Low_point',
            '4_Close_point',

            'Count_H_4', 'Count_L_4',
            'Count_H_2', 'Count_L_2',
            'res_mt_h_l_o_2_4', 'res_1_5_o_up_4', 'res_mt_h_l_o_2_2', 'res_1_5_o_up_2',
            'res_mt_l_h_o_2_4', 'res_0_5_less_4', 'res_mt_l_h_o_2_2', 'res_0_5_less_2',
            # 'Exchange',
            'm_data_count_l_h_0_5_1_4',
            'm_data_count_l_h_0_5_1_2',
            'm_data_count_l_h_0_5_1_5_4',
            'm_data_count_l_h_0_5_1_5_2',

            'm_data_count_l_h_1_1_4',
            'm_data_count_l_h_1_1_2',
            'm_data_count_l_h_1_1_5_4',
            'm_data_count_l_h_1_1_5_2',

            'Yahoo_Rating', 'Yahoo_Rating_Key', 'regVolume', 'avgVolume',
            'quickRatio', 'currentRatio', 'pegRatio', 'shortRatio', 'payoutRatio',
            '4_C-O', '4_O-H', '4_O-L', '4_L-C'
        ])
        counter = 0
        # index = 1
        # good_stocks = []
        inxd = 0

        for stock in tqdm(stocks['TICKER'], desc=f'search relevant ticker by tech analise of data tickers where close '
                                                 f'price {self.min_buy} vs {self.max_buy}: '):
            inxd += 1
            if counter == 10:
                time.sleep(10)
                counter = 0
            try:
                # df = investpy.get_stock_historical_data(
                #     stock=stock, country=self.country, from_date=self.from_date, to_date=self.current_date)
                # #stock='REZI', country=self.country, from_date=self.from_date, to_date=self.current_date)
                # time.sleep(5)
                time.sleep(2)
                technical_indicators = investpy.technical.technical_indicators(
                    # technical_indicators = investpy.technical_indicators(
                    # stock, self.country, 'stock', interval='daily')
                    stock, self.country, 'stock', interval='5hours')
                country = self.country
                time.sleep(1)
                # print(technical_indicators)
                # investpy.technical_indicators()
            except Exception:
                print()
                print(f"ERROR load data {stock} of get investpy.technical.technical_indicators ")
                traceback.print_exc()
                continue

            # print(f'\ncurrent stock - {stock}')

            try:
                tech_buy, tech_sell = self.get_tech_idicator_sell_buy(technical_indicators)
            except Exception:
                print()
                print(f"ERROR load data {stock} of get tech idicator sell buy ")
                traceback.print_exc()
                continue

            time.sleep(2)

            try:
                moving_averages, moving_sma_buy, moving_sma_sell = self.get_sma_sell_buy(country, stock)
                moving_ema_buy, moving_ema_sell = self.get_ema_sell(moving_averages)
            except:
                print()
                print(f"ERROR load data {stock} of get tech idicator SMA EMA ")
                continue

            if tech_buy < 9 or tech_sell > 2 or moving_sma_buy < 5 or moving_ema_buy < 5:
                continue
            # TODO место сбора детальных данных

            try:
                ema_100, ema_20, sma_100, sma_20 = self.get_sma_ema_20_100(moving_averages)
            except:
                print()
                print(f"ERROR load data {stock} of get tech idicator SMA EMA 100/20 ")
                continue

            try:
                print()
                df = yf.download(tickers=stock, start=self.from_date_y, end=self.current_date_y)
            except:
                print(f"ERROR load data {stock} of get yfinance")
                continue

            try:
                # print()
                print(str(len(self.good_stocks) + 1) + ') ' + 'STOCK =', stock)
                print(f'Tech sell indicators: to buy = {tech_buy} of 12;  to sell = {tech_sell} of 12')
                print(f'SMA moving averages: to buy = {moving_sma_buy} of 6;  to sell = {moving_sma_sell} of 6')
                print(f'EMA moving averages: to buy = {moving_ema_buy} of 6;  to sell = {moving_ema_sell} of 6')
                print(f'SMA_20 = {sma_20} ; SMA_100 = {sma_100} ; EMA_20 = {ema_20} ; EMA_100 = {ema_100}')
                print(
                    f"Prices Last Five days of  {stock} = {np.array(df['Close'][-5:][0])} ; {np.array(df['Close'][-5:][1])} ;"
                    f" {np.array(df['Close'][-5:][2])} ; {np.array(df['Close'][-5:][3])} ; {np.array(df['Close'][-5:][4])}")

                open_data = [float(np.array(df['Open'][-5:][4])), float(np.array(df['Open'][-5:][3])),
                             float(np.array(df['Open'][-5:][2])), float(np.array(df['Open'][-5:][1]))]
                time.sleep(1)
            except:
                print()
                print(f"ERROR print data {stock} of IndexError: index 4 is out of bounds for axis 0 with size 4 ")
                continue

            try:
                # data, meta_data = self.ts.get_intraday(symbol=stock, interval='5min', outputsize='full')

                data_y = yf.download(stock, self.from_date_y, self.current_date_y, interval='2m')

                # print(data)
                # print(data_y)
                # exit()

                # data.index = pd.DatetimeIndex(data.index) + timedelta(hours=3, minutes=58)
                # print(data.index)
                high_data = []
                low_data = []
                m_data_many_tick = []
                m_data_tick = []

                # print(open_data)

                over_count = 0
                for index, value in enumerate(open_data):
                    # print(value)
                    # print(index)
                    if index == 0:
                        high, low, ind, data_many, data_tick = self.get_stock_intraday(open=value, interval=1,
                                                                                       index=index + over_count,
                                                                                       data=data_y)
                        high_data.append(high)
                        low_data.append(low)
                        m_data_many_tick.append(data_many)
                        m_data_tick.append(data_tick)
                        over_count = ind
                    else:
                        index = over_count
                        # print(index)
                        high, low, ind, data_many, data_tick = self.get_stock_intraday(open=value, interval=1,
                                                                                       index=index, data=data_y)

                        high_data.append(high)
                        low_data.append(low)
                        m_data_many_tick.append(data_many)
                        m_data_tick.append(data_tick)
                        over_count = ind
                        # print(ind)

                    # if ind == 3:
                    #     over_count = ind

                # print(high_data)
                # print(low_data)
                # exit()

            except Exception:
                print()
                print(f"ERROR load data {stock} of alpha_vantage.timeseries ")
                traceback.print_exc()
                continue

            pp_1, pp_2, pp_3, pp_4 = self.get_percentage_for_four_day_ago(df)

            print('Percentage +/- of ' + stock + ' =', pp_1,
                  ';', pp_2, ';', pp_3, ';', pp_4, )

            # try:
            #     name_stock_exchange = self.get_name_stock_exchange(stock)
            #
            # except Exception:
            #     print()
            #     print(f"ERROR load name {stock} exchange of investpy ")
            #     traceback.print_exc()
            #     continue

            try:
                regularMarketVolume, averageVolume10days, recommendationMean, recommendationKey, quickRatio, currentRatio, pegRatio, shortRatio, payoutRatio = self.get_info_yh(
                    stock)



            except Exception:
                print()
                print(f"ERROR load name {stock} yahoo_rating")
                traceback.print_exc()
                continue
            # print(high_data)
            # print(low_data)
            res_h_4 = sum(high_data[3][:5]) + sum(high_data[2][:5]) + sum(high_data[1][:5]) + sum(high_data[0][:5])
            # print(high_data[3][:4])
            res_l_4 = sum(low_data[3][:5]) + sum(low_data[2][:5]) + sum(low_data[1][:5]) + sum(low_data[0][:5])

            res_h_2 = sum(high_data[1][:5]) + sum(high_data[0][:5])
            res_l_2 = sum(low_data[1][:5]) + sum(low_data[0][:5])

            res_mt_h_l_o_2_4 = high_data[0][8] + high_data[1][8] + high_data[2][8] + high_data[3][8]
            res_1_5_o_up_4 = high_data[0][3] + high_data[1][3] + high_data[2][3] + high_data[3][3] + high_data[0][4] + \
                             high_data[1][4] + high_data[2][4] + high_data[3][4]

            res_mt_h_l_o_2_2 = high_data[0][8] + high_data[1][8]
            res_1_5_o_up_2 = high_data[0][3] + high_data[1][3] + high_data[0][4] + high_data[1][4]

            res_mt_l_h_o_2_4 = low_data[0][8] + low_data[1][8] + low_data[2][8] + low_data[3][8]
            res_0_5_less_4 = low_data[0][4] + low_data[1][4] + low_data[2][4] + low_data[3][4]

            res_mt_l_h_o_2_2 = low_data[0][8] + low_data[1][8]
            res_0_5_less_2 = low_data[0][4] + low_data[1][4]

            m_data_count_l_h_0_5_1_4 = m_data_tick[0][2] + m_data_tick[1][2] + m_data_tick[2][2] + m_data_tick[3][2]
            m_data_count_l_h_0_5_1_2 = m_data_tick[0][2] + m_data_tick[1][2]

            m_data_count_l_h_0_5_1_5_4 = m_data_tick[0][3] + m_data_tick[1][3] + m_data_tick[2][3] + m_data_tick[3][3]
            m_data_count_l_h_0_5_1_5_2 = m_data_tick[0][3] + m_data_tick[1][3]

            m_data_count_l_h_1_1_4 = m_data_tick[0][6] + m_data_tick[1][6] + m_data_tick[2][6] + m_data_tick[3][6]
            m_data_count_l_h_1_1_2 = m_data_tick[0][6] + m_data_tick[1][6]

            m_data_count_l_h_1_1_5_4 = m_data_tick[0][7] + m_data_tick[1][7] + m_data_tick[2][7] + m_data_tick[3][7]
            m_data_count_l_h_1_1_5_2 = m_data_tick[0][7] + m_data_tick[1][7]

            # m_data_many_l_h_4_1 = m_data_many_tick[0][]
            # m_data_many_l_h_2_1 = sum(m_data_many_tick[0][:2]) + sum(m_data_many_tick[1][:2])
            #
            # m_data_tick_l_h_4_1 = sum(m_data_tick[0][:2]) + sum(m_data_tick[1][:2]) + sum(m_data_tick[2][:2]) + sum(
            #     m_data_tick[3][:2])
            # m_data_tick_l_h_2_1 = sum(m_data_tick[0][:2]) + sum(m_data_tick[1][:2])

            # res_l = sum(low_data[3][0]) + sum(low_data[3][1]) + sum(low_data[3][2]) + sum(low_data[3][3]) + sum(low_data[3][4])
            # print(res_h)
            # print(res_l)
            # exit()

            # print(df)
            # print(np.array(df['Close'][-5:][4]))
            # print(np.array(df['Close'][-5:][3]))
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

                'p1_Op_0,5_up': high_data[3][0],
                'p1_0,5_1.0_up': high_data[3][1],
                'p1_1,0_1,5_up': high_data[3][2],
                'p1_1,5_2,0_up': high_data[3][3],
                'p1_2,0_over_up': high_data[3][4],
                'p1_c_h_l_o_1': high_data[3][5],
                'p1_c_mt_h_l_o_1': high_data[3][6],
                'p1_c_h_l_o_2': high_data[3][7],
                'p1_c_mt_h_l_o_2': high_data[3][8],
                'p1_Op_0,2_dwn': low_data[3][0],
                'p1_0,2_0,3_dwn': low_data[3][1],
                'p1_0,3_0,4_dwn': low_data[3][2],
                'p1_0,4_0,5_dwn': low_data[3][3],
                'p1_0,5_less_dwn': low_data[3][4],
                'p1_c_l_h_o_1': low_data[3][5],
                'p1_c_mt_l_h_o_1': low_data[3][6],
                'p1_c_l_h_o_2': low_data[3][7],
                'p1_c_mt_l_h_o_2': low_data[3][8],
                'p1_c_mt_h_l_m_05___1': m_data_many_tick[3][0],
                'p1_c_mt_h_l_m_05___1_5': m_data_many_tick[3][1],
                'p1_c_mt_l_h_m_05___1': m_data_many_tick[3][2],
                'p1_c_mt_l_h_m_05___1_5': m_data_many_tick[3][3],
                'p1_c_h_l_m_05___1': m_data_tick[3][0],
                'p1_c_h_l_m_05___1_5': m_data_tick[3][1],
                'p1_c_l_h_m_05___1': m_data_tick[3][2],
                'p1_c_l_h_m_05___1_5': m_data_tick[3][3],

                'p1_c_mt_h_l_m_1___1': m_data_many_tick[3][4],
                'p1_c_mt_h_l_m_1___1_5': m_data_many_tick[3][5],
                'p1_c_mt_l_h_m_1___1': m_data_many_tick[3][6],
                'p1_c_mt_l_h_m_1___1_5': m_data_many_tick[3][7],
                'p1_c_h_l_m_1___1': m_data_tick[3][4],
                'p1_c_h_l_m_1___1_5': m_data_tick[3][5],
                'p1_c_l_h_m_1___1': m_data_tick[3][6],
                'p1_c_l_h_m_1___1_5': m_data_tick[3][7],

                'Percentage_1': pp_1,
                '1_CLOSE_prev': np.array(df['Close'][-5:][1]),
                '1_Open_point': np.array(df['Open'][-5:][2]),
                '1_High_point': np.array(df['High'][-5:][2]),
                '1_Low_point': np.array(df['Low'][-5:][2]),
                '1_Close_point': np.array(df['Close'][-5:][2]),

                'p2_Op_0,5_up': high_data[2][0],
                'p2_0,5_1.0_up': high_data[2][1],
                'p2_1,0_1,5_up': high_data[2][2],
                'p2_1,5_2,0_up': high_data[2][3],
                'p2_2,0_over_up': high_data[2][4],
                'p2_c_h_l_o_1': high_data[2][5],
                'p2_c_mt_h_l_o_1': high_data[2][6],
                'p2_c_h_l_o_2': high_data[2][7],
                'p2_c_mt_h_l_o_2': high_data[2][8],
                'p2_Op_0,2_dwn': low_data[2][0],
                'p2_0,2_0,3_dwn': low_data[2][1],
                'p2_0,3_0,4_dwn': low_data[2][2],
                'p2_0,4_0,5_dwn': low_data[2][3],
                'p2_0,5_less_dwn': low_data[2][4],
                'p2_c_l_h_o_1': low_data[2][5],
                'p2_c_mt_l_h_o_1': low_data[2][6],
                'p2_c_l_h_o_2': low_data[2][7],
                'p2_c_mt_l_h_o_2': low_data[2][8],
                'p2_c_mt_h_l_m_05___1': m_data_many_tick[2][0],
                'p2_c_mt_h_l_m_05___1_5': m_data_many_tick[2][1],
                'p2_c_mt_l_h_m_05___1': m_data_many_tick[2][2],
                'p2_c_mt_l_h_m_05___1_5': m_data_many_tick[2][3],
                'p2_c_h_l_m_05___1': m_data_tick[2][0],
                'p2_c_h_l_m_05___1_5': m_data_tick[2][1],
                'p2_c_l_h_m_05___1': m_data_tick[2][2],
                'p2_c_l_h_m_05___1_5': m_data_tick[2][3],

                'p2_c_mt_h_l_m_1___1': m_data_many_tick[2][4],
                'p2_c_mt_h_l_m_1___1_5': m_data_many_tick[2][5],
                'p2_c_mt_l_h_m_1___1': m_data_many_tick[2][6],
                'p2_c_mt_l_h_m_1___1_5': m_data_many_tick[2][7],
                'p2_c_h_l_m_1___1': m_data_tick[2][4],
                'p2_c_h_l_m_1___1_5': m_data_tick[2][5],
                'p2_c_l_h_m_1___1': m_data_tick[2][6],
                'p2_c_l_h_m_1___1_5': m_data_tick[2][7],

                'Percentage_2': pp_2,
                '2_CLOSE_prev': np.array(df['Close'][-5:][2]),
                '2_Open_point': np.array(df['Open'][-5:][3]),
                '2_High_point': np.array(df['High'][-5:][3]),
                '2_Low_point': np.array(df['Low'][-5:][3]),
                '2_Close_point': np.array(df['Close'][-5:][3]),

                'p3_Op_0,5_up': high_data[1][0],
                'p3_0,5_1.0_up': high_data[1][1],
                'p3_1,0_1,5_up': high_data[1][2],
                'p3_1,5_2,0_up': high_data[1][3],
                'p3_2,0_over_up': high_data[1][4],
                'p3_c_h_l_o_1': high_data[1][5],
                'p3_c_mt_h_l_o_1': high_data[1][6],
                'p3_c_h_l_o_2': high_data[1][7],
                'p3_c_mt_h_l_o_2': high_data[1][8],
                'p3_Op_0,2_dwn': low_data[1][0],
                'p3_0,2_0,3_dwn': low_data[1][1],
                'p3_0,3_0,4_dwn': low_data[1][2],
                'p3_0,4_0,5_dwn': low_data[1][3],
                'p3_0,5_less_dwn': low_data[1][4],
                'p3_c_l_h_o_1': low_data[1][5],
                'p3_c_mt_l_h_o_1': low_data[1][6],
                'p3_c_l_h_o_2': low_data[1][7],
                'p3_c_mt_l_h_o_2': low_data[1][8],
                'p3_c_mt_h_l_m_05___1': m_data_many_tick[1][0],
                'p3_c_mt_h_l_m_05___1_5': m_data_many_tick[1][1],
                'p3_c_mt_l_h_m_05___1': m_data_many_tick[1][2],
                'p3_c_mt_l_h_m_05___1_5': m_data_many_tick[1][3],
                'p3_c_h_l_m_05___1': m_data_tick[1][0],
                'p3_c_h_l_m_05___1_5': m_data_tick[1][1],
                'p3_c_l_h_m_05___1': m_data_tick[1][2],
                'p3_c_l_h_m_05___1_5': m_data_tick[1][3],

                'p3_c_mt_h_l_m_1___1': m_data_many_tick[1][4],
                'p3_c_mt_h_l_m_1___1_5': m_data_many_tick[1][5],
                'p3_c_mt_l_h_m_1___1': m_data_many_tick[1][6],
                'p3_c_mt_l_h_m_1___1_5': m_data_many_tick[1][7],
                'p3_c_h_l_m_1___1': m_data_tick[1][4],
                'p3_c_h_l_m_1___1_5': m_data_tick[1][5],
                'p3_c_l_h_m_1___1': m_data_tick[1][6],
                'p3_c_l_h_m_1___1_5': m_data_tick[1][7],

                'Percentage_3': pp_3,
                '3_CLOSE_prev': np.array(df['Close'][-5:][3]),
                '3_Open_point': np.array(df['Open'][-5:][4]),
                '3_High_point': np.array(df['High'][-5:][4]),
                '3_Low_point': np.array(df['Low'][-5:][4]),
                '3_Close_point': np.array(df['Close'][-5:][4]),

                'p4_Op_0,5_up': high_data[0][0],
                'p4_0,5_1.0_up': high_data[0][1],
                'p4_1,0_1,5_up': high_data[0][2],
                'p4_1,5_2,0_up': high_data[0][3],
                'p4_2,0_over_up': high_data[0][4],
                'p4_c_h_l_o_1': high_data[0][5],
                'p4_c_mt_h_l_o_1': high_data[0][6],
                'p4_c_h_l_o_2': high_data[0][7],
                'p4_c_mt_h_l_o_2': high_data[0][8],
                'p4_Op_0,2_dwn': low_data[0][0],
                'p4_0,2_0,3_dwn': low_data[0][1],
                'p4_0,3_0,4_dwn': low_data[0][2],
                'p4_0,4_0,5_dwn': low_data[0][3],
                'p4_0,5_less_dwn': low_data[0][4],
                'p4_c_l_h_o_1': low_data[0][5],
                'p4_c_mt_l_h_o_1': low_data[0][6],
                'p4_c_l_h_o_2': low_data[0][7],
                'p4_c_mt_l_h_o_2': low_data[0][8],
                'p4_c_mt_h_l_m_05___1': m_data_many_tick[0][0],
                'p4_c_mt_h_l_m_05___1_5': m_data_many_tick[0][1],
                'p4_c_mt_l_h_m_05___1': m_data_many_tick[0][2],
                'p4_c_mt_l_h_m_05___1_5': m_data_many_tick[0][3],
                'p4_c_h_l_m_05___1': m_data_tick[0][0],
                'p4_c_h_l_m_05___1_5': m_data_tick[0][1],
                'p4_c_l_h_m_05___1': m_data_tick[0][2],
                'p4_c_l_h_m_05___1_5': m_data_tick[0][3],

                'p4_c_mt_h_l_m_1___1': m_data_many_tick[0][4],
                'p4_c_mt_h_l_m_1___1_5': m_data_many_tick[0][5],
                'p4_c_mt_l_h_m_1___1': m_data_many_tick[0][6],
                'p4_c_mt_l_h_m_1___1_5': m_data_many_tick[0][7],
                'p4_c_h_l_m_1___1': m_data_tick[0][4],
                'p4_c_h_l_m_1___1_5': m_data_tick[0][5],
                'p4_c_l_h_m_1___1': m_data_tick[0][6],
                'p4_c_l_h_m_1___1_5': m_data_tick[0][7],

                'Percentage_4': pp_4,
                '4_CLOSE_prev': np.array(df['Close'][-5:][4]),

                'Count_H_4': res_h_4,
                'Count_L_4': res_l_4,

                'Count_H_2': res_h_2,
                'Count_L_2': res_l_2,

                'res_mt_h_l_o_2_4': res_mt_h_l_o_2_4,
                'res_1_5_o_up_4': res_1_5_o_up_4,
                'res_mt_h_l_o_2_2': res_mt_h_l_o_2_2,
                'res_1_5_o_up_2': res_1_5_o_up_2,

                'res_mt_l_h_o_2_4': res_mt_l_h_o_2_4,
                'res_0_5_less_4': res_0_5_less_4,
                'res_mt_l_h_o_2_2': res_mt_l_h_o_2_2,
                'res_0_5_less_2': res_0_5_less_2,

                'm_data_count_l_h_0_5_1_4': m_data_count_l_h_0_5_1_4,
                'm_data_count_l_h_0_5_1_2': m_data_count_l_h_0_5_1_2,
                'm_data_count_l_h_0_5_1_5_4': m_data_count_l_h_0_5_1_5_4,
                'm_data_count_l_h_0_5_1_5_2': m_data_count_l_h_0_5_1_5_2,

                'm_data_count_l_h_1_1_4': m_data_count_l_h_1_1_4,
                'm_data_count_l_h_1_1_2': m_data_count_l_h_1_1_2,
                'm_data_count_l_h_1_1_5_4': m_data_count_l_h_1_1_5_4,
                'm_data_count_l_h_1_1_5_2': m_data_count_l_h_1_1_5_2,

                # 'Exchange': name_stock_exchange,
                # 'Yahoo_Rating': yahoo_rating

                'Yahoo_Rating': recommendationMean,
                'Yahoo_Rating_Key': recommendationKey,
                'regVolume': regularMarketVolume,
                'avgVolume': averageVolume10days,

                'quickRatio': quickRatio,
                'currentRatio': currentRatio,
                'pegRatio': pegRatio,
                'shortRatio': shortRatio,
                'payoutRatio': payoutRatio

            }, ignore_index=True)
            # exit()

            print(f'{stock} add to data...')
            # index += 1
            counter += 1
            self.good_stocks.append(stock)
            # self.bot.send( f'{len(good_stocks)}) {stock} add to data...')
            time.sleep(1)
            # print(f'down {self.data}')
            # self.data.set_item_to_data(stock)

            temp_str = f'{inxd} of {len(stocks["TICKER"])}'
            # print(temp_str)
            data_to_bot = [self.good_stocks, [temp_str]]
            # print(data_to_bot)
            self.bot.add_item_to_data(data_to_bot)

            # self.bot.add_item_to_data(stock)
            # self.bot.add_count_of_parse(temp_str)
            #
            # data_ticker.to_excel(f'{self.min_buy}_{self.max_buy}_data_ticker.xlsx', index=True, header=True)
            #
            # self.bot.send(f'parse with param : {self.min_buy} vs {self.max_buy} is DONE!! Size of good_stocks after analize = {len(self.good_stocks)}')
            # exit()

            yield stock
        data_ticker.to_excel(f'{self.min_buy}_{self.max_buy}_data_ticker.xlsx', index=True, header=True)
        self.bot.send(
            f'parse with param : {self.min_buy} vs {self.max_buy} is DONE!! Size of good_stocks after analize = {len(self.good_stocks)}')
        # self.driver.close()

    def get_good_stocks(self):
        return self.good_stocks

    def get_stock_intraday(self, open, interval, index, data):
        # print('intro')
        high_data = []
        low_data = []
        m_data_many_tick = []
        m_data_tick = []

        is_date = True
        is_date_count = 0

        # print(data)

        while is_date:
            # print('while')
            # last_current_date = (data.index[0] - timedelta(days=index)).date()
            last_current_date = (data.index[-1] - timedelta(days=index)).date()
            # current_date = str((pd.Timestamp.now() - timedelta(days=1)).date())
            result_data = data.loc[str(last_current_date):str(last_current_date)]
            if len(result_data) == 0:
                index += 1
                # print(index)
                # is_date_count += 1
                pass
            else:
                # print(index)
                # print(result_data)
                # # print(len(result_data))
                # print(result_data.index[0])
                # print(last_current_date)

                is_date_count += 1
                # count += 1
                percent_0_5, percent_1, percent_1_5, percent_2, percent_m_0_2, percent_m_0_3, percent_m_0_4, percent_m_0_5 = self.create_percent_group_of_open(
                    open)

                # print(result_data)
                # exit()

                # array_h = np.array(result_data['2. high'])[::-1]
                array_h = np.array(result_data['High'])
                # array_h = np.array(result_data['High'][:len(result_data['High'])//3])
                # array_h = np.array(result_data['4. close'])[::-1]
                # array_l = np.array(result_data['3. low'])[::-1]
                array_l = np.array(result_data['Low'])
                # array_l = np.array(result_data['Low'][:len(result_data['Low'])//3])

                # print(len(array_h))
                # print(len(array_l))
                # # print(len(array_h[:len(array_h)//3]))
                # # print(len(array_l[:len(array_l)//3]))
                #
                # exit()

                count_many_tick_h_l_over_2, count_many_tick_l_h_over_2 = self.get_many_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_2,
                    open)
                # percent_m_0_5)
                # percent_m_0_2)

                count_h_l_over_2, count_l_h_over_2 = self.get_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_2,
                    open)
                # percent_m_0_5)
                # percent_m_0_2)

                count_many_tick_h_l_over_1, count_many_tick_l_h_over_1 = self.get_many_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_1,
                    open)
                # percent_m_0_5)
                # percent_m_0_2)

                count_h_l_over_1, count_l_h_over_1 = self.get_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_1,
                    open)
                # percent_m_0_5)
                # percent_m_0_2)

                count_many_tick_h_l_m_05___1, count_many_tick_l_h_m_05___1 = self.get_many_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_0_5 + (percent_m_0_5 * .01),
                    percent_m_0_5)

                count_many_tick_h_l_m_05___1_5, count_many_tick_l_h_m_05___1_5 = self.get_many_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_0_5 + (percent_m_0_5 * .015),
                    percent_m_0_5)

                count_h_l_m_05___1, count_l_h_m_05___1 = self.get_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_0_5 + (percent_m_0_5 * .01),
                    percent_m_0_5)

                count_h_l_m_05___1_5, count_l_h_m_05___1_5 = self.get_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_0_5 + (percent_m_0_5 * .015),
                    percent_m_0_5)

                percent_m_1 = open - (open * .01)

                count_many_tick_h_l_m_1___1, count_many_tick_l_h_m_1___1 = self.get_many_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_1 + (percent_m_1 * .01),
                    percent_m_1)

                count_many_tick_h_l_m_1___1_5, count_many_tick_l_h_m_1___1_5 = self.get_many_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_1 + (percent_m_1 * .015),
                    percent_m_1)

                count_h_l_m_1___1, count_l_h_m_1___1 = self.get_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_1 + (percent_m_1 * .01),
                    percent_m_1)

                count_h_l_m_1___1_5, count_l_h_m_1___1_5 = self.get_tick_height_low___low_height(
                    array_h,
                    array_l,
                    percent_m_1 + (percent_m_1 * .015),
                    percent_m_1)

                open_percent_0_5, open_percent_m_0_2, percent_0_5_percent_1, percent_1_5_percent_2, percent_1_percent_1_5, percent_2_over, percent_m_0_2_percent_m_0_3, percent_m_0_3_percent_m_0_4, percent_m_0_4_percent_m_0_5, percent_m_0_5_less = self.create_metric_of_procent_group(
                    open, percent_0_5, percent_1, percent_1_5, percent_2, percent_m_0_2, percent_m_0_3, percent_m_0_4,
                    percent_m_0_5, result_data)

                high_data = [open_percent_0_5, percent_0_5_percent_1, percent_1_percent_1_5, percent_1_5_percent_2,
                             percent_2_over, count_h_l_over_1, count_many_tick_h_l_over_1,
                             count_h_l_over_2, count_many_tick_h_l_over_2]

                low_data = [open_percent_m_0_2, percent_m_0_2_percent_m_0_3, percent_m_0_3_percent_m_0_4,
                            percent_m_0_4_percent_m_0_5,
                            percent_m_0_5_less, count_l_h_over_1, count_many_tick_l_h_over_1, count_l_h_over_2,
                            count_many_tick_l_h_over_2]
                m_data_many_tick = [count_many_tick_h_l_m_05___1, count_many_tick_h_l_m_05___1_5,
                                    count_many_tick_l_h_m_05___1, count_many_tick_l_h_m_05___1_5,
                                    count_many_tick_h_l_m_1___1, count_many_tick_h_l_m_1___1_5,
                                    count_many_tick_l_h_m_1___1, count_many_tick_l_h_m_1___1_5
                                    ]
                m_data_tick = [count_h_l_m_05___1, count_h_l_m_05___1_5,
                               count_l_h_m_05___1, count_l_h_m_05___1_5,
                               count_h_l_m_1___1, count_h_l_m_1___1_5,
                               count_l_h_m_1___1, count_l_h_m_1___1_5
                               ]

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
        index += 1

        # print(high_data)
        # print(low_data)

        return high_data, low_data, index, m_data_many_tick, m_data_tick

    def create_metric_of_procent_group(self, open, percent_0_5, percent_1, percent_1_5, percent_2, percent_m_0_2,
                                       percent_m_0_3, percent_m_0_4, percent_m_0_5, result_data):
        open_percent_0_5 = len(
            result_data.where(
                # (result_data['2. high'] > open) & (result_data['2. high'] <= percent_0_5)).dropna())
                (result_data['High'] > open) & (result_data['High'] <= percent_0_5)).dropna())
        percent_0_5_percent_1 = len(
            result_data.where(
                # (result_data['2. high'] > percent_0_5) & (result_data['2. high'] <= percent_1)).dropna())
                (result_data['High'] > percent_0_5) & (result_data['High'] <= percent_1)).dropna())
        percent_1_percent_1_5 = len(
            result_data.where(
                # (result_data['2. high'] > percent_1) & (result_data['2. high'] <= percent_1_5)).dropna())
                (result_data['High'] > percent_1) & (result_data['High'] <= percent_1_5)).dropna())
        percent_1_5_percent_2 = len(
            result_data.where(
                # (result_data['2. high'] > percent_1_5) & (result_data['2. high'] <= percent_2)).dropna())
                (result_data['High'] > percent_1_5) & (result_data['High'] <= percent_2)).dropna())
        # percent_2_over = len(result_data.where(result_data['2. high'] > percent_2).dropna())
        percent_2_over = len(result_data.where(result_data['High'] > percent_2).dropna())
        open_percent_m_0_2 = len(
            result_data.where(
                # (result_data['3. low'] < open) & (result_data['3. low'] >= percent_m_0_2)).dropna())
                (result_data['Low'] < open) & (result_data['Low'] >= percent_m_0_2)).dropna())
        percent_m_0_2_percent_m_0_3 = len(
            result_data.where(
                # (result_data['3. low'] < percent_m_0_2) & (result_data['3. low'] >= percent_m_0_3)).dropna())
                (result_data['Low'] < percent_m_0_2) & (result_data['Low'] >= percent_m_0_3)).dropna())
        percent_m_0_3_percent_m_0_4 = len(
            result_data.where(
                # (result_data['3. low'] < percent_m_0_3) & (result_data['3. low'] >= percent_m_0_4)).dropna())
                (result_data['Low'] < percent_m_0_3) & (result_data['Low'] >= percent_m_0_4)).dropna())
        percent_m_0_4_percent_m_0_5 = len(
            result_data.where(
                # (result_data['3. low'] < percent_m_0_4) & (result_data['3. low'] >= percent_m_0_5)).dropna())
                (result_data['Low'] < percent_m_0_4) & (result_data['Low'] >= percent_m_0_5)).dropna())
        # percent_m_0_5_less = len(result_data.where(result_data['3. low'] < percent_m_0_5).dropna())
        percent_m_0_5_less = len(result_data.where(result_data['Low'] < percent_m_0_5).dropna())
        return open_percent_0_5, open_percent_m_0_2, percent_0_5_percent_1, percent_1_5_percent_2, percent_1_percent_1_5, percent_2_over, percent_m_0_2_percent_m_0_3, percent_m_0_3_percent_m_0_4, percent_m_0_4_percent_m_0_5, percent_m_0_5_less

    def create_percent_group_of_open(self, open):
        percent_2 = open + (open * .02)
        percent_1_5 = open + (open * .015)
        percent_1 = open + (open * .01)
        percent_0_5 = open + (open * .005)
        percent_m_0_2 = open - (open * .002)
        percent_m_0_3 = open - (open * .003)
        percent_m_0_4 = open - (open * .004)
        percent_m_0_5 = open - (open * .005)
        return percent_0_5, percent_1, percent_1_5, percent_2, percent_m_0_2, percent_m_0_3, percent_m_0_4, percent_m_0_5

    def addition_main_data_ticker(self):
        data = pd.read_excel(f'{self.min_buy}_{self.max_buy}_data_ticker.xlsx')
        for name in tqdm(data['TICKER']):
            time.sleep(3)
            # df = investpy.get_stock_historical_data(
            #     stock=name, country=self.country, from_date=self.from_date, to_date=self.current_date)
            # print(self.from_date_y)
            # print(self.current_date_y)
            try:
                df = yf.download(tickers=name, start=self.from_date_y, end=self.current_date_y)
            except Exception:
                traceback.print_exc()
                continue
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
                    data.loc[data.TICKER[data.TICKER == name].index.tolist()[0], '4_Open_point'] = np.array(
                        df['Open'][-5:][4])
                    data.loc[data.TICKER[data.TICKER == name].index.tolist()[0], '4_High_point'] = np.array(
                        df['High'][-5:][4])
                    data.loc[data.TICKER[data.TICKER == name].index.tolist()[0], '4_Low_point'] = np.array(
                        df['Low'][-5:][4])
                    data.loc[data.TICKER[data.TICKER == name].index.tolist()[0], '4_Close_point'] = np.array(
                        df['Close'][-5:][4])
            except:
                print()
                print(f'ticker: {name} not available data')
                continue

        self.bot.send(f'addition_main_data_ticker  is DONE!!')

        # data.to_excel(f'{self.min_buy}_{self.max_buy}_data_ticker.xlsx', index=False, header=True)
        # exit()

        data.to_excel(f'{self.min_buy}_{self.max_buy}_data_ticker.xlsx', index=False, header=True)
        # await self.bot.send( f'{self.min_buy}_{self.max_buy}_data_ticker.xlsx done')
        # self.bot.send_message('167381172', f'{self.min_buy}_{self.max_buy}_data_ticker.xlsx done')
        # self.bot.process_new_updates(['\zx'])

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
        # time.sleep(1)
        ua = UserAgent()
        headers = {'User-Agent': str(ua.chrome)}
        url_ticker = investpy.get_stock_company_profile(stock, self.country)['url']
        time.sleep(1)
        r = requests.get(url_ticker, headers=headers)
        tree = html.fromstring(r.content)
        name_stock_exchange = tree.xpath('//*[@id="DropdownBtn"]/i/text()')[0]
        return name_stock_exchange

    def get_info_yh(self, stock):
        ticker = yf.Ticker(stock)
        regularMarketVolume = ticker.info["regularMarketVolume"]
        averageVolume10days = ticker.info["averageVolume10days"]
        recommendationMean = ticker.info["recommendationMean"]
        recommendationKey = ticker.info["recommendationKey"]

        quickRatio = ticker.info["quickRatio"]
        currentRatio = ticker.info["currentRatio"]
        pegRatio = ticker.info["pegRatio"]
        shortRatio = ticker.info["shortRatio"]
        payoutRatio = ticker.info["payoutRatio"]

        return regularMarketVolume, averageVolume10days, recommendationMean, recommendationKey, \
               quickRatio, currentRatio, pegRatio, shortRatio, payoutRatio

        self.driver.delete_all_cookies()
        # op = webdriver.ChromeOptions()
        # op.add_argument('headless')
        # driver = webdriver.Chrome(options=op)
        self.driver.get(f'https://finance.yahoo.com/quote/{stock}/analysis?p={stock}')
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        element = self.driver.find_element_by_xpath('//*[@id="Col2-4-QuoteModule-Proxy"]/div/section/div/div/div[1]')
        # driver.close()

        return element.text

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

    @staticmethod
    def get_many_tick_height_low___low_height(array_h, array_l, percent_up, percent_down):
        h = 0
        l = 0
        for index, val in enumerate(array_h):
            if val > percent_up:  # p2
                for item in range(index + 1, len(array_l)):
                    if array_l[item] < percent_down:  # low
                        h += 1
                        break
        for index, val in enumerate(array_l):
            if val < percent_down:  # low
                for item in range(index + 1, len(array_h)):
                    if array_l[item] > percent_up:  # p2
                        l += 1
                        break
        return h, l

    @staticmethod
    def get_tick_height_low___low_height(array_h, array_l, percent_up, percent_down):
        index_h = 0
        is_flag_h = True
        h = 0
        while index_h < len(array_h):
            for index in range(index_h, len(array_h)):
                if array_h[index] > percent_up:
                    for item in range(index + 1, len(array_l)):
                        if array_l[item] < percent_down:
                            h += 1
                            is_flag_h = False
                            index_h = item
                            break
                if not is_flag_h:
                    break
            is_flag_h = True
            index_h += 1

        index_l = 0
        is_flag_l = True
        l = 0

        while index_l < len(array_l):
            for index in range(index_l, len(array_l)):
                if array_l[index] < percent_down:  # TODO
                    for item in range(index + 1, len(array_h)):
                        if array_h[item] > percent_up:
                            l += 1
                            is_flag_l = False
                            index_l = item
                            break
                if not is_flag_l:
                    break
            is_flag_l = True
            index_l += 1
        return h, l
