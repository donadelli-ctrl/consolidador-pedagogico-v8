import streamlit as st
import pandas as pd
from io import BytesIO

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

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if gerar:

    # ------------------------------------------------------
    # LEITURA
    # ------------------------------------------------------

    df_ADE = ler_ADE(

        arquivo_ADE

    )

    df_PP1 = ler_PP(

        arquivo_PP1,

        "PP1"

    ) if arquivo_PP1 else None

    df_PP2 = ler_PP(

        arquivo_PP2,

        "PP2"

    ) if arquivo_PP2 else None

    df_ADP = ler_PP(

        arquivo_ADP,

        "ADP"

    ) if arquivo_ADP else None

    df_PP3 = ler_PP(

        arquivo_PP3,

        "PP3"

    ) if arquivo_PP3 else None

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

    base_final = limpar_base(

        base_final

    )

    # ------------------------------------------------------
    # EVOLUÇÃO
    # ------------------------------------------------------

    evolucao = gerar_evolucao(

        base_final

    )

    base_final["EVOL_LP"] = evolucao["EVOL LP"]

    base_final["EVOL_MAT"] = evolucao["EVOL MAT"]

    base_final["SITUACAO"] = evolucao["SITUAÇÃO"]

    # ------------------------------------------------------
    # PARTICIPAÇÃO
    # ------------------------------------------------------

    base_final = calcular_participacao(

        base_final

    )

    sem_participacao = obter_sem_participacao(

        base_final

    )

    # ------------------------------------------------------
    # PRIORITÁRIOS
    # ------------------------------------------------------

    coluna_lp = "PP2_LP_STATUS"

    coluna_mat = "PP2_MAT_STATUS"

    if "PP3_LP_STATUS" in base_final.columns:

        coluna_lp = "PP3_LP_STATUS"

        coluna_mat = "PP3_MAT_STATUS"

    prioritarios = obter_prioritarios(

        base_final,

        coluna_lp,

        coluna_mat

    )

    # ------------------------------------------------------
    # INDICADORES
    # ------------------------------------------------------

    resumo_por_turma = gerar_resumo_por_turma(

        base_final,

        prioritarios

    )

    painel_escola = gerar_painel_escola(

        base_final,

        resumo_por_turma

    )

    # ------------------------------------------------------
    # ABAS
    # ------------------------------------------------------

    abas = montar_abas(

        painel_escola,

        base_final,

        resumo_por_turma,

        prioritarios,

        sem_participacao,

        evolucao

    )

    # ------------------------------------------------------
    # GERAR EXCEL
    # ------------------------------------------------------

    output = BytesIO()

    with pd.ExcelWriter(

        output,

        engine="openpyxl"

    ) as writer:

        for nome_aba, df in abas.items():

            df.to_excel(

                writer,

                sheet_name=str(nome_aba)[:31],

                index=False

            )

    output.seek(

        0

    )

    # ------------------------------------------------------
    # DOWNLOAD
    # ------------------------------------------------------

    nome_arquivo = (

        nome_escola

        .upper()

        .replace(

            " ",

            "_"

        )

        +

        "_CONSOLIDADO_2026.xlsx"

    )

    st.success(

        "Consolidado gerado com sucesso."

    )

    st.download_button(

        "⬇ BAIXAR CONSOLIDADO",

        data=output,

        file_name=nome_arquivo,

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    )
