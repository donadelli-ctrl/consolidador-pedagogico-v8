import streamlit as st

from modulos.leitor_ade import ler_ADE
from modulos.leitor_pp import ler_PP

from modulos.consolidacao import consolidar_base

from modulos.limpeza import limpar_base

from modulos.participacao import (
    calcular_participacao,
    obter_sem_participacao
)

from modulos.prioritarios import (
    obter_prioritarios
)

from modulos.escola_em_numeros import (
    gerar_resumo_por_turma,
    gerar_painel_escola
)

from modulos.excel_final import (
    montar_abas
)


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

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if gerar:

    st.success("Processamento iniciado.")

    # ------------------------------------------------------
    # LEITURA DOS ARQUIVOS
    # ------------------------------------------------------

    df_ADE = None
    df_PP1 = None
    df_PP2 = None
    df_ADP = None
    df_PP3 = None

    if arquivo_ADE is not None:

        df_ADE = ler_ADE(

            arquivo_ADE

        )

    if arquivo_PP1 is not None:

        df_PP1 = ler_PP(

            arquivo_PP1,

            "PP1"

        )

    if arquivo_PP2 is not None:

        df_PP2 = ler_PP(

            arquivo_PP2,

            "PP2"

        )

    if arquivo_ADP is not None:

        df_ADP = ler_PP(

            arquivo_ADP,

            "ADP"

        )

    if arquivo_PP3 is not None:

        df_PP3 = ler_PP(

            arquivo_PP3,

            "PP3"

        )

    st.success(

        "Arquivos carregados."

    )
    
