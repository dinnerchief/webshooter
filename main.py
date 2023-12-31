import logging
import base64
import io
import re
import configs

from selenium import webdriver
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=configs.API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):
    mess = message.text
    pattern = r'(https?:\/\/(?:www\.)?[^\/\s]+)'
    matches = re.findall(pattern, mess)

    if matches == []:
        await message.answer('Пожалуйста, отправьте ссылку на веб-сайт. Например https://youtube.com/')
        return

    await message.answer("Подождите секунду")

    options = webdriver.ChromeOptions()
    options.add_argument("--lang=ru")
    options.add_argument("start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(matches[0])
    file = driver.get_screenshot_as_base64()

    image_data = base64.b64decode(file)

    photo_stream = io.BytesIO(image_data)
    photo_stream.name = f'{matches[0]}.jpg'
    photo = types.InputFile(photo_stream)
    await message.answer_photo(photo)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)