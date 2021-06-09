import investpy
from collections import Counter
import pandas as pd
import config

stocks = investpy.get_stocks()

print(Counter(stocks.country.tolist()).most_common())

united_states_list = stocks[stocks.country == 'united states'].symbol.tolist()
close_price = [101] * len(united_states_list)
# frame = pd.DataFrame(united_states_list, columns=['TICKER'])
frame = pd.DataFrame(list(zip(united_states_list,close_price)), columns=['TICKER', 'CLOSE'])

data_stocks = pd.read_excel(config.NAME_DATA, index_col=False)[['TICKER', 'CLOSE']]


# res = pd.merge(data_stocks, frame, on=['TICKER'], how='left').dropna()
# res.to_excel('data_tinkov_NEW.xlsx', index=True, header=True)


# res = pd.merge(data_stocks, frame, on=['TICKER'], how='left').dropna()

# res = data_stocks.compare(frame, align_axis=0)


# df = pd.concat([data_stocks, frame])
# res = df.reset_index(drop=True)
res = pd.concat([data_stocks,frame]).drop_duplicates()


print(frame)
print(data_stocks)
print(res)

