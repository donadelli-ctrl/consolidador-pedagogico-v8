import pandas as pd
import zipfile

from io import BytesIO
from pathlib import Path

from modulos.padronizacao import (
    padronizar_nome,
    padronizar_turma
)


# ==========================================================
# LEITOR ADE / AVD / ADP
# VERSÃO 2.0
# Consolidador Pedagógico
# ==========================================================


# ==========================================================
# NOMES POSSÍVEIS DAS COLUNAS
# ==========================================================

COLUNAS_RA = [
    "RA",
    "ID",
    "Id",
    "Id ",
    "Registro",
    "Registro do Aluno",
    "Matrícula",
    "Matricula",
    "Código",
    "Codigo"
]

COLUNAS_NOME = [
    "ESTUDANTE",
    "ALUNO",
    "NOME",
    "Nome",
    "Aluno"
]

COLUNAS_TURMA = [
    "TURMA",
    "Turma",
    "Classe"
]

COLUNAS_LP = [
    "Status",
    "STATUS",
    "Status LP",
    "LP",
    "Língua Portuguesa",
    "Lingua Portuguesa"
]

COLUNAS_MAT = [
    "Status.1",
    "STATUS.1",
    "Status MAT",
    "MAT",
    "Matemática",
    "Matematica"
]


# ==========================================================
# LOCALIZA UMA COLUNA PELO NOME
# ==========================================================

def localizar_coluna(df, possibilidades):
    """
    Procura uma coluna ignorando diferenças de
    maiúsculas/minúsculas e espaços extras.
    """

    mapa = {
        str(coluna).strip().upper(): coluna
        for coluna in df.columns
    }

    for nome in possibilidades:

        chave = str(nome).strip().upper()

        if chave in mapa:
            return mapa[chave]

    return None
    
# ==========================================================
# PADRONIZA NOMES DAS COLUNAS
# ==========================================================

def preparar_colunas(df):

    df.columns = [

        str(coluna).strip()

        for coluna in df.columns

    ]

    return df


# ==========================================================
# PADRONIZA O DATAFRAME
# ==========================================================

def padronizar_dataframe(df):

    df = preparar_colunas(df)

    coluna_ra = localizar_coluna(df, COLUNAS_RA)
    coluna_nome = localizar_coluna(df, COLUNAS_NOME)
    coluna_turma = localizar_coluna(df, COLUNAS_TURMA)
    coluna_lp = localizar_coluna(df, COLUNAS_LP)
    coluna_mat = localizar_coluna(df, COLUNAS_MAT)

    novo = pd.DataFrame()

    if coluna_ra:
        novo["RA"] = df[coluna_ra]
    else:
        novo["RA"] = ""

    if coluna_nome:
        novo["NOME"] = df[coluna_nome]
    else:
        novo["NOME"] = ""

    if coluna_turma:
        novo["TURMA"] = df[coluna_turma]
    else:
        novo["TURMA"] = ""

    if coluna_lp:
        novo["ADE_LP"] = df[coluna_lp]
    else:
        novo["ADE_LP"] = ""

    if coluna_mat:
        novo["ADE_MAT"] = df[coluna_mat]
    else:
        novo["ADE_MAT"] = ""

    return novo

# ==========================================================
# LEITURA DE UM ARQUIVO EXCEL
# ==========================================================

def ler_excel(arquivo):

    planilhas = pd.read_excel(
        arquivo,
        sheet_name=None
    )

    lista = []

    for nome_planilha, df in planilhas.items():

        if df is None:
            continue

        if df.empty:
            continue

        lista.append(df)

    return lista


# ==========================================================
# LEITURA DE ZIP
# ==========================================================

def ler_zip(arquivo_zip):

    lista = []

    with zipfile.ZipFile(arquivo_zip) as z:

        arquivos_excel = sorted([

            arq

            for arq in z.namelist()

            if (
                arq.lower().endswith((".xlsx", ".xlsm"))
                and
                not Path(arq).name.startswith("~$")
            )

        ])

        if len(arquivos_excel) == 0:

            raise Exception(
                "Nenhum arquivo Excel encontrado no ZIP."
            )

        for arquivo in arquivos_excel:

            try:

                with z.open(arquivo) as f:

                    dados = BytesIO(f.read())

                    lista.extend(
                        ler_excel(dados)
                    )

            except Exception as erro:

                print(
                    f"Aviso: não foi possível ler '{arquivo}'. "
                    f"Erro: {erro}"
                )

    return lista


