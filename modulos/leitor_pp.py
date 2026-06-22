import pandas as pd
import zipfile

from io import BytesIO


# ==========================================================
# LEITOR PROVA PAULISTA
# ==========================================================

def ler_PP(

    arquivo,

    prefixo

):

    nome = arquivo.name.lower()

    # ======================================================
    # ZIP
    # ======================================================

    if nome.endswith(

        ".zip"

    ):

        with zipfile.ZipFile(

            arquivo

        ) as z:

            arquivos_excel = [

                arq

                for arq in z.namelist()

                if arq.lower().endswith(

                    (

                        ".xlsx",

                        ".xlsm"

                    )

                )

            ]

            if len(

                arquivos_excel

            ) == 0:

                raise Exception(

                    "Nenhum arquivo Excel encontrado dentro do ZIP."

                )

            excel = arquivos_excel[0]

            with z.open(

                excel

            ) as f:

                df = pd.read_excel(

                    BytesIO(

                        f.read()

                    )

                )

    # ======================================================
    # EXCEL
    # ======================================================

    else:

        df = pd.read_excel(

            arquivo

        )

    # ======================================================
    # PADRONIZAR NOMES
    # ======================================================

    df.columns = [

        str(col).upper().strip()

        for col in df.columns

    ]

    # ======================================================
    # CHAVE DE MERGE
    # ======================================================

    if (

        "RA" in df.columns

        and

        "TURMA" in df.columns

    ):

        df["CHAVE_MERGE"] = (

            df["RA"]

            .astype(str)

            .str.strip()

            +

            "_"

            +

            df["TURMA"]

            .astype(str)

            .str.strip()

        )

    # ======================================================
    # ACRESCENTAR PREFIXO
    # ======================================================

    colunas_fixas = [

        "RA",

        "NOME",

        "TURMA",

        "SERIE",

        "CHAVE_MERGE"

    ]

    novas_colunas = {}

    for coluna in df.columns:

        if coluna not in colunas_fixas:

            novas_colunas[coluna] = (

                prefixo

                +

                "_"

                +

                coluna

            )

    df.rename(

        columns=novas_colunas,

        inplace=True

    )

    return df
