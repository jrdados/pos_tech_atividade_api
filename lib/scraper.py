import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"

def get_all_book_links():
    book_links = []
    next_page = "catalogue/page-1.html"

    while next_page:
        url = BASE_URL + next_page
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.select("article.product_pod h3 a")
        for book in books:
            link = book.get("href")
            full_link = BASE_URL + "catalogue/" + link.replace("../", "")
            book_links.append(full_link)

        next_button = soup.select_one("li.next a")
        if next_button:
            next_page = "catalogue/" + next_button.get("href")
        else:
            next_page = None

    return book_links
