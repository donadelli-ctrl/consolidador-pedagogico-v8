import os
import zipfile
from io import BytesIO

import pandas as pd


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

                if arq.lower().endswith((".xlsx", ".xlsm"))

            ]

            if not arquivos_excel:

                raise Exception("Nenhum arquivo Excel encontrado dentro do ZIP.")

            for excel in arquivos_excel:

                with z.open(excel) as f:

                    df = pd.read_excel(BytesIO(f.read()))

                    # --------------------------------------
                    # TURMA = NOME DO ARQUIVO
                    # --------------------------------------

                    turma = os.path.splitext(
                        os.path.basename(excel)
                    )[0].strip()

                    df["TURMA"] = turma

                    lista_df.append(df)

    # ======================================================
    # EXCEL
    # ======================================================

    else:

        df = pd.read_excel(arquivo)

        df["TURMA"] = ""

        lista_df.append(df)

    # ======================================================
    # UNIR TODAS AS TURMAS
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
    # RENOMEAR COLUNAS
    # ======================================================

    renomear = {

        "NR RA": "RA",

        "Nome": "NOME",

        "PORT": f"{prefixo}_LP_STATUS",

        "MAT": f"{prefixo}_MAT_STATUS"

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

        f"{prefixo}_LP_STATUS",

        f"{prefixo}_MAT_STATUS"

    ]

    for coluna in obrigatorias:

        if coluna not in df.columns:

            df[coluna] = ""

    # ======================================================
    # LIMPEZA
    # ======================================================

    df["RA"] = df["RA"].astype(str).str.strip()

    df["NOME"] = df["NOME"].astype(str).str.strip()

    df["TURMA"] = df["TURMA"].astype(str).str.strip()

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

            f"{prefixo}_LP_STATUS",

            f"{prefixo}_MAT_STATUS",

            "CHAVE_MERGE"

        ]

    ]
