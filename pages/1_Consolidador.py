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

from modulos.evolucao import (
    gerar_evolucao
)

from modulos.excel_final import (
    montar_abas
)

from modulos.formatacao_excel import (
    aplicar_cores
)


# ==========================================================
# TÍTULO
# ==========================================================

st.title("🏆 CONSOLIDADOR PEDAGÓGICO V8.1")
st.subheader("URE Pirassununga")


# ==========================================================
# ESCOLA
# ==========================================================

nome_escola = st.text_input("Nome da escola")


# ==========================================================
# UPLOAD DOS ARQUIVOS
# ==========================================================

st.header("Arquivos")

arquivo_ADE = st.file_uploader(
    "ADE / AVDE",
    type=["zip", "xlsx", "xlsm"]
)

arquivo_PP1 = st.file_uploader(
    "PP1",
    type=["zip", "xlsx", "xlsm"]
)

arquivo_PP2 = st.file_uploader(
    "PP2",
    type=["zip", "xlsx", "xlsm"]
)

arquivo_ADP = st.file_uploader(
    "ADP",
    type=["zip", "xlsx", "xlsm"]
)

arquivo_PP3 = st.file_uploader(
    "PP3",
    type=["zip", "xlsx", "xlsm"]
)


# ==========================================================
# BOTÃO
# ==========================================================

gerar = st.button("GERAR CONSOLIDADO")


# ==========================================================
# PROCESSAMENTO
# ==========================================================

if gerar:

    try:

        st.success("Processamento iniciado.")

        # --------------------------------------------------
        # LEITURA
        # --------------------------------------------------

        df_ADE = None
        df_PP1 = None
        df_PP2 = None
        df_ADP = None
        df_PP3 = None

        if arquivo_ADE is not None:
            df_ADE = ler_ADE(arquivo_ADE)

        if arquivo_PP1 is not None:
            df_PP1 = ler_PP(arquivo_PP1, "PP1")

        if arquivo_PP2 is not None:
            df_PP2 = ler_PP(arquivo_PP2, "PP2")

        # ==================================================
        # ADP = MESMO LEITOR DA ADE
        # ==================================================

        if arquivo_ADP is not None:
            df_ADP = ler_ADE(arquivo_ADP)

        if arquivo_PP3 is not None:
    df_PP3 = ler_PP(arquivo_PP3, "PP3")

st.success("Arquivos carregados.")

# ==================================================
# DIAGNÓSTICO PP1
# ==================================================

if df_PP1 is not None:

    st.subheader("DIAGNÓSTICO PP1")

    st.write("COLUNAS DO PP1")

    st.write(df_PP1.columns.tolist())

    st.write("PRIMEIROS REGISTROS")

    st.dataframe(df_PP1.head(10))

        # --------------------------------------------------
        # CONSOLIDAÇÃO
        # --------------------------------------------------

        base_final = consolidar_base(
            df_ADE,
            df_PP1,
            df_PP2,
            df_ADP,
            df_PP3
        )

        base_final = limpar_base(base_final)

        # ==================================================
        # DIAGNÓSTICO TEMPORÁRIO
        # ==================================================

        with st.expander("Diagnóstico da Base", expanded=True):

            st.write("Colunas encontradas:")

            st.write(base_final.columns.tolist())

            st.write("Quantidade de registros:")

            st.write(len(base_final))

        # --------------------------------------------------
        # PARTICIPAÇÃO
        # --------------------------------------------------

        base_final = calcular_participacao(base_final)

        sem_participacao = obter_sem_participacao(base_final)

        # --------------------------------------------------
        # PRIORITÁRIOS
        # --------------------------------------------------

        coluna_lp = "PP2_LP_STATUS"
        coluna_mat = "PP2_MAT_STATUS"

        if (
            "PP3_LP_STATUS" in base_final.columns
            and
            base_final["PP3_LP_STATUS"].notna().any()
        ):

            coluna_lp = "PP3_LP_STATUS"
            coluna_mat = "PP3_MAT_STATUS"

        prioritarios = obter_prioritarios(
            base_final,
            coluna_lp,
            coluna_mat
        )

        # --------------------------------------------------
        # RESUMO
        # --------------------------------------------------

        resumo_por_turma = gerar_resumo_por_turma(
            base_final,
            prioritarios
        )

        painel_escola = gerar_painel_escola(
            base_final,
            resumo_por_turma
        )

        # --------------------------------------------------
        # EVOLUÇÃO
        # --------------------------------------------------

        evolucao = gerar_evolucao(base_final)

        # --------------------------------------------------
        # ABAS
        # --------------------------------------------------

        abas = montar_abas(
            painel_escola,
            base_final,
            resumo_por_turma,
            prioritarios,
            sem_participacao,
            evolucao
        )

        # --------------------------------------------------
        # EXCEL
        # --------------------------------------------------

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

            workbook = writer.book

            for ws in workbook.worksheets:
                aplicar_cores(ws)

        output.seek(0)

        # --------------------------------------------------
        # INDICADORES
        # --------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Estudantes", len(base_final))

        with col2:
            st.metric("Prioritários", len(prioritarios))

        with col3:
            st.metric("Baixa participação", len(sem_participacao))

        st.subheader("Painel da Escola")

        st.dataframe(
            painel_escola,
            use_container_width=True
        )

        # --------------------------------------------------
        # DOWNLOAD
        # --------------------------------------------------

        nome_arquivo = (
            nome_escola.upper().replace(" ", "_")
            + "_CONSOLIDADO_HISTORICO_2026.xlsx"
        )

        st.download_button(
            "⬇ BAIXAR CONSOLIDADO",
            output,
            file_name=nome_arquivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as erro:

        st.error("Ocorreu um erro durante o processamento.")

        st.exception(erro)
