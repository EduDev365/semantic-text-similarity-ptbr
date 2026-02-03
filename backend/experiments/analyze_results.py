import pandas as pd
import matplotlib.pyplot as plt

# Caminhos
BASELINE_PATH = "experiments_results/results_baseline.csv"
MULTI_PATH = "experiments_results/results_multilingual.csv"

# Ler arquivos
baseline = pd.read_csv(BASELINE_PATH)
multi = pd.read_csv(MULTI_PATH)

# Converter pra float
baseline["similarity"] = baseline["similarity"].astype(float)
multi["similarity"] = multi["similarity"].astype(float)

# Estatísticas
baseline_mean = baseline["similarity"].mean()
multi_mean = multi["similarity"].mean()

baseline_std = baseline["similarity"].std()
multi_std = multi["similarity"].std()

# Tabela resumo
summary = pd.DataFrame({
    "Modelo": ["Baseline (MiniLM-L6)", "Multilingual (L12)"],
    "Média Similaridade": [baseline_mean, multi_mean],
    "Desvio Padrão": [baseline_std, multi_std]
})

print("\n=== RESUMO DOS RESULTADOS ===\n")
print(summary)

# Salvar tabela
summary.to_csv("experiments_results/summary.csv", index=False)

# Gráfico de barras
plt.figure()
plt.bar(summary["Modelo"], summary["Média Similaridade"])
plt.title("Comparação de Similaridade Média")
plt.ylabel("Similaridade")
plt.xlabel("Modelo")

plt.savefig("experiments_results/comparison_mean.png", dpi=300)
plt.close()

# Histograma
plt.figure()
plt.hist(baseline["similarity"], alpha=0.6, label="Baseline")
plt.hist(multi["similarity"], alpha=0.6, label="Multilingual")

plt.title("Distribuição das Similaridades")
plt.xlabel("Similaridade")
plt.ylabel("Frequência")
plt.legend()

plt.savefig("experiments_results/distribution.png", dpi=300)
plt.close()

print("\nArquivos gerados:")
print("- experiments_results/summary.csv")
print("- experiments_results/comparison_mean.png")
print("- experiments_results/distribution.png")
