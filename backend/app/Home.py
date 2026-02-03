import streamlit as st

st.set_page_config(
    page_title="Comparador Semântico",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Comparador Semântico de Textos (PT-BR)")
st.write(
    "Aplicação que compara **dois textos** usando **embeddings** e calcula a **similaridade semântica** "
    "via *cosine similarity* (não é comparação literal)."
)


st.divider()

# =============================
# EXEMPLOS RÁPIDOS
# =============================
st.subheader("🚀 Exemplos rápidos para teste")

examples = [
    # PARÁFRASE FORTE
    (
        "Paráfrase forte",
        "O aluno estudou muito para a prova final.",
        "O estudante se dedicou bastante para o exame final."
    ),
    (
        "Paráfrase forte",
        "O sistema apresentou falhas após a atualização.",
        "Depois da atualização, o software começou a apresentar erros."
    ),

    # PARÁFRASE MÉDIA
    (
        "Paráfrase média",
        "A empresa reduziu custos para aumentar o lucro.",
        "A organização diminuiu despesas para lucrar mais."
    ),
    (
        "Paráfrase média",
        "O servidor caiu durante o pico de acesso.",
        "Em horário de maior tráfego, o sistema ficou fora do ar."
    ),

    # MESMO TEMA
    (
        "Mesmo tema",
        "Redes neurais são usadas para reconhecimento de imagens.",
        "Algoritmos de aprendizado de máquina analisam dados visuais."
    ),
    (
        "Mesmo tema",
        "Testes automatizados ajudam a manter a qualidade do software.",
        "Revisar código é importante antes da entrega."
    ),

    # CONTRADITÓRIO
    (
        "Contraditório",
        "O projeto foi entregue antes do prazo.",
        "O projeto atrasou e não foi concluído no tempo previsto."
    ),
    (
        "Contraditório",
        "A internet está muito rápida hoje.",
        "A conexão está extremamente lenta hoje."
    ),

    # DIFERENTES
    (
        "Diferentes",
        "O banco de dados utiliza chaves primárias.",
        "Gosto de viajar para a praia nas férias."
    ),
    (
        "Diferentes",
        "O algoritmo utiliza busca em largura.",
        "Meu cachorro dorme no sofá."
    ),
]

# guarda exemplos no session_state pra página Comparar
if "example_a" not in st.session_state:
    st.session_state["example_a"] = ""
    st.session_state["example_b"] = ""

for i, (cat, a, b) in enumerate(examples, start=1):
    with st.container():
        col1, col2, col3 = st.columns([1, 4, 1])

        with col1:
            st.markdown(f"**{i}. {cat}**")

        with col2:
            st.write(f"**A:** {a}")
            st.write(f"**B:** {b}")

        with col3:
            if st.button("Usar", key=f"use_{i}"):
                st.session_state["example_a"] = a
                st.session_state["example_b"] = b
                st.success("Exemplo enviado para Comparar!")

        st.markdown("---")

# =============================
# COMO USAR
# =============================
st.subheader("📌 Como usar")

st.markdown(
    "- Clique em **Usar** em um exemplo\n"
    "- Vá em **Comparar** no menu\n"
    "- Os textos já estarão preenchidos\n"
    "- Clique em **Comparar**\n"
)

st.caption(
    "💡 Dica: paráfrases tendem a gerar valores altos, textos sem relação valores baixos "
    "e frases contraditórias valores intermediários, pois compartilham o mesmo contexto semântico."
)