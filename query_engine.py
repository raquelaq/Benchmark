import json

class QueryEngine:
    def __init__(self, index_file):
        with open(index_file, 'r') as file:
            self.inverted_index = json.load(file)

    def query(self, term):
        return self.inverted_index.get(term, [])
