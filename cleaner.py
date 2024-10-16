import os
import re
import json
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Constants
OUTPUT_JSON = "processed_books.json"
STOPWORDS = set(stopwords.words('english'))  # Stopwords set to filter useless words

class Book:
    def __init__(self, title, author, date, language, credits, words, ebook_number):
        self.title = title
        self.author = author
        self.date = date
        self.language = language
        self.credits = credits
        self.words = words
        self.ebook_number = ebook_number

    def to_dict(self):
        """Converts the Book object to a dictionary for JSON serialization."""
        return {
            'title': self.title,
            'author': self.author,
            'date': self.date,
            'language': self.language,
            'credits': self.credits,
            'ebook_number': self.ebook_number,
            'words': list(self.words)  # Convert set to list for JSON serialization
        }

def clean_text(text):
    """Remove stopwords, punctuation, underscores, and return a list of unique important words."""
    # Remove punctuation and split the text into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Remove underscores from the beginning, end, and middle of each word
    words = [word.replace('_', '') for word in words]
    
    # Filter out stopwords and words with length <= 2 (to exclude overly short words)
    meaningful_words = {word for word in words if word not in STOPWORDS and len(word) > 2}
    
    return meaningful_words  # Return unique words as a set



def extract_metadata(book_content):
    """Extracts the metadata (title, author, release date, language, credits) from the book content."""
    title = re.search(r'Title:\s*(.+)', book_content)
    author = re.search(r'Author:\s*(.+)', book_content)
    date = re.search(r'Release date:\s*(.+)', book_content)
    language = re.search(r'Language:\s*(.+)', book_content)
    credits = re.search(r'Credits:\s*(.+)', book_content)
    ebook_number = re.search(r'eBook (#\d+)', book_content)
    year = re.search(r'(\d{4})', date.group(1))

    return {
        'title': title.group(1).strip() if title else 'Unknown Title',
        'author': author.group(1).strip() if author else 'Unknown Author',
        'date': year.group(1).strip() if year else 'Unknown Date',
        'language': language.group(1).strip() if language else 'Unknown Language',
        'credits': credits.group(1).strip() if credits else 'Unknown Credits',
        'ebook_number': ebook_number.group(1).strip() if ebook_number else 'Unknown eBook Number'
    }

def process_book(filepath):
    """Processes a single book file to extract metadata and create a Book object."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from the book content
    metadata = extract_metadata(content)
    
    # Clean the text to remove stopwords and get important words
    start_of_book = re.search(r'\*\*\* START OF (THE|THIS) PROJECT GUTENBERG EBOOK', content)
    if start_of_book:
        content = content[start_of_book.end():]  # Remove header, start at the book's actual content
    
    words = clean_text(content)
    
    # Create a Book object
    book = Book(
        title=metadata['title'],
        author=metadata['author'],
        date=metadata['date'],
        language=metadata['language'],
        credits=metadata['credits'],
        ebook_number=metadata['ebook_number'],
        words=words
    )
    
    return book

def process_all_books(folder):
    """Processes all books in the given folder and returns a list of Book objects."""
    books = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath) and filename.endswith(('.txt', '.html')):
            print(f"Processing {filename}")
            book = process_book(filepath)
            books.append(book)
    
    return books


def save_books_to_json(books, output_file):
    """Saves the list of Book objects to a JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([book.to_dict() for book in books], f, ensure_ascii=False, indent=4)
    print(f"Saved {len(books)} books to {output_file}")
