import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from core import get_paths, reports_available, load_batch

st.set_page_config(page_title="Avaliação (TCC)", page_icon="🎓", layout="wide")

paths = get_paths()

st.title("🎓 Avaliação Experimental (TCC)")
st.caption("Resultados dos testes e justificativa da escolha do modelo final.")

# =========================================================
# 0) CONTEXTO
# =========================================================
st.markdown(
    """
### Contexto

Esta página apresenta os resultados experimentais utilizados no Trabalho de Conclusão de Curso.

Aqui estão reunidos:
- os testes realizados com dataset (batch);
- os gráficos gerados durante os experimentos;
- a base para a escolha do modelo final.

O objetivo é permitir a verificação direta dos dados utilizados na validação do sistema.

**Modelo final adotado:** `paraphrase-multilingual-MiniLM-L12-v2`
"""
)

st.divider()

# =========================================================
# 1) BATCH (DATASET DE TESTE)
# =========================================================
st.subheader("1) Resultados do batch (dataset de testes)")

df_batch, err = load_batch(paths)
if err:
    st.warning(err)
    st.stop()

st.write(f"Linhas no batch: **{len(df_batch)}**")

# Coluna percentual
percent_col_candidates = [
    "similaridade_percent",
    "percent",
    "percentual",
    "similarity_percent",
]

percent_col = next(
    (c for c in percent_col_candidates if c in df_batch.columns),
    None,
)

if percent_col is None:
    st.warning(
        "Coluna de percentual não encontrada no batch "
        "(esperado: similaridade_percent)."
    )
else:
    df_batch[percent_col] = pd.to_numeric(
        df_batch[percent_col],
        errors="coerce",
    )

    vals = df_batch[percent_col].dropna().astype(float)

    # Métricas
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Amostras válidas", f"{len(vals)}")
    c2.metric("Média", f"{vals.mean():.2f}%")
    c3.metric("Mínimo", f"{vals.min():.2f}%")
    c4.metric("Máximo", f"{vals.max():.2f}%")

    st.markdown("#### Distribuição dos resultados")

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        bins = st.slider("Bins", 5, 50, 20)

    with col2:
        show_mean = st.toggle("Mostrar média", value=True)

    with col3:
        st.caption(
            "Para conjuntos pequenos, menos bins tendem a gerar melhor visualização."
        )

    # Histograma
    fig, ax = plt.subplots()

    ax.hist(vals, bins=bins, edgecolor="black")

    ax.set_title("Histograma — Similaridade (%) no batch")
    ax.set_xlabel("Similaridade (%)")
    ax.set_ylabel("Frequência")
    ax.grid(True, axis="y", alpha=0.3)

    if show_mean:
        mean_val = vals.mean()

        ax.axvline(mean_val, linestyle="--", linewidth=2)

        ax.text(
            mean_val,
            ax.get_ylim()[1] * 0.95,
            f" média={mean_val:.1f}%",
            rotation=90,
            va="top",
        )

    st.pyplot(fig, clear_figure=True)

# Tabela
with st.expander("Ver tabela completa do batch"):
    st.dataframe(df_batch, use_container_width=True)

    csv_bytes = df_batch.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Baixar CSV do batch",
        data=csv_bytes,
        file_name="batch_resultados.csv",
        mime="text/csv",
    )

st.divider()

# =========================================================
# 2) GRÁFICOS EM reports/
# =========================================================
st.subheader("2) Gráficos gerados nos experimentos")

st.markdown(
    """
A seguir são exibidas as figuras geradas durante os testes e armazenadas na pasta `reports/`.
Esses gráficos são utilizados como referência no capítulo de Resultados e Discussão do TCC.
"""
)

available = reports_available(paths)

if not available:
    st.info("Nenhuma imagem encontrada na pasta reports/.")
else:
    titles = list(available.keys())

    selected = st.multiselect(
        "Selecionar gráficos",
        options=titles,
        default=titles,
    )

    for title in selected:
        img_path = available[title]

        st.markdown(f"### {title}")

        st.image(str(img_path), use_container_width=True)

        st.caption(
            f"Figura — {title}. Resultado obtido durante os testes experimentais "
            "do sistema, utilizado na validação do modelo para textos em PT-BR."
        )

st.divider()

# =========================================================
# 3) RESUMO FINAL
# =========================================================
st.subheader("3) Resumo da decisão")

st.markdown(
    """
Com base nos resultados obtidos nos testes com batch e na análise dos gráficos,
foi adotado o modelo **paraphrase-multilingual-MiniLM-L12-v2** como versão final.

Esse modelo apresentou maior consistência na identificação de similaridade semântica
em textos em português, atendendo aos requisitos definidos para o projeto.
"""
)
