import streamlit as st
import pandas as pd

from io import BytesIO
from datetime import datetime

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
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Consolidador Pedagógico",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("🏆 CONSOLIDADOR PEDAGÓGICO V8.1")

st.caption(
    "URE Pirassununga"
)

st.divider()

# ==========================================================
# ESCOLA
# ==========================================================

nome_escola = st.text_input(
    "Nome da escola"
)

st.divider()

# ==========================================================
# ARQUIVOS
# ==========================================================

st.subheader("Arquivos")

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

st.divider()

gerar = st.button(
    "🚀 GERAR CONSOLIDADO",
    use_container_width=True
)

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if gerar:

    try:

        st.info("Iniciando processamento...")

        df_ADE = None
        df_PP1 = None
        df_PP2 = None
        df_ADP = None
        df_PP3 = None

        if arquivo_ADE is not None:
            df_ADE = ler_ADE(arquivo_ADE)

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
            df_ADP = ler_ADE(
                arquivo_ADP
            )

        if arquivo_PP3 is not None:
            df_PP3 = ler_PP(
                arquivo_PP3,
                "PP3"
            )

        st.success("Arquivos carregados.")

        base_final = consolidar_base(
            df_ADE=df_ADE,
            df_PP1=df_PP1,
            df_PP2=df_PP2,
            df_ADP=df_ADP,
            df_PP3=df_PP3
        )

        base_final = limpar_base(
            base_final
        )

        base_final = calcular_participacao(
            base_final
        )

        sem_participacao = obter_sem_participacao(
            base_final
        )

        # ==================================================
        # DEFINIR A AVALIAÇÃO MAIS RECENTE
        # ==================================================

        coluna_lp = "PP2_LP_STATUS"
        coluna_mat = "PP2_MAT_STATUS"

        if (
            "PP3_LP_STATUS" in base_final.columns
            and
            base_final["PP3_LP_STATUS"].notna().any()
        ):

            coluna_lp = "PP3_LP_STATUS"
            coluna_mat = "PP3_MAT_STATUS"

        # ==================================================
        # PRIORITÁRIOS
        # ==================================================

        prioritarios = obter_prioritarios(
            base_final,
            coluna_lp,
            coluna_mat
        )

        # ==================================================
        # RESUMO POR TURMA
        # ==================================================

        resumo_por_turma = gerar_resumo_por_turma(
            base_final,
            prioritarios
        )

        # ==================================================
        # PAINEL DA ESCOLA
        # ==================================================

        painel_escola = gerar_painel_escola(
            base_final,
            resumo_por_turma
        )

        # ==================================================
        # EVOLUÇÃO
        # ==================================================

        evolucao = gerar_evolucao(
            base_final
        )

        # ==================================================
        # MONTAGEM DAS ABAS
        # ==================================================

        abas = montar_abas(
            painel_escola,
            base_final,
            resumo_por_turma,
            prioritarios,
            sem_participacao,
            evolucao
        )

        # ==================================================
        # GERAÇÃO DO EXCEL
        # ==================================================

        output = BytesIO()

        with pd.ExcelWriter(
            output,
            engine="openpyxl"
        ) as writer:

            for nome_aba, df in abas.items():

                if df is None:
                    continue

                df.to_excel(
                    writer,
                    sheet_name=str(nome_aba)[:31],
                    index=False
                )

            workbook = writer.book

            for ws in workbook.worksheets:

                aplicar_cores(ws)

        output.seek(0)

        # ==================================================
        # INDICADORES
        # ==================================================

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Estudantes",
                len(base_final)
            )

        with col2:
            st.metric(
                "Prioritários",
                len(prioritarios)
            )

        with col3:
            st.metric(
                "Sem participação",
                len(sem_participacao)
            )

        st.subheader(
            "Painel da Escola"
        )

        st.dataframe(
            painel_escola,
            use_container_width=True
        )

        st.subheader(
            "Resumo por Turma"
        )

        st.dataframe(
            resumo_por_turma,
            use_container_width=True
        )

        if len(prioritarios):

            st.subheader(
                "Estudantes Prioritários"
            )

            st.dataframe(
                prioritarios,
                use_container_width=True
            )

        # ==================================================
        # SEM PARTICIPAÇÃO
        # ==================================================

        if len(sem_participacao):

            st.subheader(
                "Estudantes sem participação"
            )

            st.dataframe(
                sem_participacao,
                use_container_width=True
            )

        # ==================================================
        # BASE CONSOLIDADA
        # ==================================================

        with st.expander(
            "Visualizar Base Consolidada",
            expanded=False
        ):

            st.dataframe(
                base_final,
                use_container_width=True
            )

        # ==================================================
        # DOWNLOAD
        # ==================================================

        if nome_escola.strip():

            nome_arquivo = (
                nome_escola
                .upper()
                .replace(" ", "_")
                .replace("/", "_")
            )

        else:

            nome_arquivo = "CONSOLIDADO"

        nome_arquivo += (
            "_HISTORICO_"
            + datetime.now().strftime("%Y%m%d_%H%M")
            + ".xlsx"
        )

        st.download_button(

            label="⬇ BAIXAR CONSOLIDADO",

            data=output.getvalue(),

            file_name=nome_arquivo,

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )

        st.success(
            "Consolidado gerado com sucesso!"
        )

    except Exception as erro:

        st.error(
            "Ocorreu um erro durante o processamento."
        )

        st.exception(erro)

st.divider()

st.caption(
    "Consolidador Pedagógico • URE Pirassununga"
)

