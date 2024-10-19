import json

class QueryEngine:
    def __init__(self, hashmap_index_file, trie_index_file, metadata_file):
        # Load both inverted indexes and metadata
        with open(hashmap_index_file, 'r') as file:
            self.hashmap_index = json.load(file)
            
        with open(trie_index_file, 'r') as file:
            self.trie_index = json.load(file)
            
        with open(metadata_file, 'r') as file:
            self.metadata_index = json.load(file)

    def choose_index(self, index_type):
        """
        Choose which inverted index to use for the query.
        index_type should be either 'hashmap' or 'trie'.
        """
        if index_type == 'hashmap':
            self.inverted_index = self.hashmap_index
        elif index_type == 'trie':
            self.inverted_index = self.trie_index
        else:
            raise ValueError("index_type should be either 'hashmap' or 'trie'")
    
    def query(self, term):
        """
        Query the chosen inverted index for the given term.
        Returns a list of book IDs or an empty list if the term is not found.
        """
        if not hasattr(self, 'inverted_index'):
            raise ValueError("You need to choose an index first using choose_index()")
            
        return self.inverted_index.get(term, [])

    def filter_metadata(self, book_ids, metadata_filters):
        """
        Filter the book IDs based on loose metadata criteria.
        metadata_filters is a dictionary where values are expected metadata matches (e.g., Title, Author).
        This function tries to match the filters with the keys in the metadata_index.
        
        Example of metadata_filters:
        {
            "Author": "william shakespeare",
            "Year": "1994"
        }
        """
        filtered_ids = set(book_ids)
        
        for _, filter_value in metadata_filters.items():
            # Lowercase the filter value for case-insensitive comparison
            filter_value = filter_value.lower()
            
            # Get the book IDs matching the filter value from the metadata index
            matching_books = set(self.metadata_index.get(filter_value, []))
            
            # Filter the book IDs by intersecting with the current filtered_ids
            filtered_ids &= matching_books
        
        return list(filtered_ids)