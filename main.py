from scraper.exporter import export_books_to_csv, export_webcam_to_csv
from scraper.scraper_books import scrape_all as scrape_all_book
from scraper.scraper_custom import scrap_all as scrape_all_webcam


URL = "https://books.toscrape.com/catalogue/page-{page_number}.html"

books = scrape_all_book(URL, 50)

export_books_to_csv(books, "./data/books.csv")

print(f"Nombre de livres scrapés: {len(books)}")

webcams = scrape_all_webcam()

export_webcam_to_csv(webcams, "./data/webcams.csv")

print(f"Nombre de webcams scrapés: {len(webcams)}")