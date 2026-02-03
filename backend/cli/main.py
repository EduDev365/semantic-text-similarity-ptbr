import csv
import os
from datetime import datetime
from pathlib import Path

# Esconde logs do HuggingFace/Transformers (limpa o terminal)
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

from transformers.utils import logging
logging.set_verbosity_error()

from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RESULTS_PATH = DATA_DIR / "results_multilingual.csv"


# Carrega uma vez só
model = SentenceTransformer(MODEL_NAME)

def similarity(text_a: str, text_b: str) -> float:
    emb_a = model.encode(text_a, convert_to_tensor=True)
    emb_b = model.encode(text_b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b).item())

def save_result(text_a: str, text_b: str, score: float, path: str = RESULTS_PATH) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = ["timestamp", "model", "text_a", "text_b", "similarity", "percent"]
    row = [now, MODEL_NAME, text_a, text_b, f"{score:.6f}", f"{score*100:.2f}"]

    file_exists = os.path.exists(path)

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

def classify(score: float) -> str:
    # Faixas pro TCC
    if score >= 0.80:
        return "alta"
    if score >= 0.60:
        return "moderada"
    if score >= 0.40:
        return "baixa-moderada"
    return "baixa"

if __name__ == "__main__":
    print("=== Comparador Semântico PT-BR (IA leve) ===")
    a = input("Texto A:\n> ").strip()
    b = input("\nTexto B:\n> ").strip()

    if not a or not b:
        print("\nERRO: preencha os dois textos.")
        raise SystemExit(1)

    score = similarity(a, b)
    nivel = classify(score)

    print("\nResultado:")
    print(f"Modelo: {MODEL_NAME}")
    print(f"Similaridade: {score:.4f}")
    print(f"Percentual: {score*100:.2f}%")
    print(f"Classificação: {nivel}")

    save_result(a, b, score)
    print(f"\n✅ Salvo em {RESULTS_PATH}")
