import os
import requests
import asyncio
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher
from time import sleep
from dotenv import load_dotenv
from Parser import Parser


dotenv_path = os.path.join(os.path.dirname(__file__), ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher()

channel_id = os.environ["CHANNEL_ID"]

parser = Parser(bot, channel_id)


async def main():
    while True:
        await parser.parse_gk()
        await parser.parse_nn()
        await parser.parse_article_nn()
        sleep(5)


asyncio.run(main())

dp.start_polling(dp, skip_updates=True)
