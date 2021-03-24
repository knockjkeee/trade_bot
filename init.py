from multiprocessing.dummy import Process

import config
from download import Parser
from logger_bot import TGBOT
import os
from multiprocessing import Pool
import threading

data = ['one', 'two', 'ads']
# tg_bot = 0

def get_tg_bot(bot):
    bot.init()
    # return tg_bot

def main():
    tg_bot = TGBOT(config.API_bot, data)
    # pool = Pool(processes=2)
    # pool.apply_async(get_tg_bot(tg_bot))
    # print(type(bot))
    parser = Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage, tg_bot)
    # pool = ThreadPool(4)
    # results = pool.map(parser.addition_main_data_ticker(), tg_bot.init())

    # p = Process(target=parser.addition_main_data_ticker())
    #
    #
    # p1.start()
    # p.start()
    # p1.join()
    # p.join()

    # tg_bot.init()
    # tg_bot.change_data_ticker(data)

    # file_name = f'{config.MIN_BUY}_{config.MAX_BUY}_{config.NAME_DATA}'
    #
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
