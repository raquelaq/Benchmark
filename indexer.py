import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.ebook_numbers = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, ebook_number):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if ebook_number not in node.ebook_numbers:
            node.ebook_numbers.append(ebook_number)

    def to_dict(self):
        """Convert the Trie to dict for exporting to JSON."""
        result = {}
        
        def _to_dict(node, current_word):
            if node.ebook_numbers:
                result[current_word] = node.ebook_numbers
            
            for char, child in node.children.items():
                _to_dict(child, current_word + char)
        
        _to_dict(self.root, "")
        return result

def create_inverted_index(json_file, structure):
    if structure == "hashmap":
        inverted_index = {}

        # Open and read the JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            books = json.load(file)

        # Iterate over each book in the JSON file
        for book in books:
            ebook_number = book['ebook_number']
            if ebook_number is None:
                continue

            # Iterate over each word in the book
            for word in book['words']:
                word = word.lower()  # Convert the word to lowercase
                if word in inverted_index:
                    # If the word is already in the inverted index, add the eBook number to the list
                    if ebook_number not in inverted_index[word]:
                        inverted_index[word].append(ebook_number)
                else:
                    # If the word is not in the inverted index, create a new list with the eBook number
                    inverted_index[word] = [ebook_number]

        # Create the JSON file with the inverted index
        with open('inverted_index_hashmap.json', 'w', encoding='utf-8') as file:
            json.dump(inverted_index, file, indent=4)
        
        return inverted_index

    elif structure == "trie":
        trie = Trie()

        # Open and read the JSON file
        with open(json_file, 'r', encoding='utf-8') as file:
            books = json.load(file)

        # Iterate over each book in the JSON file
        for book in books:
            ebook_number = book['ebook_number']
            if ebook_number is None:
                continue

            # Iterate over each word in the book
            for word in book['words']:
                word = word.lower()  # Convert the word to lowercase
                trie.insert(word, ebook_number)

        # Convert the trie to a dictionary and create the JSON file
        inverted_index = trie.to_dict()
        with open('inverted_index_trie.json', 'w', encoding='utf-8') as file:
            json.dump(inverted_index, file, indent=4)

        return inverted_index

def create_metadata_index(json_file):
    # Create an index for the metadata fields (title, author, release date, language, credits) it can be a normal index
    metadata_index = {}

    # Open and read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        books = json.load(file)

    # Iterate over each book in the JSON file
    for book in books:
        ebook_number = book['ebook_number']
        if ebook_number is None:
            continue

        # Iterate over each metadata field in the book
        for field, value in book.items():
            if field != 'words':
                value = value.lower()
                if value in metadata_index:
                    # If the value is already in the metadata index, add the eBook number to the list
                    if ebook_number not in metadata_index[value]:
                        metadata_index[value].append(ebook_number)
                else:
                    # If the value is not in the metadata index, create a new list with the eBook number
                    metadata_index[value] = [ebook_number]

    # Create the JSON file with the metadata index
    with open('metadata_index.json', 'w', encoding='utf-8') as file:
        json.dump(metadata_index, file, indent=4)

    return metadata_index
