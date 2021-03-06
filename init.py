import time
from multiprocessing.dummy import Process

import config
from download import Parser
from logger_bot import LGBT
import os
from multiprocessing import Pool, Process
import threading
import up

data = ['one', 'two', 'ads']


def main():
    parser = Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage, config.NAME_DATA)

    file_name = f'{config.MIN_BUY}_{config.MAX_BUY}_{config.NAME_DATA}'

    if is_data_exist(config.NAME_DATA):
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
    return False


if __name__ == '__main__':
    main()

