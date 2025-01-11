import requests
import asyncio
from bs4 import BeautifulSoup
from aiogram.enums.parse_mode import ParseMode


class Parser:
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel_id = channel_id
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36"
        }
        self.URL_GK = "https://glavkniga.ru"
        self.URL_NN = "https://nalog-nalog.ru"

    async def parse_gk(self):
        response = requests.get(self.URL_GK, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        article_gk = soup.find("div", class_="news_block")

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
            text = f"{title_gk_text}\n\n{self.URL_GK}{post_url_gk}"
            await self.bot.send_message(self.channel_id, text)
            with open("gk_last.post.txt", "w") as file:
                file.write(post_id_gk)

    async def parse_nn(self):
        response = requests.get(self.URL_NN, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        title_nn = soup.find("a", class_="news-list_item_title")
        post_url_nn = title_nn.get("href")

        try:
            with open("nn_last.post.txt", encoding="utf-8") as file:
                last_post_title_nn = file.read()
        except:
            last_post_title_nn = None

        if title_nn.text != last_post_title_nn:
            text = f"{title_nn.text}\n\n{post_url_nn}"
            await self.bot.send_message(self.channel_id, text)
            with open("nn_last.post.txt", "w", encoding="utf-8") as file:
                file.write(title_nn.text)

    async def parse_article_nn(self):
        response = requests.get(self.URL_NN, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        article_nn = soup.find("div", class_="article-list_item_content")
        title_nn = article_nn.find("a", class_="article-list_item_title")
        article_text_nn = article_nn.find("div", class_="article-list_item_text").text.strip()
        post_url_nn = title_nn.get("href")

        try:
            with open("nn_last.article.txt", encoding="utf-8") as file:
                last_article_title_nn = file.read()
        except:
            last_article_title_nn = None

        if title_nn.text != last_article_title_nn:
            text = f"<b>{title_nn.text}</b>\n\n{article_text_nn}\n\n{post_url_nn}"
            await self.bot.send_message(self.channel_id, text, parse_mode=ParseMode.HTML)
            with open("nn_last.article.txt", "w", encoding="utf-8") as file:
                file.write(title_nn.text)