# ==========================================================
# CARREGA TODOS OS DATAFRAMES
# ==========================================================

def carregar_dataframes(arquivo):

    nome = getattr(
        arquivo,
        "name",
        ""
    ).lower()

    if nome.endswith(".zip"):

        return ler_zip(arquivo)

    if nome.endswith(".xlsx") or nome.endswith(".xlsm"):

        return ler_excel(arquivo)

    raise Exception(
        "Formato de arquivo não suportado."
    )

# ==========================================================
# LIMPEZA E PADRONIZAÇÃO DOS DADOS
# ==========================================================

def limpar_dataframe(df):

    df = padronizar_dataframe(df).copy()

    # ------------------------------------------------------
    # RA
    # ------------------------------------------------------

    df["RA"] = (
        df["RA"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------
    # NOME
    # ------------------------------------------------------

    df["NOME"] = (
        df["NOME"]
        .fillna("")
        .astype(str)
        .apply(padronizar_nome)
    )

    # ------------------------------------------------------
    # TURMA
    # ------------------------------------------------------

    df["TURMA"] = (
        df["TURMA"]
        .fillna("")
        .astype(str)
        .apply(padronizar_turma)
    )

    # ------------------------------------------------------
    # LP
    # ------------------------------------------------------

    df["ADE_LP"] = (
        df["ADE_LP"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------
    # MAT
    # ------------------------------------------------------

    df["ADE_MAT"] = (
        df["ADE_MAT"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------
    # REMOVE LINHAS SEM ALUNO
    # ------------------------------------------------------

    df = df[
        (df["NOME"] != "")
    ]

    # ------------------------------------------------------
    # REMOVE DUPLICADOS
    # ------------------------------------------------------

    df = df.drop_duplicates(
        subset=[
            "RA",
            "NOME",
            "TURMA"
        ],
        keep="first"
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df


# ==========================================================
# CRIA CHAVE PARA O MERGE
# ==========================================================

def criar_chave(df):

    df = df.copy()

    possui_ra = df["RA"].astype(str).str.strip() != ""

    df.loc[possui_ra, "CHAVE_MERGE"] = (
        df.loc[possui_ra, "RA"]
        + "_"
        + df.loc[possui_ra, "TURMA"]
    )

    df.loc[~possui_ra, "CHAVE_MERGE"] = (
        df.loc[~possui_ra, "NOME"]
        + "_"
        + df.loc[~possui_ra, "TURMA"]
    )

    return df


# ==========================================================
# UNE TODOS OS DATAFRAMES
# ==========================================================

def consolidar_dataframes(lista_df):

    if len(lista_df) == 0:
        raise Exception(
            "Nenhuma planilha válida encontrada."
        )

    lista_limpa = []

    for df in lista_df:

        try:

            df = limpar_dataframe(df)

            if not df.empty:
                lista_limpa.append(df)

        except Exception as erro:

            print(
                f"Aviso: planilha ignorada ({erro})"
            )

    if len(lista_limpa) == 0:

        raise Exception(
            "Nenhum dado válido encontrado."
        )

    df_final = pd.concat(
        lista_limpa,
        ignore_index=True
    )

    df_final = criar_chave(df_final)

    df_final = df_final.drop_duplicates(
        subset="CHAVE_MERGE",
        keep="first"
    )

    df_final.reset_index(
        drop=True,
        inplace=True
    )

    return df_final

# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def ler_ADE(arquivo):
    """
    Lê arquivos ADE / AVD / ADP nos formatos:
        - .xlsx
        - .xlsm
        - .zip (contendo arquivos Excel)

    Retorna um DataFrame padronizado contendo:
        RA
        NOME
        TURMA
        ADE_LP
        ADE_MAT
        CHAVE_MERGE
    """

    try:

        lista_df = carregar_dataframes(arquivo)

        df_final = consolidar_dataframes(lista_df)

        colunas = [
            "RA",
            "NOME",
            "TURMA",
            "ADE_LP",
            "ADE_MAT",
            "CHAVE_MERGE"
        ]

        for coluna in colunas:
            if coluna not in df_final.columns:
                df_final[coluna] = ""

        df_final = df_final[colunas]

        return df_final

    except Exception as erro:

        raise Exception(
            f"Erro ao processar o arquivo ADE/AVD/ADP: {erro}"
        )

