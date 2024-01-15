import requests
from bs4 import BeautifulSoup
from time import sleep


URL = "https://glavkniga.ru/"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.3.904 Yowser/2.5 Safari/537.36"}

last_post_id = 0

while True:
    sleep(60)
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    #print("Запрос")
    article = soup.find("table", class_="news_block news_block_margin news_block_has_image")
    title = article.find("a", class_="news_block_hdg")
    url = title.get("href")
    post_id = article.get("data-news_id")
    if post_id != last_post_id:
        print(title.text, "https://glavkniga.ru" + url, post_id)
        last_post_id = post_id

