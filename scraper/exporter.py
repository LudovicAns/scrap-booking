from scraper.book import Book
import csv


def export_books_to_csv(books: list[Book], file_path: str) -> None:
    """
    Exports a list of Book objects to a CSV file.

    This function takes a list of Book objects and writes their data to a CSV file
    at the specified path. Each row in the CSV represents a book, with columns
    corresponding to the book's attributes (title, price, price_type, availability, rating).

    :param books: A list of Book objects to export
    :type books: list[Book]
    :param file_path: The path where the CSV file will be created or overwritten
    :type file_path: str
    :return: None
    """
    if not books:
        return

    # Get the field names from the first book's dictionary
    fieldnames = books[0].to_dict().keys()

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write a row for each book
        for book in books:
            writer.writerow(book.to_dict())
