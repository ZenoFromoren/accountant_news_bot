import os
import requests
import asyncio
from bs4 import BeautifulSoup
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from time import sleep


URL_GK = "https://glavkniga.ru/"
URL_NN = "https://nalog-nalog.ru/"
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36"
}

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)

channel_id = "-1002029021519"

print(os.getenv("TOKEN"))


async def main():
    while True:
        sleep(5)
        response = requests.get(URL_GK, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        article_gk = soup.find("table", class_="news_block news_block_margin news_block_has_image")
        title_gk = article_gk.find("a", class_="news_block_hdg")
        url_gk = title_gk.get("href")
        post_id_gk = article_gk.get("data-news_id")
        with open("last_post_id_gk.txt") as file:
            last_post_id_gk = file.read()

        if post_id_gk != last_post_id_gk:
            text = f"{title_gk.text}\n https://glavkniga.ru{url_gk}"
            await bot.send_message(channel_id, text)
            with open("last_post_id_gk.txt", "w") as file:
                file.write(post_id_gk.text)

        sleep(5)
        response = requests.get(URL_NN, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title_nn = soup.find("a", class_="news-list_item_title")
        url_nn = title_nn.get("href")
        with open("last_post_title_nn.txt") as file:
            last_post_title_nn = file.read()
            print(title_nn)
            print(last_post_title_nn)

        if title_nn.text != last_post_title_nn:
            text = f"{title_nn.text}\n {url_nn}"
            await bot.send_message(channel_id, text)
            with open("last_post_title_nn.txt", "w") as file:
                file.write(title_nn.text)


asyncio.run(main())

executor.start_polling(dp, skip_updates=True)