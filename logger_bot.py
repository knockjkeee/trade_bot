import telebot
import logging
import config
import random
import string

# from typing import cast

# from download import Parser

logging.basicConfig(level=logging.INFO)


def listener(messages):
    for m in messages:
        print(str(m.from_user))
        print(str(m))


class TGBOT(object):
    """"""

    def __init__(self, api_key, id_chat):
        self.id_chat = id_chat
        self.data = [[], []]
        self.data_parse_item = []
        # self.parser = None
        # self.data_data = data
        # print(f'init {data}')
        # print(f'init2 {self.data_data}')
        self.bot = telebot.AsyncTeleBot(api_key)

        # self.bot.set_update_listener(listener=listener)

        @self.bot.message_handler(commands=['start', 'help'])
        def _send_welcome(message):
            # print(type(message.from_user.id))
            self.send_welcome(message)

        @self.bot.message_handler(commands=['menu'])
        def _send_collage(message):
            self.get_menu(message)

        @self.bot.message_handler(commands=['dir'])
        def _get_ticker(message):
            self.get_data(message)

        @self.bot.message_handler(commands=['drop'])
        def _drop(message):
            self.drop_item(message)

        @self.bot.message_handler(commands=['append'])
        def _append(message):
            self.append_data(message)

        @self.bot.message_handler(commands=['good'])
        def _good(message):
            self.get_parse(message)

    # def set_parser(self, p):
    #     self.parser = p



    def append_items(self, item):
        self.data.append(item)

    def get_parse(self, message):
        # self.parser.search_relevant_ticker()
        self.bot.send_message(self.id_chat, str(self.data[1]))
        # self.bot.send_message(self.id_chat, str(self.data_parse_item))


    def set_data(self, data):
        self.data = data

    def set_parser_item(self, p):
        self.data_parse_item = p

    def get_data(self, message):
        # self.bot.send_message(self.id_chat, str(self.data_parse_item))
        self.bot.send_message(self.id_chat, str(self.data[0]))
        self.bot.send_message(self.id_chat, str(len(self.data[0])))

    def append_data(self, message):
        letters = string.ascii_lowercase
        result = (''.join(random.choice(letters) for i in range(10)))
        self.data.append(result)
        self.bot.send_message(self.id_chat, str(self.data))

    def drop_item(self, message):
        if len(self.data) == 0:
            pass
        else:
            del self.data[-1]
        self.bot.send_message(self.id_chat, str(self.data))


    def get_menu(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = telebot.types.KeyboardButton('/start')
        itembtn2 = telebot.types.KeyboardButton('/dir')
        itembtn3 = telebot.types.KeyboardButton('/append')
        itembtn4 = telebot.types.KeyboardButton('/drop')
        itembtn5 = telebot.types.KeyboardButton('/good')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
        # markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        # markup.resize_keyboard()
        self.bot.send_message(self.id_chat, "Choose one items:", reply_markup=markup)

    def send_welcome(self, message):
        msg = '''
            Hello!
            check menu -> /menu
        '''
        self.bot.reply_to(message, msg)

    def send(self, msg):
        self.bot.send_message(self.id_chat, msg)

    def add_item_to_data(self, item):
        # self.data.append(item)
        self.data[0] = item[0]
        self.data[1] = item[1]

    def add_count_of_parse(self, item):
        print(item)
        self.data_parse_item = [item]
        print(self.data_parse_item)

    def init(self):
        self.bot.set_update_listener(listener)
        self.bot.polling(none_stop=True)
        # self.bot.prone()
        # return self.bot
