import requests
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
        self.URL_KLERK = "https://www.klerk.ru"
        self.URL_BUHGALTERIA = "https://www.buhgalteria.ru"
        self.URL_KDELO = "https://www.kdelo.ru"

    async def parse_gk(self):
        response = requests.get(self.URL_GK, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        article_gk = soup.find("div", class_="news_block")

        title_gk = article_gk.find("a", class_="news_block_hdg_f")

        title_gk_text = title_gk.text
        post_url_gk = title_gk.get("href")
        post_id_gk = post_url_gk.split("/")[-1]

        response = requests.get(
            f"{self.URL_GK}/news/{post_id_gk}", headers=self.headers
        )
        soup = BeautifulSoup(response.text, "html.parser")

        image_gk_src = (
            soup.find("div", id="news_content").find("picture").find("img").get("src")
        )

        try:
            with open("gk_last.post.txt") as file:
                last_post_id_gk = file.read()
        except:
            last_post_id_gk = None

        if post_id_gk != last_post_id_gk:
            text = f"<b>{title_gk_text}</b>\n\n{self.URL_GK}{post_url_gk}"
            if image_gk_src:
                await self.bot.send_photo(
                    self.channel_id,
                    image_gk_src,
                    caption=text,
                    parse_mode=ParseMode.HTML,
                )
            else:
                await self.bot.send_message(
                    self.channel_id, text, parse_mode=ParseMode.HTML
                )
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
            text = f"<b>{title_nn.text}</b>\n\n{post_url_nn}"
            await self.bot.send_message(
                self.channel_id, text, parse_mode=ParseMode.HTML
            )
            with open("nn_last.post.txt", "w", encoding="utf-8") as file:
                file.write(title_nn.text)

    async def parse_article_nn(self):
        response = requests.get(self.URL_NN, headers=self.headers)
        soup = BeautifulSoup(response.text, "html.parser")

        article_nn = soup.find("div", class_="article-list_item_content")
        title_nn = article_nn.find("a", class_="article-list_item_title")
        article_text_nn = article_nn.find(
            "div", class_="article-list_item_text"
        ).text.strip()
        post_url_nn = title_nn.get("href")

        try:
            with open("nn_last.article.txt", encoding="utf-8") as file:
                last_article_title_nn = file.read()
        except:
            last_article_title_nn = None

        if title_nn.text != last_article_title_nn:
            text = f"<b>{title_nn.text}</b>\n\n{article_text_nn}\n\n{post_url_nn}"
            await self.bot.send_message(
                self.channel_id, text, parse_mode=ParseMode.HTML
            )
            with open("nn_last.article.txt", "w", encoding="utf-8") as file:
                file.write(title_nn.text)

    async def parse_klerk(self):
        try:
            response = requests.get(self.URL_KLERK, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            title_klerk = soup.find("section").find("li").find("a")
            post_url_klerk = title_klerk.get("href")
            post_id_klerk = post_url_klerk.split("/")[-2]

            try:
                with open("klerk_last.post.txt", encoding="utf-8") as file:
                    last_post_id_klerk = file.read()
            except:
                last_post_id_klerk = None

            if post_id_klerk != last_post_id_klerk:
                text = f"<b>{title_klerk.text}</b>\n\n{self.URL_KLERK}{post_url_klerk}"
                await self.bot.send_message(
                    self.channel_id, text, parse_mode=ParseMode.HTML
                )
                with open("klerk_last.post.txt", "w", encoding="utf-8") as file:
                    file.write(post_id_klerk)
        except:
            print("parse klerk failed")

    async def parse_article_klerk(self):
        try:
            response = requests.get(self.URL_KLERK, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            article_klerk = soup.find("section", id="top-feed").find(
                "a", class_="group"
            )
            article_url_klerk = article_klerk.get("href")
            article_title_klerk = article_klerk.find("h3").text.strip()
            article_text_klerk = article_klerk.find("p").text.strip()

            try:
                with open("klerk_last.article.txt", encoding="utf-8") as file:
                    article_title_last_klerk = file.read()
            except:
                article_title_last_klerk = None

            if article_title_klerk != article_title_last_klerk:
                text = f"<b>{article_title_klerk}</b>\n\n{article_text_klerk}\n\n{self.URL_KLERK}{article_url_klerk}"
                await self.bot.send_message(
                    self.channel_id, text, parse_mode=ParseMode.HTML
                )
                with open("klerk_last.article.txt", "w", encoding="utf-8") as file:
                    file.write(article_title_klerk)
        except:
            print("parse article klerk failed")

    async def parse_buhgalteria(self):
        try:
            response = requests.get(self.URL_BUHGALTERIA, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            post_buhgalteria = soup.find_all("div", class_="hidden-xs")[3].find(
                "article"
            )

            post_title_buhgalteria = post_buhgalteria.find("h3").find("a")
            post_title_text_buhgalteria = post_title_buhgalteria.text
            post_url_buhgalteria = post_title_buhgalteria.get("href")
            post_buhgalteria_id = post_buhgalteria.parent.get("id")

            try:
                with open("buhgalteria_last.post.txt", encoding="utf-8") as file:
                    post_last_id_buhgalteria = file.read()
            except:
                post_last_id_buhgalteria = None

            if post_buhgalteria_id != post_last_id_buhgalteria:
                text = f"<b>{post_title_text_buhgalteria}</b>\n\n{self.URL_BUHGALTERIA}{post_url_buhgalteria}"
                await self.bot.send_message(
                    self.channel_id, text, parse_mode=ParseMode.HTML
                )
                with open("buhgalteria_last.post.txt", "w", encoding="utf-8") as file:
                    file.write(post_buhgalteria_id)
        except:
            print("parse buhgalteria failed")

    async def parse_buhgalteria_article(self):
        try:
            response = requests.get(self.URL_BUHGALTERIA, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            article_buhgalteria = soup.find("article")

            article_title_buhgalteria = article_buhgalteria.find("h3").find("a")
            article_title_text_buhgalteria = article_title_buhgalteria.text.strip()
            article_text_buhgalteria = article_buhgalteria.find(
                "span", class_="text"
            ).text.strip()
            article_url_buhgalteria = article_title_buhgalteria.get("href")
            article_buhgalteria_id = article_buhgalteria.find("div").get("id")
            article_buhgalteria_image = article_buhgalteria.find("img").get("src")

            try:
                with open("buhgalteria_last.article.txt", encoding="utf-8") as file:
                    article_last_id_buhgalteria = file.read()
            except:
                article_last_id_buhgalteria = None

            if article_buhgalteria_id != article_last_id_buhgalteria:
                text = f"<b>{article_title_text_buhgalteria}</b>\n\n{article_text_buhgalteria}\n\n{self.URL_BUHGALTERIA}{article_url_buhgalteria}"
                if article_buhgalteria_image:
                    await self.bot.send_photo(
                        self.channel_id,
                        f"{self.URL_BUHGALTERIA}{article_buhgalteria_image}",
                        caption=text,
                        parse_mode=ParseMode.HTML,
                    )
                else:
                    await self.bot.send_message(
                        self.channel_id, text, parse_mode=ParseMode.HTML
                    )
                with open(
                    "buhgalteria_last.article.txt", "w", encoding="utf-8"
                ) as file:
                    file.write(article_buhgalteria_id)
        except:
            print("parse buhgalteria article failed")

    async def parse_kdelo_article(self):
        try:
            response = requests.get(self.URL_KDELO, headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            kdelo_article = soup.find("div", class_="defaultBlock__item")

            kdelo_article_title = kdelo_article.find(
                "a", class_="defaultBlock__itemTitleLink"
            )
            kdelo_article_title_text = kdelo_article_title.text
            kdelo_article_title_url = kdelo_article_title.get("href")
            kdelo_article_text = kdelo_article.find(
                "span", class_="defaultBlock__itemDescriptionInside"
            ).text.strip()

            try:
                with open("kdelo_last.article.txt", encoding="utf-8") as file:
                    article_title_last_kdelo = file.read()
            except:
                article_title_last_kdelo = None

            if kdelo_article_title_text != article_title_last_kdelo:
                text = f"<b>{kdelo_article_title_text}</b>\n\n{kdelo_article_text}\n\n{self.URL_KDELO}{kdelo_article_title_url}"

                await self.bot.send_message(
                    self.channel_id, text, parse_mode=ParseMode.HTML
                )
                with open("kdelo_last.article.txt", "w", encoding="utf-8") as file:
                    file.write(kdelo_article_title_text)

        except:
            print("failed parse kdelo article")

    async def parse_kdelo_new(self):
        try:
            response = requests.get(f"{self.URL_KDELO}/news", headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            kdelo_article_title = soup.find("a", class_="defaultBlock__itemTitleLink")
            kdelo_article_title_text = kdelo_article_title.text.strip()
            kdelo_article_title_url = kdelo_article_title.get("href")

            try:
                with open("kdelo_last.new.txt", encoding="utf-8") as file:
                    article_title_last_kdelo = file.read()
            except:
                article_title_last_kdelo = None

            if kdelo_article_title_text != article_title_last_kdelo:
                text = f"<b>{kdelo_article_title_text}</b>\n\n{self.URL_KDELO}{kdelo_article_title_url}"

                await self.bot.send_message(
                    self.channel_id, text, parse_mode=ParseMode.HTML
                )

                with open("kdelo_last.new.txt", "w", encoding="utf-8") as file:
                    file.write(kdelo_article_title_text)

        except:
            print("failed parse kdelo new")

    async def parse_kdelo_question(self):
        try:
            response = requests.get(f"{self.URL_KDELO}/question", headers=self.headers)
            soup = BeautifulSoup(response.text, "html.parser")

            kdelo_question_title = soup.find("a", class_="defaultBlock__itemTitleLink")
            kdelo_question_title_text = kdelo_question_title.text.strip()
            kdelo_question_title_url = kdelo_question_title.get("href")

            try:
                with open("kdelo_last.question.txt", encoding="utf-8") as file:
                    question_title_last_kdelo = file.read()
            except:
                question_title_last_kdelo = None

            if kdelo_question_title_text != question_title_last_kdelo:
                text = f"<b>{kdelo_question_title_text}</b>\n\n{self.URL_KDELO}{kdelo_question_title_url}"

                await self.bot.send_message(
                    self.channel_id, text, parse_mode=ParseMode.HTML
                )

                with open("kdelo_last.question.txt", "w", encoding="utf-8") as file:
                    file.write(kdelo_question_title_text)
        except Exception as e:
            print(e)
            print("failed parse kdelo question")
