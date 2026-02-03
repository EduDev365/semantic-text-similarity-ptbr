from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def main():
    BASE_DIR = Path(__file__).resolve().parents[1]
    DATA_DIR = BASE_DIR / "data"
    REPORTS_DIR = BASE_DIR / "reports"
    REPORTS_DIR.mkdir(exist_ok=True)

    BASELINE_PATH = DATA_DIR / "results_baseline.csv"
    MULTI_PATH = DATA_DIR / "results_multilingual.csv"

    baseline = pd.read_csv(BASELINE_PATH)
    multi = pd.read_csv(MULTI_PATH)

    baseline["similarity"] = baseline["similarity"].astype(float)
    multi["similarity"] = multi["similarity"].astype(float)

    summary = pd.DataFrame({
        "Modelo": ["Baseline", "Multilingual"],
        "Média": [baseline["similarity"].mean(), multi["similarity"].mean()],
        "Desvio": [baseline["similarity"].std(), multi["similarity"].std()],
        "Mínimo": [baseline["similarity"].min(), multi["similarity"].min()],
        "Máximo": [baseline["similarity"].max(), multi["similarity"].max()],
    })

    print("\n=== RESUMO (Baseline vs Multilingual) ===\n")
    print(summary)

    summary.to_csv(REPORTS_DIR / "summary_v2.csv", index=False)

    # boxplot
    plt.figure()
    plt.boxplot(
        [baseline["similarity"], multi["similarity"]],
        tick_labels=["Baseline", "Multilingual"]
    )
    plt.title("Distribuição das Similaridades (Boxplot)")
    plt.ylabel("Similaridade")
    plt.savefig(REPORTS_DIR / "boxplot.png", dpi=300)
    plt.close()

    # scatter
    plt.figure()
    plt.scatter(range(len(baseline)), baseline["similarity"], label="Baseline")
    plt.scatter(range(len(multi)), multi["similarity"], label="Multilingual")
    plt.axhline(0.8, linestyle="--", label="Alta Similaridade")

    plt.title("Resultados Individuais por Teste")
    plt.xlabel("Execução")
    plt.ylabel("Similaridade")
    plt.legend()

    plt.savefig(REPORTS_DIR / "scatter.png", dpi=300)
    plt.close()

    print("\nArquivos gerados em reports/:")
    print("- summary_v2.csv")
    print("- boxplot.png")
    print("- scatter.png")

if __name__ == "__main__":
    main()
