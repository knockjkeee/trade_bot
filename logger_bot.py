# import telebot
from threading import Thread
import logging
import config
from multiprocessing import Process
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)


def listener(messages):
    for m in messages:
        print(str(m.from_user))
        print(str(m))


class TGBOT():
    """"""

    def __init__(self, api_key, data):
        self.bot = telebot.TeleBot(api_key)
        self.data = data

        # self.bot.set_update_listener(listener)
        # self.bot.polling()

        @self.bot.message_handler(commands=['start', 'help'])
        def _send_welcome(message):
            # print(type(message.from_user.id))
            self.send_welcome(message)

        @self.bot.message_handler(commands=['menu'])
        def _send_collage(message):
            self.send_collage(message)

        @self.bot.message_handler(commands=['dir'])
        def _get_ticker(message):
            self.get_ticker(message)

        @self.bot.message_handler(commands=['drop'])
        def _drop(message):
            self.drop(message)

        self.bot.set_update_listener(listener)
        # self.bot.process_new_updates()
        # self.bot.polling()
        # return self.bot

    def drop(self, message):
        self.data = self.data[1:]

    def get_ticker(self, message):
        self.bot.send_message('167381172', str(self.data))

    def change_data_ticker(self, data):
        self.data = data

    def send_collage(self, message):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = telebot.types.KeyboardButton('/start')
        itembtn2 = telebot.types.KeyboardButton('/dir')
        itembtn3 = telebot.types.KeyboardButton('/help')
        itembtn4 = telebot.types.KeyboardButton('/drop')
        markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
        # markup.resize_keyboard()
        self.bot.send_message('167381172', "Choose one letter:", reply_markup=markup)

    def send_welcome(self, message):
        # print(type(message.from_user.id))
        self.bot.reply_to(message, "hello")

    def init(self):
        self.bot.set_update_listener(listener)
        # self.bot.prone()
        # return self.bot


async def echo(message: types.Message):
    await message.answer(message.text)


async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


class LGBT(Thread):
    """"""

    def __init__(self, api_key, data):

        self.bot = Bot(token=api_key)
        self.dp = Dispatcher(self.bot)
        Thread.__init__(self)
        self.daemon = True
        self.start()

        """Constructor for LGBT"""

        @self.dp.message_handler(commands=['start', 'help'])
        async def _send_welcome(message: types.Message):
            await send_welcome(message)

        @self.dp.message_handler()
        async def _echo(message: types.Message):
            await echo(message)

    def pooling(self):
        executor.start_polling(self.dp, skip_updates=True)
