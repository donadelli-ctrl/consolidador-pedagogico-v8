import os
import zipfile
from io import BytesIO

import pandas as pd


# ==========================================================
# CLASSIFICAÇÃO PROVA PAULISTA
# ==========================================================

def classificar_pp(valor):

    if pd.isna(valor):
        return ""

    try:
        valor = float(valor)

    except:
        return ""

    if valor < 0.50:
        return "Abaixo do Básico"

    elif valor < 0.70:
        return "Básico"

    elif valor < 0.90:
        return "Adequado"

    else:
        return "Proficiente"


# ==========================================================
# LEITOR PROVA PAULISTA
# ==========================================================

def ler_PP(arquivo, prefixo):

    lista_df = []

    # ======================================================
    # ZIP
    # ======================================================

    if arquivo.name.lower().endswith(".zip"):

        with zipfile.ZipFile(arquivo) as z:

            arquivos_excel = [

                arq

                for arq in z.namelist()

                if arq.lower().endswith(

                    (".xlsx", ".xlsm")

                )

            ]

            if len(arquivos_excel) == 0:

                raise Exception(

                    "Nenhum Excel encontrado dentro do ZIP."

                )

            for excel in arquivos_excel:

                with z.open(excel) as f:

                    df = pd.read_excel(

                        BytesIO(

                            f.read()

                        )

                    )

                    # -----------------------------
                    # TURMA = NOME DO ARQUIVO
                    # -----------------------------

                    turma = os.path.splitext(

                        os.path.basename(excel)

                    )[0].strip()

                    df["TURMA"] = turma

                    lista_df.append(df)

    else:

        df = pd.read_excel(arquivo)

        df["TURMA"] = ""

        lista_df.append(df)

    # ======================================================
    # JUNTAR TODAS AS TURMAS
    # ======================================================

    df = pd.concat(

        lista_df,

        ignore_index=True

    )

    # ======================================================
    # PADRONIZAR COLUNAS
    # ======================================================

    df.columns = [

        str(col).strip()

        for col in df.columns

    ]

    # ======================================================
    # RENOMEAR
    # ======================================================

    renomear = {

        "NR RA": "RA",

        "Nome": "NOME"

    }

    df.rename(

        columns=renomear,

        inplace=True

    )

    # ======================================================
    # GARANTIR COLUNAS
    # ======================================================

    obrigatorias = [

        "RA",

        "NOME",

        "TURMA",

        "PORT",

        "MAT"

    ]

    for coluna in obrigatorias:

        if coluna not in df.columns:

            df[coluna] = None

    # ======================================================
    # CONVERTER PARA NÚMERO
    # ======================================================

    df["PORT"] = pd.to_numeric(

        df["PORT"],

        errors="coerce"

    )

    df["MAT"] = pd.to_numeric(

        df["MAT"],

        errors="coerce"

    )

    # ======================================================
    # PERCENTUAIS
    # ======================================================

    df[f"{prefixo}_LP"] = df["PORT"]

    df[f"{prefixo}_MAT"] = df["MAT"]

    # ======================================================
    # STATUS
    # ======================================================

    df[f"{prefixo}_LP_STATUS"] = (

        df["PORT"]

        .apply(

            classificar_pp

        )

    )

    df[f"{prefixo}_MAT_STATUS"] = (

        df["MAT"]

        .apply(

            classificar_pp

        )

    )

    # ======================================================
    # LIMPEZA
    # ======================================================

    df["RA"] = (

        df["RA"]

        .astype(str)

        .str.strip()

    )

    df["NOME"] = (

        df["NOME"]

        .astype(str)

        .str.strip()

    )

    df["TURMA"] = (

        df["TURMA"]

        .astype(str)

        .str.strip()

    )

    # ======================================================
    # CHAVE
    # ======================================================

    df["CHAVE_MERGE"] = (

        df["RA"]

        +

        "_"

        +

        df["TURMA"]

    )

    # ======================================================
    # RETORNO
    # ======================================================

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
