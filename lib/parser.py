import requests
from bs4 import BeautifulSoup
from include.constants import RATING_MAP

def parse_book_page(book_url):
    response = requests.get(book_url)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text.strip()

    price_text = soup.select_one("p.price_color").text
    price = float(
    price_text
    .replace("£", "")
    .replace("Â", "")
    .strip()
)

    rating_class = soup.select_one("p.star-rating")["class"]
    rating = RATING_MAP.get(rating_class[1], None)

    availability_text = soup.select_one("p.availability").text
    availability = availability_text.strip()

    category = soup.select("ul.breadcrumb li a")[-1].text.strip()

    image_rel_url = soup.select_one("div.item.active img")["src"]
    image_url = image_rel_url.replace("../../", "https://books.toscrape.com/")

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "availability": availability,
        "category": category,
        "image_url": image_url,
        "book_url": book_url
    }
