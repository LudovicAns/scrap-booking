import pandas
from pandas import DataFrame


def load_books(file_path: str) -> DataFrame:
    return pandas.read_csv(file_path)

if __name__ == "__main__":
    books = load_books("../data/books.csv")
    print(books)