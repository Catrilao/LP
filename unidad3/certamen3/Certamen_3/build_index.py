import os
import re
from collections import defaultdict

DATASET_PATH = "dataset"

index = defaultdict(set)

for filename in os.listdir(DATASET_PATH):

    if filename.endswith(".txt"):
        filepath = os.path.join(DATASET_PATH, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read().lower()

        text = re.sub(r"[.,:;()\"'?¡¿!]", " ", text)

        for word in text.split():
            index[word].add(filename)

with open("index.txt", "w", encoding="utf-8") as out:
    for word, docs in index.items():
        out.write(f"{word} {' '.join(docs)}\n")

print("Index generado correctamente .")
