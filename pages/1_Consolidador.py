import streamlit as st
import pandas as pd

from io import BytesIO
from datetime import datetime

# ==========================================================
# IMPORTAÇÃO DOS MÓDULOS
# ==========================================================

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
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Consolidador Pedagógico",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("🏆 CONSOLIDADOR PEDAGÓGICO V9")

st.caption(
    "URE Pirassununga • Consolidação automática de avaliações "
    "ADE • PP1 • PP2 • ADP • PP3"
)

st.divider()

# ==========================================================
# DADOS DA ESCOLA
# ==========================================================

col1, col2 = st.columns([3,1])

with col1:

    nome_escola = st.text_input(
        "Nome da Escola",
        placeholder="Ex.: EE Prof. José Jorge Neto"
    )

with col2:

    ano = st.selectbox(
        "Ano",
        [
            "2026",
            "2027",
            "2028"
        ]
    )

# ==========================================================
# UPLOAD
# ==========================================================

st.subheader("Arquivos")

col1, col2 = st.columns(2)

with col1:

    arquivo_ADE = st.file_uploader(
        "ADE / AVD",
        type=["zip","xlsx","xlsm"],
        key="ADE"
    )

    arquivo_PP1 = st.file_uploader(
        "Prova Paulista 1º Bimestre",
        type=["zip","xlsx","xlsm"],
        key="PP1"
    )

    arquivo_PP2 = st.file_uploader(
        "Prova Paulista 2º Bimestre",
        type=["zip","xlsx","xlsm"],
        key="PP2"
    )

with col2:

    arquivo_ADP = st.file_uploader(
        "ADP",
        type=["zip","xlsx","xlsm"],
        key="ADP"
    )

    arquivo_PP3 = st.file_uploader(
        "Prova Paulista 3º Bimestre",
        type=["zip","xlsx","xlsm"],
        key="PP3"
    )

st.divider()

# ==========================================================
# BOTÕES
# ==========================================================

col1, col2, col3 = st.columns([1,1,4])

with col1:

    gerar = st.button(
        "🚀 Gerar Consolidado",
        use_container_width=True
    )

with col2:

    limpar = st.button(
        "🗑 Limpar",
        use_container_width=True
    )

if limpar:

    st.rerun()

# ==========================================================
# PROCESSAMENTO
# ==========================================================

