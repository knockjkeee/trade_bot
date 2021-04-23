from download import Parser
import os
from logger_bot import TGBOT
from multiprocessing import Process, Manager, managers
from multiprocessing.managers import BaseManager
import config
from data import Data

data = Data()
bot = TGBOT(config.API_bot, config.ID_chat)


# bot.init()

# bot.__class__(TGBOT)
# parser = Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage, config.NAME_DATA,  bot)
# print(bot)
# parser.__dict__['bot'] = bot
# bot.set_parser(parser)


def init_bot(items):
    # parser = queue.get_nowait()
    # bot.set_parser_item(parse_item)
    bot.set_data(items)
    # bot.set_parser(parser)
    bot.init()


def process(items):
    # p = Process(target=init_bot, args=(q, ))
    p = Process(target=init_bot, args=(items,))
    p.start()


def main():
    data_stock = Manager().list()
    data_stock.append([])
    data_stock.append([])
    # print(data_stock)
    # data_parse = Manager().list()

    # BaseManager.register('Parser', Parser)
    # manager = BaseManager()
    # manager.register('parser', Parser)
    # manager.start()

    # parser = manager.Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage, config.NAME_DATA, bot)
    # parser

    # queue = Manager().Queue()
    parser = Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage, config.NAME_DATA, bot)
    # data_stock.append([parser])

    # queue.put_nowait(parser)

    print("test")
    # process(data_stock, queue)
    process(data_stock)

    # bot.set_parser_item(data_parse)
    bot.set_data(data_stock)
    print("test")

    if is_data_exist(config.NAME_DATA):
        for stock in parser.search_relevant_ticker():
            print(f'diiiir:  {stock}')
            # data_stock.append(stock)
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
