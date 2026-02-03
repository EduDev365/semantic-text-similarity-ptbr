# Backend — Comparador Semântico de Textos (TCC)

Este diretório contém o protótipo funcional do TCC: um sistema que compara semanticamente dois textos usando embeddings (Sentence-Transformers) e calcula a similaridade via cosine similarity.

## Estrutura de pastas

backend/
app/ # Interface Web (Streamlit) + core do sistema
Home.py # Página inicial do app (menu)
core.py # Funções centrais (modelo, similaridade, utilidades)
pages/ # Páginas do Streamlit (Comparar, Histórico, Análises)

cli/ # Versão terminal (CLI)
main.py # Comparador no terminal (salva CSV em data/)

experiments/ # Scripts de experimento/metodologia
batch_test.py
analyze_batch_results.py
analyze_results_v2.py
compare.py
compare_csv.py
compare_multilingual.py
...

data/ # CSVs (dados brutos e históricos)
results_baseline.csv
results_multilingual.csv
results_multilingual_batch.csv
history.csv (se existir — no modo antigo)
...

reports/ # Saídas: gráficos e summaries
boxplot_batch.png
scatter_batch.png
boxplot_categoria.png
summary_batch.csv
boxplot.png
scatter.png
summary_v2.csv
...