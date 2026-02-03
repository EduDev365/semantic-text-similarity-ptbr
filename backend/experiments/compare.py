from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def similarity(text_a: str, text_b: str) -> float:
    emb_a = model.encode(text_a, convert_to_tensor=True)
    emb_b = model.encode(text_b, convert_to_tensor=True)
    return float(util.cos_sim(emb_a, emb_b).item())

if __name__ == "__main__":
    print("=== Comparador Semântico (IA leve) ===")

    a = input("Cole o TEXTO A:\n> ").strip()
    b = input("\nCole o TEXTO B:\n> ").strip()

    if not a or not b:
        print("Erro: textos vazios.")
        exit(1)

    score = similarity(a, b)

    print("\nResultado:")
    print(f"Similaridade: {score:.4f}")
    print(f"Percentual: {score*100:.2f}%")
