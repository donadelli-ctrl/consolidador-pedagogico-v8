# ==========================================================
# LEITOR PROVA PAULISTA - MVP
# ==========================================================

import os
import zipfile
from io import BytesIO

import pandas as pd

from modulos.padronizacao import (
    padronizar_nome,
    padronizar_turma,
    normalizar_ra,
    criar_chave_merge
)


# ==========================================================
# CLASSIFICAÇÃO
# ==========================================================

def classificar_pp(valor):

    if pd.isna(valor):
        return ""

    try:
        valor = float(valor)
    except:
        return ""

    if valor > 1:
        valor /= 100

    if valor < 0.50:
        return "Abaixo do Básico"

    elif valor < 0.70:
        return "Básico"

    elif valor < 0.90:
        return "Adequado"

    return "Proficiente"


# ==========================================================
# OBTÉM A TURMA PELO NOME DO ARQUIVO
# ==========================================================

def obter_turma(nome_arquivo):

    turma = os.path.splitext(
        os.path.basename(nome_arquivo)
    )[0]

    return padronizar_turma(turma)


# ==========================================================
# LEITURA DA PLANILHA
# ==========================================================

def ler_planilha(arquivo):

    bruto = pd.read_excel(
        arquivo,
        header=None,
        dtype=object
    )

    linha_cabecalho = None

    limite = min(20, len(bruto))

    for i in range(limite):

        texto = " ".join(
            bruto.iloc[i]
            .fillna("")
            .astype(str)
            .str.upper()
        )

        possui_ra = (
            "RA" in texto
            or "NR RA" in texto
            or "Nº RA" in texto
            or "NUMERO RA" in texto
            or "NÚMERO RA" in texto
        )

        possui_nome = (
            "NOME" in texto
            or "ALUNO" in texto
            or "ESTUDANTE" in texto
        )

        if possui_ra and possui_nome:

            linha_cabecalho = i
            break

    if linha_cabecalho is None:

        raise ValueError(
            "Cabeçalho não localizado."
        )

    arquivo.seek(0)

    df = pd.read_excel(
        arquivo,
        header=linha_cabecalho
    )

    df = df.dropna(
        axis=1,
        how="all"
    )

    df = df.dropna(
        how="all"
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    df.columns = [

        str(coluna)
        .strip()
        .upper()

        for coluna in df.columns

    ]

    return df

# ==========================================================
# LEITOR PRINCIPAL
# ==========================================================

def ler_PP(arquivo, prefixo):

    if arquivo is None:
        return pd.DataFrame()

    lista = []

    # ------------------------------------------------------
    # LEITURA DE ZIP
    # ------------------------------------------------------

    if arquivo.name.lower().endswith(".zip"):

        with zipfile.ZipFile(arquivo) as zip_ref:

            arquivos = sorted([

                nome

                for nome in zip_ref.namelist()

                if nome.lower().endswith(
                    (".xlsx", ".xlsm")
                )

                and not os.path.basename(nome).startswith("~$")

            ])

            for nome in arquivos:

                with zip_ref.open(nome) as f:

                    dados = BytesIO(f.read())

                    df = ler_planilha(dados)

                    df["TURMA"] = obter_turma(nome)

                    lista.append(df)

    else:

        df = ler_planilha(arquivo)

        if "TURMA" not in df.columns:

            df["TURMA"] = obter_turma(
                arquivo.name
            )

        lista.append(df)

    if len(lista) == 0:

        return pd.DataFrame()

    df = pd.concat(
        lista,
        ignore_index=True
    )

    # ------------------------------------------------------
    # PADRONIZA NOMES DAS COLUNAS
    # ------------------------------------------------------

    mapa = {}

    for coluna in df.columns:

        nome = str(coluna).upper()

        if (
            nome == "RA"
            or "NR RA" in nome
            or "Nº RA" in nome
            or "NUMERO RA" in nome
            or "NÚMERO RA" in nome
        ):

            mapa[coluna] = "RA"

        elif any(
            x in nome
            for x in [
                "NOME",
                "ALUNO",
                "ESTUDANTE"
            ]
        ):

            mapa[coluna] = "NOME"

        elif any(
            x in nome
            for x in [
                "PORT",
                "PORTUG",
                "LINGUA",
                "LÍNGUA",
                "LP"
            ]
        ):

            mapa[coluna] = "PORT"

        elif any(
            x in nome
            for x in [
                "MAT",
                "MATEM"
            ]
        ):

            mapa[coluna] = "MAT"

    df.rename(
        columns=mapa,
        inplace=True
    )

    for coluna in [
        "RA",
        "NOME",
        "PORT",
        "MAT",
        "TURMA"
    ]:

        if coluna not in df.columns:

            df[coluna] = ""

    # ------------------------------------------------------
    # NORMALIZAÇÃO
    # ------------------------------------------------------

    df["RA"] = (
        df["RA"]
        .apply(normalizar_ra)
        .fillna("")
        .astype(str)
    )

    df["NOME"] = (
        df["NOME"]
        .fillna("")
        .astype(str)
        .apply(padronizar_nome)
    )

    df["TURMA"] = (
        df["TURMA"]
        .fillna("")
        .astype(str)
        .apply(padronizar_turma)
    )

    # ------------------------------------------------------
    # CONVERTE NOTAS
    # ------------------------------------------------------

    df["PORT"] = pd.to_numeric(
        df["PORT"],
        errors="coerce"
    )

    df["MAT"] = pd.to_numeric(
        df["MAT"],
        errors="coerce"
    )

    df.loc[df["PORT"] > 1, "PORT"] = (
        df.loc[df["PORT"] > 1, "PORT"] / 100
    )

    df.loc[df["MAT"] > 1, "MAT"] = (
        df.loc[df["MAT"] > 1, "MAT"] / 100
    )

    # ------------------------------------------------------
    # RESULTADOS
    # ------------------------------------------------------

    df[f"{prefixo}_LP"] = df["PORT"]

    df[f"{prefixo}_MAT"] = df["MAT"]

    df[f"{prefixo}_LP_STATUS"] = (
        df["PORT"].apply(classificar_pp)
    )

    df[f"{prefixo}_MAT_STATUS"] = (
        df["MAT"].apply(classificar_pp)
    )

    # ------------------------------------------------------
    # CHAVE DE MERGE
    # ------------------------------------------------------

    df["CHAVE_MERGE"] = df.apply(
        lambda linha: criar_chave_merge(
            linha["RA"],
            linha["NOME"],
            linha["TURMA"]
        ),
        axis=1
    )

    # ------------------------------------------------------
    # REMOVE DUPLICADOS
    # ------------------------------------------------------

    df = (
        df
        .drop_duplicates(
            subset="CHAVE_MERGE",
            keep="first"
        )
        .sort_values(
            by=["TURMA", "NOME"],
            ignore_index=True
        )
    )

    # ------------------------------------------------------
    # RETORNO
    # ------------------------------------------------------

    return df[
        [
            "RA",
            "NOME",
            "TURMA",
            f"{prefixo}_LP",
            f"{prefixo}_LP_STATUS",
            f"{prefixo}_MAT",
            f"{prefixo}_MAT_STATUS",
            "CHAVE_MERGE"
        ]
    ]

