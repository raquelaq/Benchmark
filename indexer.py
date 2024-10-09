import json

def create_inverted_index(json_file):
    inverted_index = {}

    # Abrir y leer el archivo JSON
    with open(json_file, 'r', encoding='utf-8') as file:
        books = json.load(file)

    # Recorrer los libros en el JSON
    for book in books:
        ebook_number = extract_ebook_number(book['date'])
        if ebook_number is None:
            continue

        # Recorrer las palabras en el campo 'words' de cada libro
        for word in book['words']:
            word = word.lower()  # Convertir la palabra a minúscula para evitar duplicados por mayúsculas/minúsculas
            if word in inverted_index:
                # Si la palabra ya está en el índice inverso, añadir el ebook_number si no está presente
                if ebook_number not in inverted_index[word]:
                    inverted_index[word].append(ebook_number)
            else:
                # Si la palabra no está en el índice inverso, crear una nueva entrada
                inverted_index[word] = [ebook_number]

    return inverted_index


def extract_ebook_number(date_field):
    # Extraer el número del eBook del campo 'date'
    try:
        # El número del eBook siempre sigue el patrón "eBook #XXX"
        ebook_number = date_field.split('eBook #')[1].split(']')[0]
        return int(ebook_number)
    except (IndexError, ValueError):
        return None




