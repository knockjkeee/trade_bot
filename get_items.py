import pandas as pd
import config

data = pd.read_excel(f'{config.interval}_data_ticker.xlsx')

# print(data.to_markdown())

result = data[
    (data.m_data_count_l_h_0_5_1_4 > 2) &
    (data.m_data_count_l_h_0_5_1_2 > 1) &
    (data.m_data_count_l_h_0_5_1_5_4 > 2) &
    (data.m_data_count_l_h_0_5_1_5_2 > 1) &
    (data.m_data_count_l_h_1_1_4 > 2) &
    (data.m_data_count_l_h_1_1_2 > 1) &
    (data.m_data_count_l_h_1_1_5_4 > 2) &
    (data.m_data_count_l_h_1_1_5_2 > 1) &
    (data.res_mt_l_h_o_2_4 > 4) &
    (data.res_mt_l_h_o_2_2 > 0) &
    # (data.Tech_sell < 1) &
    (data.regVolume > 50000) &
    (data.Yahoo_Rating < 2.9)
]

print(f'total count: {len(result.TICKER.tolist())}, list tickers: {result.TICKER.tolist()}')