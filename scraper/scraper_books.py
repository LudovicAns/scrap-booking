import bs4.element
import requests
from bs4 import BeautifulSoup

from scraper.book import Book


def __get_price_and_price_type(html_element: bs4.element.Tag) -> (float, str):
    if not html_element.text.strip()[0].isdigit():
        i = 1
        while not html_element.text.strip()[i].isdigit():
            i += 1
        return float(html_element.text.strip()[i:]), html_element.text.strip()[0:i]
    else:
        i = -1
        while not html_element.text.strip()[i].isdigit():
            i -= 1
        return float(html_element.text.strip()[:i]), html_element.text.strip()[i:-1]

def __convert_str_rating(rating_str: str) -> int:
    rating_dict = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return rating_dict[rating_str]

def scrape_page(url: str) -> list[Book]:
    """
    Scrape a webpage to extract information about books formatted in a specific structure.

    This function fetches the HTML content of a webpage and parses it using BeautifulSoup
    to extract details about books. The returned book data includes attributes such as the
    title, price, price type, availability, and rating.

    :param url: The URL of the webpage to scrape.
    :type url: str
    :return: A list of `Book` objects containing details of the books extracted from the webpage.
    :rtype: list[Book]
    :raises Exception: If the HTTP response code from the requested `url` is not 200.
    """
    response = requests.get(url)

    if not response.status_code == 200:
        raise Exception(f"La réponse n'est pas valide. Code de statut : {response.status_code}")

    html = response.text

    soup = BeautifulSoup(html, "html.parser")

    books_html = soup.find_all("article", class_="product_pod")


    books = []
    for book_html in books_html:
        price_def = __get_price_and_price_type(book_html.find("p", class_="price_color"))
        books.append(Book(
            book_html.h3.a["title"],
            price_def[0],
            price_def[1],
            book_html.find("p", class_="instock availability").text.strip().lower() == "in stock",
            __convert_str_rating(book_html.find("p", class_="star-rating")["class"][1].strip())
        ))
    return books

def scrape_all(url: str, pages: int=50) -> list[Book]:
    """
    Scrapes multiple pages of a website to extract book information by calling the
    `scrape_page` function. If a page does not return the expected status code,
    the process halts, and the collected data up until that point is returned.

    :param url: The base URL of the website where the pages are located. The URL
        should include a placeholder for the page number (e.g., `{page_number}`).
    :param pages: The number of pages to scrape. Defaults to 50.
    :return: A list of `Book` objects containing extracted data from the scraped
        pages.
    """
    books = []
    for page_number in range(1, pages+1):
        try:
            books.extend(scrape_page(url.format(page_number=page_number)))
        except Exception as e:
            print(f"Fin du scrapping car une page n'a pas retourné le bon code de statut : {e}")
            break
    return books

if __name__ == "__main__":
    books = scrape_all("https://books.toscrape.com/catalogue/page-{page_number}.html", 10)
    for book in books:
        print(book)