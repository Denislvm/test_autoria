import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hlink, hbold

from auth_data import token
from main import collect_cars

import json

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_button = ['Toyota Sequoia']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer("Toyota Sequoia", reply_markup=keyboard)


@dp.message_handler(Text(equals='Toyota Sequoia'))
async def get_cars(message: types.Message):
    await message.answer("Please wait for load all Toyota Sequoia cars...")

    collect_cars()

    with open('result.json') as file:
        data = json.load(file)
        print(data)

    print(data)

    for item in data:
        card = f'{hlink(item.get("link"), item.get("mark"))}\n' \
            f'{hbold("Цiна: ")} {item.get("price")} {item.get("mileage")} {item.get("place")} \n'

        await message.answer(card)
        await asyncio.sleep(1)


def main():
    executor.start_polling(dp)



if __name__ == '__main__':
    main()
