import requests
from collections import Counter
import matplotlib.pyplot as plt
from map_reduce import map_reduce


def download_text(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def main():
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    try:
        text = download_text(url)
    except requests.RequestException as e:
        print(f"Error while downloading the text: {e}")

    word_counts = map_reduce(text)
    visualize_top_words(word_counts, 10)


def visualize_top_words(word_counts, top_n=10):
    """Візуалізація топ-слів з найвищою частотою."""
    # Вибираємо топ-N слів
    top_words = Counter(word_counts).most_common(top_n)
    words, counts = zip(*top_words)

    # Створення графіка
    plt.barh(words, counts, color="skyblue")
    plt.xlabel("Frequency")
    plt.ylabel("Words")
    plt.title(f"Top {top_n} most frequent words")
    plt.gca().invert_yaxis()
    plt.show()


if __name__ == "__main__":
    main()
