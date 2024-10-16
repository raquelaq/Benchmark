import json

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
        with open('inverted_index.json', 'w', encoding='utf-8') as file:
            json.dump(inverted_index, file, indent=4)
        
        return inverted_index
    
    # Use another data structure to make the inverted index (
    
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




