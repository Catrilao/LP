import sys


def load_stopwords(path):
    """Carga stopwords desde archivo."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return set(f.read().split())
    except:
        print("⚠️ Advertencia: No se encontró stopwords.txt")
        return set()


def load_index(path):
    """Carga index.txt en memoria como diccionario palabra → set(documentos)"""
    index = {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    palabra = parts[0]
                    documentos = set(parts[1:])
                    index[palabra] = documentos
    except:
        print(" Error: No se encontró index.txt. Genéralo primero con AWK.")
        sys.exit(1)

    return index



def remove_stopwords_recursive(words, stopwords):
    """Elimina stopwords de la consulta usando recursividad."""
    if not words:
        return []

    head, tail = words[0], words[1:]

    if head in stopwords:
        print(f" → Stopword removida: {head}")
        return remove_stopwords_recursive(tail, stopwords)

    return [head] + remove_stopwords_recursive(tail, stopwords)



def intersect_recursive(posting_lists):
    """Devuelve intersección recursiva entre sets de documentos."""
    if not posting_lists:
        return set()

    if len(posting_lists) == 1:
        return posting_lists[0]

    return posting_lists[0].intersection(
        intersect_recursive(posting_lists[1:])
    )


def main():

    stopwords = load_stopwords('stopwords.txt')
    inv_index = load_index('index.txt')

    print(f" Índice cargado correctamente.")
    print(f"   → {len(inv_index)} palabras únicas indexadas.")

    while True:
        try:
            q = input("\nBuscar (escribe palabras, o 'exit' para salir): ").lower().strip()

            if q == "exit":
                print(" Saliendo del buscador...")
                break

            query_terms = q.split()

            # Limpieza recursiva de stopwords
            clean_query = remove_stopwords_recursive(query_terms, stopwords)

            if not clean_query:
                print(" Consulta vacía (solo stopwords eliminadas). Intenta otra.")
                continue

            print(f" Buscando términos: {clean_query}")

            # Obtener listas de documentos para cada palabra
            posting_lists = []
            unknown = False

            for w in clean_query:
                if w not in inv_index:
                    print(f" La palabra '{w}' no existe en ningún documento.")
                    unknown = True
                else:
                    posting_lists.append(inv_index[w])

            if unknown or not posting_lists:
                print(" Resultado: Ningún documento coincide.")
                continue

            # Intersección recursiva
            results = intersect_recursive(posting_lists)

            if results:
                print(f" Resultados ({len(results)} documentos): {results}")
            else:
                print(" Resultado: Ningún documento contiene todas las palabras.")

        except (KeyboardInterrupt, EOFError):
            print("\n Saliendo del buscador...")
            break

if __name__ == "__main__":
    main()
