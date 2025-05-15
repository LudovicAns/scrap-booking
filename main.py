from scraper.exporter import export_books_to_csv
from scraper.scraper_books import scrape_all


URL = "https://books.toscrape.com/catalogue/page-{page_number}.html"

books = scrape_all(URL, 50)

export_books_to_csv(books, "./data/books.csv")

print(f"Nombre de livres scrapés: {len(books)}")