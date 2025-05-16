import pandas
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

def load_books(file_path: str) -> DataFrame:
    return pandas.read_csv(file_path)


def load_webcams(file_path: str) -> DataFrame:
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

def plot_price_histogram(df: DataFrame, out: str) -> None:
    plt.figure(figsize=(6, 4))
    plt.hist(df['price'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram du prix')
    plt.xlabel('Prix')
    plt.ylabel('Fréquence')
    plt.grid(True, linestyle='dashed', alpha=0.7)

    # Save the histogram to a file
    plt.savefig(out)
    plt.close()


def plot_price_boxplot(df: DataFrame, out: str, product_title: str) -> None:
    plt.figure(figsize=(6, 4))
    plt.boxplot(df['price'])
    plt.title(f'Boxplot du prix des {product_title}')
    plt.ylabel('Prix')
    plt.savefig(out)
    plt.close()

def plot_price_cluster(df: DataFrame) -> None:
    """scatter plot index/prix coloré par cluster."""
    prices = df['price'].values

    # Define price thresholds for clusters
    low_threshold = 20
    high_threshold = 40

    # Create cluster assignments
    clusters = np.zeros(len(prices))
    clusters[prices > low_threshold] = 1
    clusters[prices > high_threshold] = 2

    # Create a scatter plot
    plt.figure(figsize=(10, 6))

    # Plot each cluster with different colors
    colors = ['green', 'blue', 'red']
    labels = ['Prix Bas', 'Prix Moyen', 'Prix Elevé']

    for i in range(len(labels)):
        mask = clusters == i
        plt.scatter(np.asarray(mask).nonzero()[0], prices[mask],
                    c=colors[i], label=labels[i], alpha=0.6)

    plt.title('Scatter Plot des Prix par Cluster')
    plt.xlabel('Index')
    plt.ylabel('Prix (£)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)

    # Save the plot
    plt.savefig('../data/clustering_price.png')
    plt.close()

def plot_cluster_distribution(df: DataFrame) -> None:
    """boxplot des prix par cluster."""
    # todo: faire un boxplot par cluster

if __name__ == "__main__":
    books_df = load_books("../data/books.csv")
    webcams_df = load_webcams("../data/webcams.csv")

    # Generate price histogram
    plot_price_histogram(books_df, "../data/book_histogram_price.png")
    plot_price_histogram(webcams_df, "../data/webcam_histogram_price.png")

    plot_price_boxplot(books_df, "../data/book_boxplot_price.png", "livres")
    plot_price_boxplot(webcams_df, "../data/webcam_boxplot_price.png", "webcams")

    plot_price_cluster(books_df)

    plot_cluster_distribution(books_df)
