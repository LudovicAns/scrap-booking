import pandas
from pandas import DataFrame


def load_books(file_path: str) -> DataFrame:
    return pandas.read_csv(file_path)

def describe_prices(df: DataFrame) -> None:
    print(
        df.groupby("price_type")["price"].describe()
    )

def availability_counts(df: DataFrame) -> None:
    print(
        df.groupby(["availability", "rating"])["availability"].count()
        .unstack(fill_value=0)
        .reset_index()
        .set_index("availability")
    )

def summary_by_rating(df: DataFrame) -> None:
    print(
        df.groupby(["rating", "price_type"])["price"].mean().reset_index().set_index("rating")
    )

if __name__ == "__main__":
    books_df = load_books("../data/books.csv")
    print(describe_prices(books_df))
    print("-" * 100)
    print(availability_counts(books_df))
    print("-" * 100)
    print(summary_by_rating(books_df))