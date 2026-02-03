import streamlit as st
import pandas as pd
from datetime import datetime

from core import get_paths, load_model, cosine_similarity, classify, MODELS

st.set_page_config(page_title="Comparar", page_icon="🧪", layout="wide")

paths = get_paths()  # mantém (útil pro app)

# Modelo fixo (produto final)
MODEL_LABEL = "Multilingual (final)"

st.title("🧪 Comparar textos")
st.caption(f"Modelo fixo: {MODEL_LABEL} — {MODELS[MODEL_LABEL]}")

# Sidebar só com info (sem config)
with st.sidebar:
    st.subheader("Histórico")
    st.caption("Modo **privado por sessão** (não compartilha com outros usuários).")
    st.markdown("---")
    st.caption("Dica: faça alguns testes e depois veja **Histórico** e **Análises**.")

@st.cache_resource(show_spinner=False)
def _cached_model(model_label: str):
    return load_model(model_label)

# Inicializa histórico da sessão
if "history" not in st.session_state:
    st.session_state["history"] = pd.DataFrame(
        columns=[
            "timestamp",
            "model_label",
            "model_name",
            "text_a",
            "text_b",
            "similarity",
            "percent",
            "classificacao",
        ]
    )

# carrega modelo fixo
model_label = MODEL_LABEL
model = _cached_model(model_label)

colA, colB = st.columns(2)

with colA:
    text_a = st.text_area(
        "Texto A",
        height=220,
        value=st.session_state.get("example_a", ""),
        placeholder="Cole ou digite o Texto A...",
    )

with colB:
    text_b = st.text_area(
        "Texto B",
        height=220,
        value=st.session_state.get("example_b", ""),
        placeholder="Cole ou digite o Texto B...",
    )

btn = st.button("Comparar", type="primary", use_container_width=True)

if btn:
    a = text_a.strip()
    b = text_b.strip()

    if not a or not b:
        st.error("Preencha os dois textos.")
        st.stop()

    # Aviso para entradas muito curtas (embeddings podem ficar instáveis)
    # Regra prática: se ambos tiverem menos de 2 palavras OU forem muito curtinhos
    if (len(a.split()) < 2 and len(b.split()) < 2) or (len(a) < 3 or len(b) < 3):
        st.warning(
            "⚠️ **Entradas muito curtas** (ex.: 1 palavra ou poucas letras) podem gerar "
            "similaridades artificiais. Para resultados mais confiáveis, use frases ou "
            "pequenos parágrafos."
        )

    with st.spinner("Calculando similaridade..."):
        score = cosine_similarity(model, a, b)

    percent = score * 100
    nivel = classify(score)

    st.success("Comparação concluída!")

    c1, c2, c3 = st.columns(3)
    c1.metric("Similaridade (−1 a 1)", f"{score:.4f}")
    c2.metric("Percentual", f"{percent:.2f}%")
    c3.metric("Classificação", nivel)

    st.caption(f"Modelo usado: {model_label} ({MODELS[model_label]})")

    # Salvar no histórico da sessão
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "model_label": model_label,
        "model_name": MODELS[model_label],
        "text_a": a,
        "text_b": b,
        "similarity": round(score, 6),
        "percent": round(percent, 2),
        "classificacao": nivel,
    }

    st.session_state["history"] = pd.concat(
        [st.session_state["history"], pd.DataFrame([new_row])],
        ignore_index=True,
    )

st.divider()
st.subheader("Meu histórico (sessão)")

hist = st.session_state["history"]

if hist.empty:
    st.info("Ainda não há itens. Faça uma comparação acima.")
else:
    st.dataframe(hist.sort_values("timestamp", ascending=False), use_container_width=True)

colx, coly = st.columns(2)

with colx:
    if st.button("🧹 Limpar meu histórico (sessão)"):
        st.session_state["history"] = st.session_state["history"].iloc[0:0]
        st.success("Histórico da sessão limpo.")

with coly:
    csv_bytes = hist.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Baixar meu histórico (CSV)",
        data=csv_bytes,
        file_name="meu_historico.csv",
        mime="text/csv",
        use_container_width=True,
    )
