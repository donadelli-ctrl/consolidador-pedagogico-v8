import streamlit as st


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(

    page_title="Consolidador Pedagógico V8.0",

    layout="wide"

)


# ==========================================================
# TÍTULO
# ==========================================================

st.title(

    "🏆 CONSOLIDADOR PEDAGÓGICO V8.0"

)

st.subheader(

    "URE Pirassununga"

)


# ==========================================================
# ESCOLA
# ==========================================================

nome_escola = st.text_input(

    "Nome da escola"

)


# ==========================================================
# UPLOAD DOS ARQUIVOS
# ==========================================================

st.header(

    "Arquivos"

)

arquivo_ADE = st.file_uploader(

    "ADE",

    type=[

        "xlsx",

        "xlsm"

    ]

)

arquivo_PP1 = st.file_uploader(

    "PP1",

    type=[

        "xlsx",

        "xlsm"

    ]

)

arquivo_PP2 = st.file_uploader(

    "PP2",

    type=[

        "xlsx",

        "xlsm"

    ]

)

arquivo_ADP = st.file_uploader(

    "ADP",

    type=[

        "xlsx",

        "xlsm"

    ]

)

arquivo_PP3 = st.file_uploader(

    "PP3",

    type=[

        "xlsx",

        "xlsm"

    ]

)


# ==========================================================
# BOTÃO
# ==========================================================

gerar = st.button(

    "GERAR CONSOLIDADO"

)
