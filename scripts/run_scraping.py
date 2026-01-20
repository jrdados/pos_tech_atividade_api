import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from lib.scraper import get_all_book_links
from lib.parser import parse_book_page

def run():
    print("Iniciando scraping...")

    links = get_all_book_links()
    print(f"{len(links)} livros encontrados")

    books = []
    for i, link in enumerate(links, start=1):
        print(f"Processando livro {i}/{len(links)}")
        book = parse_book_page(link)
        books.append(book)

    df = pd.DataFrame(books)
    df.to_csv("data/books.csv", index=False)

    print("Scraping finalizado! Arquivo salvo em data/books.csv")

if __name__ == "__main__":
    run()
