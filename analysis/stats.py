import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt

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

def plot_price_histogram(df: DataFrame) -> None:
    plt.figure(figsize=(6, 4))
    plt.hist(df['price'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram du prix des livres')
    plt.xlabel('Prix')
    plt.ylabel('Fréquence')
    plt.grid(True, linestyle='dashed', alpha=0.7)

    # Save the histogram to a file
    plt.savefig('../data/histogram_price.png')
    plt.close()


def plot_price_boxplot(df: DataFrame) -> None:
    plt.figure(figsize=(6, 4))
    plt.boxplot(df['price'])
    plt.title('Boxplot du prix des livres')
    plt.ylabel('Prix (£)')
    plt.savefig('../data/boxplot_price.png')
    plt.close()

if __name__ == "__main__":
    books_df = load_books("../data/books.csv")
    print(describe_prices(books_df))
    print("-" * 100)
    print(availability_counts(books_df))
    print("-" * 100)
    print(summary_by_rating(books_df))

    # Generate price histogram
    plot_price_histogram(books_df)
    print("Price histogram saved to '../data/histogram_price.png'")

    plot_price_boxplot(books_df)
    print("Price boxplot saved to '../data/boxplot_price.png'")

