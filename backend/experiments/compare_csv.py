import csv
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def similarity(text_a: str, text_b: str) -> float:
    emb_a = model.encode(text_a, convert_to_tensor=True)
    emb_b = model.encode(text_b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b).item())

def save_result(text_a: str, text_b: str, score: float, path: str = "results.csv") -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = ["timestamp", "text_a", "text_b", "similarity", "percent"]

    row = [now, text_a, text_b, f"{score:.6f}", f"{score*100:.2f}"]

    # cria arquivo com cabeçalho se não existir
    try:
        with open(path, "r", encoding="utf-8") as _:
            file_exists = True
    except FileNotFoundError:
        file_exists = False

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

if __name__ == "__main__":
    print("=== Comparador Semântico (IA leve) + Histórico CSV ===")

    a = input("Cole o TEXTO A:\n> ").strip()
    b = input("\nCole o TEXTO B:\n> ").strip()

    if not a or not b:
        print("ERRO: preencha os dois textos.")
        raise SystemExit(1)

    score = similarity(a, b)

    print("\nResultado:")
    print(f"Similaridade: {score:.4f}")
    print(f"Percentual: {score*100:.2f}%")

    save_result(a, b, score)
    print("\n✅ Salvo em results.csv (na pasta backend)")
