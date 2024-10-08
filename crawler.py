import os
import requests
from bs4 import BeautifulSoup
import time

# Constants
BASE_URL = "https://www.gutenberg.org"
BOOKS_URL = f"{BASE_URL}/browse/scores/top"
DOWNLOAD_FOLDER = "gutenberg_books"

# Create download folder if it doesn't exist
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def get_book_links():
    """Fetches the links to the top books on Project Gutenberg."""
    response = requests.get(BOOKS_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all book links
    book_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/ebooks/'):
            book_links.append(f"{BASE_URL}{href}")
    
    return book_links

def download_book(book_id):
    """Download the .txt version of the book, or fall back to .html, .epub, or .mobi if not available."""
    formats = {
        'txt': f"https://gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt",
        'html': f"https://gutenberg.org/cache/epub/{book_id}/pg{book_id}.html",
        'epub': f"https://gutenberg.org/cache/epub/{book_id}/pg{book_id}.epub",
        'mobi': f"https://gutenberg.org/cache/epub/{book_id}/pg{book_id}.mobi"
    }

    # Try each format
    for format, url in formats.items():
        print(f"Attempting to download book {book_id} from {url}")
        response = requests.get(url)
        if response.status_code == 200:
            # Save the file in the corresponding format
            book_path = os.path.join(DOWNLOAD_FOLDER, f"{book_id}.{format}")
            with open(book_path, 'wb') as f:  # 'wb' for binary formats
                f.write(response.content)
            print(f"Downloaded book {book_id} in {format} format.")
            return  # Exit the function once a format is successfully downloaded
    
    print(f"Book {book_id} is not available in any of the supported formats.")

def crawl_books(num_books):
    """Crawls through the Project Gutenberg top books and downloads a specified number of them."""
    book_links = get_book_links()
    book_ids = [link.split('/')[-1] for link in book_links]

    for i, book_id in enumerate(book_ids):
        if i >= num_books:
            break
        download_book(book_id)
        time.sleep(1)