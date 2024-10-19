import crawler
import cleaner
import indexer
import query_engine
import json

def main():
    # Define constants
    BOOKS_FOLDER = "gutenberg_books"
    PROCESSED_JSON = "processed_books.json"

    # Step 1: Crawl books
    print("Crawling books...")
    crawler.crawl_books(20)  # Make sure this function works as intended

    # Step 2: Process all books and save to JSON
    print("Processing books...")
    all_books = cleaner.process_all_books(BOOKS_FOLDER)
    cleaner.save_books_to_json(all_books, PROCESSED_JSON)

    # Step 3: Create inverted index with hashmap
    print("Creating inverted index using hashmap...")
    index_hashmap = indexer.create_inverted_index(PROCESSED_JSON, "hashmap")
    
    # Step 4: Create inverted index with trie
    print("Creating inverted index using trie...")
    index_trie = indexer.create_inverted_index(PROCESSED_JSON, "trie")

    # Step 5: Create metadata index
    print("Creating metadata index...")
    metadata_index = indexer.create_metadata_index(PROCESSED_JSON)

    # Step 6: Query the inverted index
    print("Initializing query engine...")
    engine = query_engine.QueryEngine('inverted_index_hashmap.json', 'inverted_index_trie.json', 'metadata_index.json')
    engine.choose_index('hashmap')
    book_ids = engine.query('grasshoppers')
    filtered_books = engine.filter_metadata(book_ids, {"Author": "william shakespeare", "Year": "1994", "Language": "english"})
    print(f'Books that contain the term: {book_ids}')
    print(f'Books that also match the metadata: {filtered_books}')

if __name__ == "__main__":
    main()
