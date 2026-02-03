import streamlit as st
import pandas as pd

st.set_page_config(page_title="Histórico", page_icon="🗂️", layout="wide")

st.title("🗂️ Histórico (sessão)")

df = st.session_state.get("history", pd.DataFrame())

if df.empty:
    st.warning("Ainda não há histórico nesta sessão. Vá em **Comparar** e execute alguns testes.")
    st.stop()

with st.sidebar:
    st.subheader("Filtros")
    models = sorted(df["model_label"].unique().tolist()) if "model_label" in df.columns else []
    model_filter = st.multiselect("Modelo", options=models, default=models)

    min_percent = st.slider("Percentual mínimo", 0, 100, 0)
    max_rows = st.number_input("Máx. linhas", min_value=10, max_value=5000, value=200, step=10)

filtered = df.copy()

if "model_label" in filtered.columns and model_filter:
    filtered = filtered[filtered["model_label"].isin(model_filter)]

if "percent" in filtered.columns:
    filtered["percent"] = pd.to_numeric(filtered["percent"], errors="coerce")
    filtered = filtered[filtered["percent"] >= min_percent]

filtered = filtered.sort_values("timestamp", ascending=False).head(int(max_rows))

st.dataframe(filtered, use_container_width=True)

st.divider()

csv_bytes = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Baixar CSV filtrado",
    data=csv_bytes,
    file_name="history_filtrado.csv",
    mime="text/csv",
)
