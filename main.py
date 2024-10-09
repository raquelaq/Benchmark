import crawler
import cleaner

def main():

    BOOKS_FOLDER = "gutenberg_books"
    crawler.crawl_books(20)
    all_books = cleaner.process_all_books(BOOKS_FOLDER)
    cleaner.save_books_to_json(all_books, "processed_books.json")


if __name__ == "__main__":
    main()