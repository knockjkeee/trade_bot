import os
import logging
import config
from multiprocessing import Process
from aiogram import Bot, Dispatcher, executor, types
from download import Parser

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_bot)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    # await bot.send_message(config.ID_chat, "TEST!!!!!!")
    # await send("sda")
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


async def send(message):
    await bot.send_message(config.ID_chat, message)


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.answer(message.text)


def up_bot():
    executor.start_polling(dp, skip_updates=True)


def polling_bot():
    p = Process(target=up_bot)
    p.start()


async def app():
    parser = Parser(config.COUNTRY, config.MIN_BUY, config.MAX_BUY, config.API_alpha_vantage, config.NAME_DATA, bot)

    # if is_data_exist(config.NAME_DATA):
    #     parser.search_relevant_ticker()
    # else:
    #     parser.create_data_ticker_min_max_by_close()
    #     parser.search_relevant_ticker()

    await parser.addition_main_data_ticker()


def is_data_exist(file_name):
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if name == file_name:
                return True
    return False


if __name__ == '__main__':
    polling_bot()
    app()
