from datetime import date
import numpy as np

import yfinance as yf

current_date_y = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day)
from_date_y = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day - 1)


# aapl.info["volume"]
ticker = yf.Ticker("AA")
download = yf.download(tickers="AA", start=current_date_y,  interval='2m', prepost=False)

print(download)

print(np.array(download['Volume']))

print(ticker.info)

# print(ticker.info["volume"])
print(ticker.info["regularMarketVolume"])
print(ticker.info["averageVolume10days"])
print(ticker.info["recommendationMean"])
print(ticker.info["recommendationKey"])


# payoutRatio
# shortRatio
# pegRatio
# currentRatio
# quickRatio
print(ticker.info["quickRatio"])
print(ticker.info["currentRatio"])
print(ticker.info["pegRatio"])
print(ticker.info["shortRatio"])
print(ticker.info["payoutRatio"])