if gerar:

    try:

        if nome_escola.strip() == "":

            st.warning(
                "Informe o nome da escola."
            )

            st.stop()

        with st.spinner("Lendo arquivos..."):

            df_ADE = None
            df_PP1 = None
            df_PP2 = None
            df_ADP = None
            df_PP3 = None

            # ----------------------------------------------
            # ADE
            # ----------------------------------------------

            if arquivo_ADE is not None:

                df_ADE = ler_ADE(
                    arquivo_ADE
                )

            # ----------------------------------------------
            # PP1
            # ----------------------------------------------

            if arquivo_PP1 is not None:

                df_PP1 = ler_PP(
                    arquivo_PP1,
                    "PP1"
                )

            # ----------------------------------------------
            # PP2
            # ----------------------------------------------

            if arquivo_PP2 is not None:

                df_PP2 = ler_PP(
                    arquivo_PP2,
                    "PP2"
                )

            # ----------------------------------------------
            # ADP
            # ----------------------------------------------

            if arquivo_ADP is not None:

                df_ADP = ler_ADE(
                    arquivo_ADP
                )

            # ----------------------------------------------
            # PP3
            # ----------------------------------------------

            if arquivo_PP3 is not None:

                df_PP3 = ler_PP(
                    arquivo_PP3,
                    "PP3"
                )

        st.success("Arquivos carregados com sucesso.")

        # ==================================================
        # DIAGNÓSTICO DOS ARQUIVOS
        # ==================================================

        with st.expander("Diagnóstico"):

            if df_ADE is not None:

                st.write(
                    "ADE:",
                    len(df_ADE),
                    "registros"
                )

            if df_PP1 is not None:

                st.write(
                    "PP1:",
                    len(df_PP1),
                    "registros"
                )

            if df_PP2 is not None:

                st.write(
                    "PP2:",
                    len(df_PP2),
                    "registros"
                )

            if df_ADP is not None:

                st.write(
                    "ADP:",
                    len(df_ADP),
                    "registros"
                )

            if df_PP3 is not None:

                st.write(
                    "PP3:",
                    len(df_PP3),
                    "registros"
                )

        # ==================================================
        # CONSOLIDAÇÃO
        # ==================================================

        with st.spinner("Consolidando as avaliações..."):

            base_final = consolidar_base(
                df_ADE=df_ADE,
                df_PP1=df_PP1,
                df_PP2=df_PP2,
                df_ADP=df_ADP,
                df_PP3=df_PP3
            )

            base_final = limpar_base(base_final)

        st.success("Base consolidada.")

        # ==================================================
        # DIAGNÓSTICO DA BASE
        # ==================================================

        with st.expander(
            "Diagnóstico da Base Consolidada",
            expanded=False
        ):

            st.write(
                f"Total de estudantes: {len(base_final)}"
            )

            st.write("Colunas disponíveis:")

            st.dataframe(
                pd.DataFrame(
                    {
                        "Colunas":
                        base_final.columns
                    }
                ),
                use_container_width=True
            )

        # ==================================================
        # PARTICIPAÇÃO
        # ==================================================

        with st.spinner(
            "Calculando participação..."
        ):

            base_final = calcular_participacao(
                base_final
            )

            sem_participacao = (
                obter_sem_participacao(
                    base_final
                )
            )

        # ==================================================
        # DEFINE QUAL AVALIAÇÃO
        # MAIS RECENTE
        # ==================================================

        coluna_lp = None
        coluna_mat = None

        if (
            "PP3_LP_STATUS" in base_final.columns
            and
            base_final["PP3_LP_STATUS"].notna().any()
        ):

            coluna_lp = "PP3_LP_STATUS"
            coluna_mat = "PP3_MAT_STATUS"

        elif (

            "ADP_LP_STATUS"
            in base_final.columns

        ):

            coluna_lp = "ADP_LP_STATUS"
            coluna_mat = "ADP_MAT_STATUS"

        elif (

            "PP2_LP_STATUS"
            in base_final.columns

        ):

            coluna_lp = "PP2_LP_STATUS"
            coluna_mat = "PP2_MAT_STATUS"

        elif (

            "PP1_LP_STATUS"
            in base_final.columns

        ):

            coluna_lp = "PP1_LP_STATUS"
            coluna_mat = "PP1_MAT_STATUS"

        elif (

            "ADE_LP_STATUS"
            in base_final.columns

        ):

            coluna_lp = "ADE_LP_STATUS"
            coluna_mat = "ADE_MAT_STATUS"

        # ==================================================
        # PRIORITÁRIOS
        # ==================================================

        if coluna_lp is not None:

            prioritarios = obter_prioritarios(

                base_final,

                coluna_lp,

                coluna_mat

            )

        else:

            prioritarios = pd.DataFrame()

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
        # INDICADORES
        # ==================================================

        st.divider()

        st.subheader(
            "Indicadores Gerais"
        )

        col1, col2, col3, col4 = st.columns(4)

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

        with col4:

            if len(base_final):

                percentual = round(

                    (
                        len(base_final)
                        -
                        len(sem_participacao)
                    )

                    /

                    len(base_final)

                    * 100,

                    1

                )

            else:

                percentual = 0

            st.metric(

                "Participação",

                f"{percentual}%"

            )

        st.divider()

        # ==================================================
        # PAINEL
        # ==================================================

        st.subheader(
            "Painel da Escola"
        )

        st.dataframe(

            painel_escola,

            use_container_width=True,

            hide_index=True

        )

        # ==================================================
        # RESUMO DAS TURMAS
        # ==================================================

        st.subheader(
            "Resumo por Turma"
        )

        st.dataframe(

            resumo_por_turma,

            use_container_width=True,

            hide_index=True

        )

        # ==================================================
        # ALUNOS PRIORITÁRIOS
        # ==================================================

        if len(prioritarios):

            st.subheader(
                "Estudantes Prioritários"
            )

            st.dataframe(

                prioritarios,

                use_container_width=True,

                hide_index=True

            )

        # ==================================================
        # SEM PARTICIPAÇÃO
        # ==================================================

        if len(sem_participacao):

            st.subheader(
                "Sem Participação"
            )

            st.dataframe(

                sem_participacao,

                use_container_width=True,

                hide_index=True

            )

        # ==================================================
        # MONTAGEM DAS ABAS
        # ==================================================

        with st.spinner("Montando planilhas..."):

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

                if len(df) == 0:
                    df = pd.DataFrame()

                df.to_excel(
                    writer,
                    sheet_name=str(nome_aba)[:31],
                    index=False
                )

            workbook = writer.book

            for ws in workbook.worksheets:

                try:

                    aplicar_cores(ws)

                except Exception:

                    pass

        output.seek(0)

        # ==================================================
        # RESUMO FINAL
        # ==================================================

        st.success(
            "Consolidado gerado com sucesso."
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Total de estudantes",
                len(base_final)
            )

        with col2:

            st.metric(
                "Estudantes prioritários",
                len(prioritarios)
            )

        with col3:

            st.metric(
                "Sem participação",
                len(sem_participacao)
            )

        st.divider()

        st.subheader("Visualização da Base Consolidada")

        st.dataframe(

            base_final,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ==================================================
        # DOWNLOAD
        # ==================================================

        data_geracao = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )

        st.caption(
            f"Gerado em {data_geracao}"
        )

        if nome_escola.strip() == "":

            nome_arquivo = (
                "CONSOLIDADO_HISTORICO.xlsx"
            )

        else:

            nome_arquivo = (
                nome_escola.upper()
                .replace(" ", "_")
                .replace("/", "_")
                + "_CONSOLIDADO_HISTORICO.xlsx"
            )

        st.download_button(

            label="📥 BAIXAR CONSOLIDADO",

            data=output,

            file_name=nome_arquivo,

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            use_container_width=True

        )

    # ==================================================
    # FINALIZAÇÃO
    # ==================================================

    except Exception as erro:

        st.error(
            "Ocorreu um erro durante o processamento."
        )

        st.exception(erro)

        st.stop()

# ==========================================================
# RODAPÉ
# ==========================================================

st.divider()

st.caption(
    "Consolidador Pedagógico V9 • URE Pirassununga"
)
        



