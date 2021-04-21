# import multiprocessing
#
# # from datetime import date
# #
# # import investpy
# # import numpy as np
# # import config
# #
# # import yfinance as yf
# #
# # current_date_y = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day)
# # from_date_y = str(date.today().year) + '-' + str(date.today().month - 1) + '-' + str(date.today().day)
# # #
# # #
# # # # aapl.info["volume"]
# # # ticker = yf.Ticker("FNKO")
# # download = yf.download(tickers="MMM", start=from_date_y, end=current_date_y, interval='1d', prepost=False)
# #
# #
# #
# #
# #
# # #
# # print(download[['Close', 'Open', 'High']])
# # #
# # # print(np.array(download['Volume']))
# # #
# # # print(ticker.info)
# # #
# # # # print(ticker.info["volume"])
# # # print(ticker.info["regularMarketVolume"])
# # # print(ticker.info["averageVolume10days"])
# # # print(ticker.info["recommendationMean"])
# # # print(ticker.info["recommendationKey"])
# # #
# # #
# # # # payoutRatio
# # # # shortRatio
# # # # pegRatio
# # # # currentRatio
# # # # quickRatio
# # # print(ticker.info["quickRatio"])
# # # print(ticker.info["currentRatio"])
# # # print(ticker.info["pegRatio"])
# # # print(ticker.info["shortRatio"])
# # # print(ticker.info["payoutRatio"])
# #
# # technical_indicators = investpy.technical.technical_indicators(
# #     # technical_indicators = investpy.technical_indicators(
# #     "AA", config.COUNTRY, 'stock', interval='daily')
# # print(technical_indicators)
# import time
# import os
#
#
# class Temp(object):
#     """"""
#
#     def __init__(self, ):
#         self.data = []
#         """Constructor for Temp"""
#
#     def apnd(self, item):
#         self.data.append(item)
#
#     def get(self):
#         return self.data
#
#     def set(self, data):
#         self.data = data
#
#
# temp = Temp()
# # tt = Temp()
#
#
#
# def init(data):
#     for i in range(10):
#         print(i)
#         time.sleep(2)
#         data.append(i)
#         # print(temp.get())
#
#
# def proccess(data):
#     # print(temp)
#     process = multiprocessing.Process(target=init, name='test', args=(data, ))
#     process.start()
#     # process.join()
#
#
# def main():
#     data = multiprocessing.Manager().list()
#     temp.set(data)
#     proccess(data)
#     # for p in multiprocessing.active_children():
#     #     if p.name == "test":
#     #         print(p.pid)
#     #         print(os.getpid())
#     #         print(p)
#
#     while True:
#         # print(temp)
#         time.sleep(2)
#         print(temp.get())
#
#
# if __name__ == '__main__':
#     main()
#
# # from multiprocessing import Process, Manager
# #
# # def f(d, l):
# #     d[1] = '1'
# #     d['2'] = 2
# #     d[0.25] = None
# #     l.reverse()
# #
# # def pool(d, l):
# #     p = Process(target=f, args=(d, l))
# #     p.start()
# #     # p.join()
# #
# # if __name__ == '__main__':
# #     with Manager() as manager:
# #         d = manager.dict()
# #         l = manager.list(range(10))
# #
# #         pool(d, l)
# #
# #         print(d)
# #         print(l)

lc = ['a','aa', 'aaa', 'aaa', 'aaaa','aaaa']

print(lc[:5])