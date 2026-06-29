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
    "Aluno",
    "Nome do Estudante",
    "Nome do aluno",
    "Estudante"
]

COLUNAS_TURMA = [
    "TURMA",
    "Turma",
    "Classe",
    "Classe/Turma",
    "Classe Turma",
    "Sala",
    "Sala/Turma"
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

    novo = pd.DataFrame(index=df.index)

    if coluna_ra is not None:
        novo["RA"] = df[coluna_ra]
    else:
        novo["RA"] = ""

    if coluna_nome is not None:
        novo["NOME"] = df[coluna_nome]
    else:
        novo["NOME"] = ""

    if coluna_turma is not None:
        novo["TURMA"] = df[coluna_turma]
    else:
        novo["TURMA"] = ""

    if coluna_lp is not None:
        novo["ADE_LP"] = df[coluna_lp]
    else:
        novo["ADE_LP"] = ""

    if coluna_mat is not None:
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

        # Ignora planilhas ocultas de sistema
        if str(nome_planilha).strip().startswith("_"):
            continue

        # Remove linhas totalmente vazias
        df = df.dropna(how="all")

        if df.empty:
            continue

        lista.append(df)

    return lista


# ==========================================================
# LEITURA DE ARQUIVOS ZIP
# ==========================================================

def ler_zip(arquivo_zip):

    lista = []

    with zipfile.ZipFile(arquivo_zip) as z:

        arquivos_excel = sorted(

            arq

            for arq in z.namelist()

            if (
                arq.lower().endswith((".xlsx", ".xlsm"))
                and
                not Path(arq).name.startswith("~$")
                and
                not Path(arq).name.startswith(".")
            )

        )

        if not arquivos_excel:

            raise Exception(
                "Nenhum arquivo Excel encontrado no ZIP."
            )

        for nome_arquivo in arquivos_excel:

            try:

                with z.open(nome_arquivo) as f:

                    dados = BytesIO(f.read())

                    lista.extend(
                        ler_excel(dados)
                    )

            except Exception as erro:

                print(
                    f"[AVISO] Arquivo ignorado: "
                    f"{nome_arquivo} ({erro})"
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
    ).strip().lower()

    if nome.endswith(".zip"):
        return ler_zip(arquivo)

    elif nome.endswith((".xlsx", ".xlsm")):
        return ler_excel(arquivo)

    raise ValueError(
        f"Formato de arquivo não suportado: {nome}"
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

    # Remove ".0" quando o RA vem como número decimal
    df["RA"] = df["RA"].str.replace(".0", "", regex=False)

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
    # RESULTADOS
    # ------------------------------------------------------

    for coluna in ["ADE_LP", "ADE_MAT"]:

        df[coluna] = (
            df[coluna]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    # ------------------------------------------------------
    # REMOVE LINHAS SEM NOME
    # ------------------------------------------------------

    df = df[df["NOME"] != ""]

    # Remove possíveis cabeçalhos repetidos
    df = df[
        ~df["NOME"].str.upper().isin([
            "NOME",
            "ESTUDANTE",
            "ALUNO"
        ])
    ]

    # ------------------------------------------------------
    # REMOVE DUPLICIDADES
    # ------------------------------------------------------

    df = df.drop_duplicates(
        subset=["RA", "NOME", "TURMA"],
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

    # Remove espaços e garante string
    df["RA"] = (
        df["RA"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["NOME"] = (
        df["NOME"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    df["TURMA"] = (
        df["TURMA"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    possui_ra = df["RA"] != ""

    # Quando existe RA, utiliza RA + TURMA
    df.loc[possui_ra, "CHAVE_MERGE"] = (
        df.loc[possui_ra, "RA"]
        + "_"
        + df.loc[possui_ra, "TURMA"]
    )

    # Quando não existe RA, utiliza NOME + TURMA
    df.loc[~possui_ra, "CHAVE_MERGE"] = (
        df.loc[~possui_ra, "NOME"]
        .str.upper()
        + "_"
        + df.loc[~possui_ra, "TURMA"]
    )

    return df


# ==========================================================
# UNE TODOS OS DATAFRAMES
# ==========================================================

def consolidar_dataframes(lista_df):

    if not lista_df:
        raise ValueError(
            "Nenhuma planilha válida encontrada."
        )

    lista_limpa = []

    for df in lista_df:

        try:

            df_limpo = limpar_dataframe(df)

            if not df_limpo.empty:
                lista_limpa.append(df_limpo)

        except Exception as erro:

            print(
                f"[AVISO] Planilha ignorada: {erro}"
            )

    if not lista_limpa:

        raise ValueError(
            "Nenhum dado válido encontrado após a limpeza."
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

    df_final = df_final.sort_values(
        by=["TURMA", "NOME"],
        ignore_index=True
    )

    return df_final

# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def ler_ADE(arquivo):
    """
    Lê arquivos ADE, AVD e ADP e devolve um DataFrame
    padronizado para o Consolidador Pedagógico.
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

        raise RuntimeError(
            f"Erro ao processar ADE/AVD/ADP: {erro}"
        ) from erro

