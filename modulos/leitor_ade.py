import pandas as pd

from modulos.funcoes import (

    padronizar_turma,

    criar_chave

)


# ==========================================================
# LEITOR ADE
# ==========================================================

def ler_ADE(caminho):

    df = pd.read_excel(caminho)

    df.columns = [

        str(col).strip()

        for col in df.columns

    ]

    temp = pd.DataFrame()

    temp["RA"] = df["Id"]

    temp["NOME"] = df["ESTUDANTE"]

    temp["TURMA"] = df["TURMA"]

    temp["ADE_LP"] = df["Status"]

    temp["ADE_MAT"] = df["Status.1"]

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
