import pandas as pd

from modulos.funcoes import (

    padronizar_turma,

    criar_chave,

    definir_status

)


# ==========================================================
# LEITOR UNIVERSAL DAS PROVAS PAULISTAS
# ==========================================================

def ler_PP(caminho, prefixo):

    df = pd.read_excel(caminho)

    df.columns = [

        str(col).strip()

        for col in df.columns

    ]

    df = df[

        df["Nome"].notna()

    ].copy()

    df = df[

        ~

        df["Nome"]

        .astype(str)

        .str.upper()

        .str.contains(

            "TOTAL|FILTROS APLICADOS",

            na=False

        )

    ]

    temp = pd.DataFrame()

    temp["RA"] = df["NR RA"]

    temp["NOME"] = df["Nome"]

    temp["TURMA"] = ""

    temp[f"{prefixo}_MAT"] = df["MAT"]

    temp[f"{prefixo}_LP"] = df["PORT"]

    temp[f"{prefixo}_MAT_STATUS"] = (

        temp[f"{prefixo}_MAT"]

        .apply(

            definir_status

        )

    )

    temp[f"{prefixo}_LP_STATUS"] = (

        temp[f"{prefixo}_LP"]

        .apply(

            definir_status

        )

    )

    temp["TURMA_PAD"] = (

        temp["TURMA"]

        .apply(

            padronizar_turma

        )

    )

    temp["CHAVE_MERGE"] = (

        temp.apply(

            lambda x:

            criar_chave(

                x["NOME"],

                x["TURMA"]

            ),

            axis=1

        )

    )

    return temp
