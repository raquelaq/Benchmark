import crawler
import cleaner
import indexer
import query_engine
import json

def main():

    BOOKS_FOLDER = "gutenberg_books"
    #crawler.crawl_books(20)
    #all_books = cleaner.process_all_books(BOOKS_FOLDER)
    #cleaner.save_books_to_json(all_books, "processed_books.json")
    #index = indexer.create_inverted_index("processed_books.json", "hashmap")
    #metadata_index = indexer.create_metadata_index("processed_books.json")

    # Query the inverted index
    engine = query_engine.QueryEngine('inverted_index.json')
    term = "grasshopper"
    results = engine.query(term)
    print(f"Results for the term '{term}':")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()