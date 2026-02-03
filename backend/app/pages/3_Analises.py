import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Análises", page_icon="📊", layout="wide")

st.title("📊 Análises")
st.caption("Estatísticas e gráficos do seu uso na sessão atual (dados em memória).")

# =========================================================
# 1) ANÁLISES DO USUÁRIO (SESSÃO)
# =========================================================
st.subheader("Meu uso (sessão)")

hist = st.session_state.get("history", pd.DataFrame())

if hist.empty:
    st.info("Ainda não há comparações nesta sessão. Vá em **Comparar** e faça alguns testes.")
else:
    hist = hist.copy()

    # =========================
    # Normalização de tipos
    # =========================
    if "percent" in hist.columns:
        # aceita vírgula como decimal: "-12,3" -> "-12.3"
        hist["percent"] = (
            hist["percent"]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        hist["percent"] = pd.to_numeric(hist["percent"], errors="coerce")

    if "similarity" in hist.columns:
        hist["similarity"] = (
            hist["similarity"]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )
        hist["similarity"] = pd.to_numeric(hist["similarity"], errors="coerce")

    if "percent" not in hist.columns or hist["percent"].dropna().empty:
        st.warning("Não encontrei valores numéricos em `percent` para gerar estatísticas/gráficos.")
        st.stop()

    vals = hist["percent"].dropna().astype(float)

    # =========================
    # KPIs
    # =========================
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Comparações", f"{len(hist)}")
    c2.metric("Média (%)", f"{vals.mean():.2f}%")
    c3.metric("Mínimo (%)", f"{vals.min():.2f}%")
    c4.metric("Máximo (%)", f"{vals.max():.2f}%")

    # =========================================================
    # RESUMO POR CLASSIFICAÇÃO (mini visão geral)
    # =========================================================
    has_class = ("classificacao" in hist.columns) and hist["classificacao"].notna().any()
    if has_class:
        st.markdown("### Resumo por classificação")

        counts = hist["classificacao"].fillna("Sem classificação").value_counts()
        total = int(counts.sum()) if len(counts) else 0

        # tenta ordenar em um padrão "bonito"
        desired_order = ["Alta", "Moderada", "Baixa-mod.", "Baixa", "Sem classificação"]
        ordered_index = [c for c in desired_order if c in counts.index] + [c for c in counts.index if c not in desired_order]
        counts = counts.reindex(ordered_index)

        summary_df = pd.DataFrame({
            "Classificação": counts.index,
            "Qtde": counts.values,
            "%": [round((v / total) * 100, 1) if total else 0 for v in counts.values]
        })

        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # =========================================================
    # A) HISTOGRAMA
    # =========================================================
    st.markdown("### Distribuição das similaridades (%) — sessão")

    colh1, colh2, colh3, colh4 = st.columns([1, 1, 1, 2])
    with colh1:
        bins = st.slider("Bins (granularidade)", 5, 40, 15)
    with colh2:
        show_mean = st.toggle("Mostrar média", value=True)
    with colh3:
        fixed_range = st.toggle("Fixar range (-100..100)", value=True)
    with colh4:
        st.caption(
            "Valores podem ser negativos porque cosine similarity varia de -1 a 1 (convertido para -100 a 100). "
            "Fixar range ajuda a enxergar os negativos quando há muitos valores altos."
        )

    fig, ax = plt.subplots()

    if fixed_range:
        ax.hist(vals, bins=bins, edgecolor="black", range=(-100, 100))
        ax.set_xlim(-100, 100)
    else:
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
    if has_class:
        with st.expander("Ver distribuição por classificação (alta/moderada/etc)"):
            fig2, ax2 = plt.subplots()

            groups = (
                hist.dropna(subset=["percent"])
                .groupby("classificacao")["percent"]
            )

            for name, series in groups:
                series = series.dropna().astype(float)
                if series.empty:
                    continue

                if fixed_range:
                    ax2.hist(
                        series,
                        bins=bins,
                        alpha=0.5,
                        label=str(name),
                        edgecolor="black",
                        range=(-100, 100),
                    )
                    ax2.set_xlim(-100, 100)
                else:
                    ax2.hist(
                        series,
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

    st.divider()

    # =========================================================
    # B) EVOLUÇÃO AO LONGO DA SESSÃO
    # =========================================================
    st.markdown("### Evolução ao longo da sessão")

    tmp = hist.dropna(subset=["percent"]).copy()
    tmp["percent"] = tmp["percent"].astype(float)

    x_label = "Ordem dos testes"
    x = None

    if "timestamp" in tmp.columns and tmp["timestamp"].notna().any():
        tmp["timestamp_dt"] = pd.to_datetime(tmp["timestamp"], errors="coerce")
        if tmp["timestamp_dt"].notna().any():
            tmp = tmp.sort_values("timestamp_dt")
            x = tmp["timestamp_dt"]
            x_label = "Tempo"

    if x is None:
        tmp = tmp.reset_index(drop=True)
        x = tmp.index

    fig_t, ax_t = plt.subplots()
    ax_t.plot(x, tmp["percent"], marker="o", linewidth=2)

    ax_t.set_title("Similaridade (%) ao longo da sessão")
    ax_t.set_xlabel(x_label)
    ax_t.set_ylabel("Similaridade (%)")

    if fixed_range:
        ax_t.set_ylim(-100, 100)

    ax_t.grid(True, axis="y", alpha=0.3)
    st.pyplot(fig_t, clear_figure=True)

    st.divider()

    # =========================================================
    # C) DESTAQUES (Top 5 melhores e piores)
    # =========================================================
    st.markdown("### Destaques da sessão")

    cA, cB = st.columns(2)

    cols_priority = [c for c in ["timestamp", "classificacao", "percent", "similarity"] if c in tmp.columns]
    other_cols = [c for c in tmp.columns if c not in cols_priority and c not in ["timestamp_dt"]]
    show_cols = cols_priority + other_cols

    with cA:
        st.markdown("**Top 5 maiores similaridades**")
        st.dataframe(
            tmp[show_cols].sort_values("percent", ascending=False).head(5),
            use_container_width=True
        )

    with cB:
        st.markdown("**Top 5 menores similaridades**")
        st.dataframe(
            tmp[show_cols].sort_values("percent", ascending=True).head(5),
            use_container_width=True
        )

    # =========================================================
    # D) BOX PLOT (opcional)
    # =========================================================
    with st.expander("Ver resumo estatístico (boxplot)"):
        fig_b, ax_b = plt.subplots()
        ax_b.boxplot(vals, vert=False)
        ax_b.set_title("Boxplot — Similaridade (%) na sessão")
        ax_b.set_xlabel("Similaridade (%)")

        if fixed_range:
            ax_b.set_xlim(-100, 100)

        ax_b.grid(True, axis="x", alpha=0.3)
        st.pyplot(fig_b, clear_figure=True)

    # =========================================================
    # E) DEBUG (cosine similarity -1..1)
    # =========================================================
    with st.expander("Debug: cosine similarity (-1..1)"):
        if "similarity" not in hist.columns or hist["similarity"].dropna().empty:
            st.info("A coluna `similarity` não está disponível/numérica nesta sessão.")
        else:
            svals = hist["similarity"].dropna().astype(float)

            cD1, cD2, cD3 = st.columns(3)
            cD1.metric("Média", f"{svals.mean():.4f}")
            cD2.metric("Mínimo", f"{svals.min():.4f}")
            cD3.metric("Máximo", f"{svals.max():.4f}")

            fig_s, ax_s = plt.subplots()
            ax_s.hist(svals, bins=20, edgecolor="black", range=(-1, 1))
            ax_s.set_xlim(-1, 1)
            ax_s.set_title("Histograma — cosine similarity (debug)")
            ax_s.set_xlabel("Cosine similarity")
            ax_s.set_ylabel("Frequência")
            ax_s.grid(True, axis="y", alpha=0.3)
            st.pyplot(fig_s, clear_figure=True)

    st.divider()

    # =========================================================
    # F) TABELA + EXPORT
    # =========================================================
    with st.expander("Ver tabela da sessão"):
        sort_col = "timestamp" if "timestamp" in hist.columns else None
        view = hist.sort_values(sort_col, ascending=False) if sort_col else hist

        st.dataframe(view, use_container_width=True)

        csv_bytes = view.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Baixar CSV da sessão",
            data=csv_bytes,
            file_name="historico_sessao.csv",
            mime="text/csv",
        )

st.divider()
