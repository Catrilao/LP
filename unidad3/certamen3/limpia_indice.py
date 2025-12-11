def limpiar_indice():
    # Leer stopwords
    with open("stopwords.txt", "r", encoding="utf-8") as archivo:
        stopwords = {line.strip() for line in archivo}

    # Leer índice
    with open("index.txt", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    nuevas_lineas = []
    for linea in lineas:
        parts = linea.strip().split()
        if not parts:
            continue

        palabra = parts[0]
        docs = parts[1:]

        if palabra in stopwords:
            print(f"Stopword eliminada del índice: {palabra}")
            continue

        nuevas_lineas.append(palabra + " " + " ".join(docs) + "\n")

    with open("index.txt", "w", encoding="utf-8") as f:
        f.writelines(nuevas_lineas)

    print("Índice limpio de stopwords.")


limpiar_indice()
