import pandas as pd
import zipfile

from io import BytesIO

from modulos.padronizacao import padronizar_turma


# ==========================================================
# LEITOR AVD / AVDE / ADP
# ==========================================================

def ler_ADE(arquivo):

    lista_df = []

    # ======================================================
    # LEITURA ZIP
    # ======================================================

    if arquivo.name.lower().endswith(".zip"):

        with zipfile.ZipFile(arquivo) as z:

            arquivos_excel = [

                arq

                for arq in z.namelist()

                if arq.lower().endswith((".xlsx", ".xlsm"))

            ]

            if len(arquivos_excel) == 0:

                raise Exception("Nenhum arquivo Excel encontrado no ZIP.")

            for excel in arquivos_excel:

                with z.open(excel) as f:

                    df = pd.read_excel(BytesIO(f.read()))

                    lista_df.append(df)

    else:

        lista_df.append(pd.read_excel(arquivo))

    # ======================================================
    # UNIR TODAS AS TURMAS
    # ======================================================

    df = pd.concat(lista_df, ignore_index=True)

    # ======================================================
    # PADRONIZAR NOMES DAS COLUNAS
    # ======================================================

    df.columns = [

        str(col).strip()

        for col in df.columns

    ]

    # ======================================================
    # RENOMEAR
    # ======================================================

    renomear = {

        "Id": "RA",
        "Id ": "RA",
        "ESTUDANTE": "NOME",
        "TURMA": "TURMA",
        "Status": "ADE_LP",
        "Status.1": "ADE_MAT"

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
        "ADE_LP",
        "ADE_MAT"

    ]

    for coluna in obrigatorias:

        if coluna not in df.columns:

            df[coluna] = ""

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

        .apply(padronizar_turma)

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
            "ADE_LP",
            "ADE_MAT",
            "CHAVE_MERGE"

        ]

    ]
