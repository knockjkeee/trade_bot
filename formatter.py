import pandas as pd

stocks_buying_range = ["25_35", "35_45", "45_55", "55_65", "65_75", "75_85", "85_95"]
# stocks_buying_range = ["25_35", "35_45"]


def main():
    result = pd.DataFrame()
    for name in stocks_buying_range:
        excel = pd.read_excel(f'history/{name}/_data_ticker_1903.xlsx')
        result = pd.concat([result, excel])
    result.to_excel('summary.xlsx', index=False)


def search_ready_file():
    result = pd.DataFrame()
    for name in stocks_buying_range:
        excel = pd.read_excel(f'{name}_data_ticker.xlsx')
        # excel = pd.read_excel(f'history/{name}/data_ticker_1803.xlsx', skiprows=7)
        result = pd.concat([result, excel.dropna(subset=['TICKER'])])
    # print(result)
    result.to_excel('summary_R.xlsx', index=False)

if __name__ == '__main__':
    # main()
    search_ready_file()
