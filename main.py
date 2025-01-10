import os
import requests
import asyncio
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher
from time import sleep
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

URL_GK = "https://glavkniga.ru/"
URL_NN = "https://nalog-nalog.ru/"
headers = {
    "User-Agent": os.environ["USER_AGENT"]
}

bot = Bot(token=os.environ["TOKEN"])
dp = Dispatcher()

channel_id = os.environ["CHANNEL_ID"]

async def main():
    while True:
        sleep(5)
        response = requests.get(URL_GK, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        article_gk = soup.find(
            "div", class_="news_block"
        )
        
        title_gk = article_gk.find("a", class_="news_block_hdg_f")

        title_gk_text = title_gk.text
        post_url_gk = title_gk.get("href")
        post_id_gk = post_url_gk.split("/")[-1]

        try:
            with open("gk_last.post.txt") as file:
                last_post_id_gk = file.read()
        except:
            last_post_id_gk = None

        if post_id_gk != last_post_id_gk:
            text = f"{title_gk_text}\nhttps://glavkniga.ru{post_url_gk}"
            await bot.send_message(channel_id, text)
            with open("gk_last.post.txt", "w") as file:
                file.write(post_id_gk)

        # response = requests.get(URL_NN, headers=headers)
        # soup = BeautifulSoup(response.text, "html.parser")

        # title_nn = soup.find("a", class_="news-list_item_title")
        # url_nn = title_nn.get("href")
        # with open("last_post_title_nn.txt") as file:
        #     last_post_title_nn = file.read()
        #     # print(title_nn.text)
        #     # print(last_post_title_nn)
        #     # print(title_nn.text == last_post_title_nn)

        # if title_nn.text != last_post_title_nn:
        #     text = f"{title_nn.text}\n{url_nn}"
        #     await bot.send_message(channel_id, text)
        #     with open("last_post_title_nn.txt", "w") as file:
        #         file.write(title_nn.text)


asyncio.run(main())

dp.start_polling(dp, skip_updates=True)
