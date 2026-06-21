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

from modulos.evolucao import (
    gerar_evolucao
)

from modulos.excel_final import (
    montar_abas
)


# ==========================================================
# TÍTULO
# ==========================================================

st.title(

    "🏆 CONSOLIDADOR PEDAGÓGICO V8.1"

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
# ARQUIVOS
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
