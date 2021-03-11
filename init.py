import config
from download import Parser
import os


def main():
    parser = Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage)

    if not is_data_exist(config.NAME_DATA):
        parser.search_relevant_ticker()
    else:
        parser.create_data_ticker_min_max_by_close()
        parser.search_relevant_ticker()

    # parser.addition_main_data_ticker()


def is_data_exist(file_name):
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name == file_name:
                return True
            else:
                return False


if __name__ == '__main__':
    main()
