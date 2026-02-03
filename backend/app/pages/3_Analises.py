import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from core import get_paths, reports_available, load_batch

st.set_page_config(page_title="Análises", page_icon="📊", layout="wide")

paths = get_paths()

st.title("📊 Análises")

# =========================================================
# 1) ANÁLISES DO USUÁRIO (SESSÃO)
# =========================================================
st.subheader("Meu uso (sessão)")

hist = st.session_state.get("history", pd.DataFrame())

if hist.empty:
    st.info("Ainda não há comparações nesta sessão. Vá em **Comparar** e faça alguns testes.")
else:
    # garantir tipos numéricos
    if "percent" in hist.columns:
        hist["percent"] = pd.to_numeric(hist["percent"], errors="coerce")
    if "similarity" in hist.columns:
        hist["similarity"] = pd.to_numeric(hist["similarity"], errors="coerce")

    vals = hist["percent"].dropna().astype(float)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Comparações", f"{len(hist)}")
    c2.metric("Média (%)", f"{vals.mean():.2f}%")
    c3.metric("Mínimo (%)", f"{vals.min():.2f}%")
    c4.metric("Máximo (%)", f"{vals.max():.2f}%")

    st.markdown("### Distribuição das similaridades (%) — sessão")

    colh1, colh2, colh3 = st.columns([1, 1, 2])
    with colh1:
        bins = st.slider("Bins (granularidade)", 5, 40, 15)
    with colh2:
        show_mean = st.toggle("Mostrar média", value=True)
    with colh3:
        st.caption("Mais bins = mais detalhe. Com poucas amostras, use menos bins.")

    # Histograma principal
    fig, ax = plt.subplots()
    ax.hist(vals, bins=bins, edgecolor="black")

    ax.set_title("Histograma — Similaridade (%)")
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

    # Histograma por classificação (opcional)
    if "classificacao" in hist.columns and hist["classificacao"].notna().any():
        with st.expander("Ver distribuição por classificação (alta/moderada/etc)"):
            fig2, ax2 = plt.subplots()
            groups = hist.dropna(subset=["percent"]).groupby("classificacao")["percent"]

            for name, series in groups:
                ax2.hist(
                    series.astype(float),
                    bins=bins,
                    alpha=0.5,
                    label=str(name),
                    edgecolor="black",
                )

            ax2.set_title("Histograma por classificação — sessão")
            ax2.set_xlabel("Similaridade (%)")
            ax2.set_ylabel("Frequência")
            ax2.grid(True, axis="y", alpha=0.3)
            ax2.legend()

            st.pyplot(fig2, clear_figure=True)

    with st.expander("Ver tabela da sessão"):
        st.dataframe(hist.sort_values("timestamp", ascending=False), use_container_width=True)

st.divider()

# =========================================================
# 2) ANÁLISES DO PROJETO (TCC): BATCH + GRÁFICOS
# =========================================================
with st.expander("📌 Análises do projeto (TCC): Batch e gráficos", expanded=False):
    st.subheader("Resumo do batch (dataset de testes)")

    df_batch, err = load_batch(paths)
    if err:
        st.warning(err)
    else:
        st.write(f"Linhas: **{len(df_batch)}**")

        if "similaridade_percent" in df_batch.columns:
            df_batch["similaridade_percent"] = pd.to_numeric(df_batch["similaridade_percent"], errors="coerce")

            c1, c2, c3 = st.columns(3)
            c1.metric("Média", f"{df_batch['similaridade_percent'].mean():.2f}%")
            c2.metric("Mínimo", f"{df_batch['similaridade_percent'].min():.2f}%")
            c3.metric("Máximo", f"{df_batch['similaridade_percent'].max():.2f}%")

        with st.expander("Ver tabela do batch"):
            st.dataframe(df_batch, use_container_width=True)

    st.markdown("---")
    st.subheader("Gráficos em reports/")

    available = reports_available(paths)
    if not available:
        st.info("Nenhum gráfico encontrado em reports/. Gere com seus scripts e volte aqui.")
    else:
        for title, path in available.items():
            st.markdown(f"**{title}**")
            st.image(str(path), use_container_width=True)
