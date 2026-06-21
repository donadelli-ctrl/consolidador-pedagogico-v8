import streamlit as st

# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(

    page_title="Consolidador Pedagógico 2026",

    page_icon="📊",

    layout="wide"

)

# ==========================================================
# TÍTULO
# ==========================================================

st.title("📊 CONSOLIDADOR PEDAGÓGICO 2026")

st.subheader("URE Pirassununga")

st.markdown("---")

# ==========================================================
# LGPD
# ==========================================================

st.info(

    """
    🔒 Os arquivos enviados são utilizados exclusivamente
    para gerar o consolidado pedagógico.

    Nenhum dado dos estudantes é armazenado após o
    processamento.
    """

)

# ==========================================================
# ESCOLA
# ==========================================================

escola = st.text_input(

    "Nome da Escola"

)

# ==========================================================
# BOTÃO TESTE
# ==========================================================

gerar = st.button(

    "🚀 GERAR CONSOLIDADO"

)

if gerar:

    st.success(

        "Estrutura da V8.0 criada com sucesso!"

    )
