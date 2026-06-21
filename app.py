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

from modulos.evolucao import (
    gerar_evolucao
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

    st.success(

        "Processamento iniciado."

    )

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

    # ------------------------------------------------------
    # CONSOLIDAÇÃO
    # ------------------------------------------------------

    base_final = consolidar_base(

        df_ADE,

        df_PP1,

        df_PP2,

        df_ADP,

        df_PP3

    )

    # ------------------------------------------------------
    # LIMPEZA
    # ------------------------------------------------------

    base_final = limpar_base(

        base_final

    )

    # ------------------------------------------------------
    # PARTICIPAÇÃO
    # ------------------------------------------------------

    base_final = calcular_participacao(

        base_final

    )

    sem_participacao = (

        obter_sem_participacao(

            base_final

        )

    )

    st.success(

        "Participação calculada."

    )

    # ------------------------------------------------------
    # PRIORITÁRIOS
    # ------------------------------------------------------

    prioridade_lp = "PP2_LP_STATUS"

    prioridade_mat = "PP2_MAT_STATUS"

    if "PP3_LP_STATUS" in base_final.columns:

        prioridade_lp = "PP3_LP_STATUS"

        prioridade_mat = "PP3_MAT_STATUS"

    prioritarios = (

        obter_prioritarios(

            base_final,

            prioridade_lp,

            prioridade_mat

        )

    )

    st.success(

        "Prioritários identificados."

    )

    # ------------------------------------------------------
    # RESUMO POR TURMA
    # ------------------------------------------------------

    resumo_por_turma = (

        gerar_resumo_por_turma(

            base_final,

            prioritarios

        )

    )

    painel_escola = (

        gerar_painel_escola(

            base_final,

            resumo_por_turma

        )

    )

    st.success(

        "Painel da escola gerado."

    )

    # ------------------------------------------------------
    # EVOLUÇÃO
    # ------------------------------------------------------

    evolucao = gerar_evolucao(

        base_final

    )

    st.success(

        "Evolução calculada."

    )

    # ------------------------------------------------------
    # MONTAGEM DAS ABAS
    # ------------------------------------------------------

    abas = montar_abas(

        painel_escola,

        base_final,

        resumo_por_turma,

        prioritarios,

        sem_participacao,

        evolucao

    )

    st.success(

        "Abas do Excel preparadas."

    )

    # ------------------------------------------------------
    # RESULTADOS
    # ------------------------------------------------------

    st.write(

        "Quantidade de estudantes:",

        len(base_final)

    )

    st.write(

        "Quantidade de prioritários:",

        len(prioritarios)

    )

    st.write(

        "Quantidade de estudantes com baixa participação:",

        len(sem_participacao)

    )

    st.dataframe(

        painel_escola

    )
