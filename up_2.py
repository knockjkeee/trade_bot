import time
import os
import random
import string

import telebot
import config
from multiprocessing import Process

from download import Parser

bot_tg = telebot.TeleBot(config.API_bot)

DIROS = ["one", "two", "free"]


def listener(messages):
    for m in messages:
        print(str(m.from_user))
        print(str(m))


@bot_tg.message_handler(commands=['menu'])
def send_collage(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('/start')
    itembtn2 = telebot.types.KeyboardButton('/dir')
    itembtn3 = telebot.types.KeyboardButton('/append')
    itembtn4 = telebot.types.KeyboardButton('/drop')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    # markup.resize_keyboard()
    bot_tg.send_message('167381172', "Choose one function:", reply_markup=markup)


@bot_tg.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # print(type(message.from_user.id))
    # bot_tg.send_message('167381172', "Choose one letter:")
    bot_tg.reply_to(message, "hello")


@bot_tg.message_handler(commands=['dir'])
def get_data(message):
    data = get__data(DIROS)
    bot_tg.send_message(config.ID_chat, str(data))


@bot_tg.message_handler(commands=['drop'])
def drop_data(message):
    # del DIROS[-1]
    data = dr_data(DIROS)
    bot_tg.send_message(config.ID_chat, str(data))


@bot_tg.message_handler(commands=['append'])
def append_data(message):
    data = append_random_data(DIROS)
    bot_tg.send_message(config.ID_chat, str(data))


def get__data(data):
    return data


def append_random_data(data):
    letters = string.ascii_lowercase
    result = (''.join(random.choice(letters) for i in range(10)))
    data.append(result)
    return data


def dr_data(data):
    if len(data) == 0:
        pass
    else:
        del data[-1]
    return data


def init():
    bot_tg.set_update_listener(listener)
    bot_tg.polling(none_stop=True)


def polling():
    p = Process(target=init)
    p.start()


def is_data_exist(file_name):
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name == file_name:
                return True
    return False


def scrappy(bot):
    parser = Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage, config.NAME_DATA, bot)

    if is_data_exist(config.NAME_DATA):
        parser.search_relevant_ticker()
    else:
        parser.create_data_ticker_min_max_by_close()
        parser.search_relevant_ticker()

    # parser.addition_main_data_ticker()


if __name__ == '__main__':
    polling()
    # print(DIROS)
    scrappy(bot_tg)
