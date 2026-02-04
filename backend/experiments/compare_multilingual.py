import csv
from datetime import datetime
from transformers.utils import logging
logging.set_verbosity_error()
from sentence_transformers import SentenceTransformer, util


# Modelo melhor para o PT-BR
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def similarity(text_a: str, text_b: str) -> float:
    emb_a = model.encode(text_a, convert_to_tensor=True)
    emb_b = model.encode(text_b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b).item())

def save_result(text_a, text_b, score, path="results_multilingual.csv"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = ["timestamp", "text_a", "text_b", "similarity", "percent"]

    row = [now, text_a, text_b, f"{score:.6f}", f"{score*100:.2f}"]

    try:
        with open(path, "r", encoding="utf-8"):
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

if __name__ == "__main__":
    print("=== Comparador Semântico PT-BR ===")

    a = input("Texto A:\n> ").strip()
    b = input("\nTexto B:\n> ").strip()

    if not a or not b:
        print("Erro: textos vazios.")
        exit(1)

    score = similarity(a, b)

    print("\nResultado:")
    print(f"Similaridade: {score:.4f}")
    print(f"Percentual: {score*100:.2f}%")

    save_result(a, b, score)

    print("✅ Salvo em results_multilingual.csv")
