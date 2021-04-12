from datetime import date
import numpy as np

import yfinance as yf

current_date_y = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day)
from_date_y = str(date.today().year) + '-' + str(date.today().month) + '-' + str(date.today().day - 1)

download = yf.download(tickers="TDS", start=current_date_y,  interval='2m', prepost=True)

print(download)

print(np.array(download['Volume']))
