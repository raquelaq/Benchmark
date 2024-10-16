from pymongo import MongoClient
import os
import glob

client = MongoClient('mongodb://localhost:27017/')
db = client['Search_Engine']
collection = db['words']

data_path = "./gutenberg_books/"
files_txt = glob.glob(os.path.join(data_path, "*.txt"))

def get_metadata(content):
    author = ""
    title = ""
    language = ""

    for linea in content.splitlines():
        if linea.startswith("Author:"):
            author = linea.replace("Author:", "").strip()
        elif linea.startswith("Title:"):
            title = linea.replace("Title:", "").strip()
        elif linea.startswith("Language:"):
            language = linea.replace("Language:", "").strip()
        elif "*** START OF THE PROJECT GUTENBERG EBOOK" in linea:
            break

    return author, title, language

def get_book_content(content):
    lines = content.splitlines()
    book_content = []
    start = False

    for line in lines:
        if "*** START OF THE PROJECT GUTENBERG EBOOK" in line:
            start = True
        elif "*** END OF THE PROJECT GUTENBERG EBOOK" in line:
            break

        if start and line:
            book_content.append(line)

    return " ".join(book_content)

for file in files_txt:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        author, titulo, language = get_metadata(content)
        book_content = get_book_content(content)
        words = set(content.split())

        for word in words:
            entry = collection.find_one({"word": word})

            if entry:
                collection.update_one(
                    {"word": word},
                    {"$addToSet": {"books": titulo, "authors": author, "language": language}}
                )
                print("New entry created")
            else:
                new_entry = {
                    "word": word,
                    "books": [titulo],
                    "authors": [author],
                    "language": language
                }
                collection.insert_one(new_entry)

        print("Files processed and inserted into MongoDB. ")