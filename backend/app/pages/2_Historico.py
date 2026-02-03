import streamlit as st
import pandas as pd

st.set_page_config(page_title="Histórico", page_icon="🗂️", layout="wide")
st.title("🗂️ Histórico (sessão)")

df = st.session_state.get("history", pd.DataFrame())

if df.empty:
    st.warning("Ainda não há histórico nesta sessão. Vá em **Comparar** e execute alguns testes.")
    st.stop()

# Garante tipos
if "percent" in df.columns:
    df["percent"] = pd.to_numeric(df["percent"], errors="coerce")

with st.sidebar:
    st.subheader("Filtros")
    min_percent = st.slider("Percentual mínimo", -100, 100, 0)

    # Slider baseado no tamanho real do histórico
    total = len(df)
    max_rows = st.slider(
        "Máx. linhas exibidas",
        min_value=1,
        max_value=total,
        value=min(200, total),
        step=1,
    )

filtered = df.copy()

if "percent" in filtered.columns:
    filtered = filtered[filtered["percent"] >= min_percent]

filtered = filtered.sort_values("timestamp", ascending=False).head(int(max_rows))

st.caption(f"Mostrando {len(filtered)} de {len(df)} registros.")
st.dataframe(filtered, use_container_width=True)

st.divider()

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Baixar CSV filtrado",
    data=csv_bytes,
    file_name="history_filtrado.csv",
    mime="text/csv",
)
