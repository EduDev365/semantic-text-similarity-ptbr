from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def main():
    BASE_DIR = Path(__file__).resolve().parents[1]
    DATA_DIR = BASE_DIR / "data"
    REPORTS_DIR = BASE_DIR / "reports"
    REPORTS_DIR.mkdir(exist_ok=True)

    batch_path = DATA_DIR / "results_multilingual_batch.csv"
    df = pd.read_csv(batch_path)
    df["similaridade_percent"] = df["similaridade_percent"].astype(float)

    # resumo
    summary = df["similaridade_percent"].describe()
    print("\n=== RESUMO GERAL (BATCH) ===\n")
    print(summary)
    summary.to_csv(REPORTS_DIR / "summary_batch.csv")

    # boxplot geral
    plt.figure()
    plt.boxplot(df["similaridade_percent"])
    plt.title("Distribuição das Similaridades (Batch)")
    plt.ylabel("Similaridade (%)")
    plt.savefig(REPORTS_DIR / "boxplot_batch.png", dpi=300)
    plt.close()

    # boxplot por categoria
    plt.figure()
    categories = list(df["categoria"].unique())
    data = [df[df["categoria"] == c]["similaridade_percent"] for c in categories]

    # Matplotlib 3.9+: usar tick_labels (evita warning)
    plt.boxplot(data, tick_labels=categories)

    plt.title("Distribuição por Categoria (Batch)")
    plt.ylabel("Similaridade (%)")
    plt.savefig(REPORTS_DIR / "boxplot_categoria.png", dpi=300)
    plt.close()

    # scatter
    plt.figure()
    plt.scatter(range(len(df)), df["similaridade_percent"])
    plt.axhline(80, linestyle="--", label="Alta Similaridade")
    plt.title("Resultados Individuais (Batch)")
    plt.xlabel("Execução")
    plt.ylabel("Similaridade (%)")
    plt.legend()
    plt.savefig(REPORTS_DIR / "scatter_batch.png", dpi=300)
    plt.close()

    print("\nArquivos gerados em reports/:")
    print("- summary_batch.csv")
    print("- boxplot_batch.png")
    print("- boxplot_categoria.png")
    print("- scatter_batch.png")

if __name__ == "__main__":
    main()
