import pandas as pd


# ==========================================================
# PARTICIPAÇÃO
# ==========================================================

def calcular_participacao(base):

    colunas = [

        "ADE_LP",

        "PP1_LP_STATUS",

        "PP2_LP_STATUS",

        "ADP_LP_STATUS",

        "PP3_LP_STATUS"

    ]

    for coluna in colunas:

        nome = "PART_" + coluna.split("_")[0]

        if coluna in base.columns:

            base[nome] = (

                base[coluna]

                .notna()

            )

        else:

            base[nome] = False

    base["TOTAL_PARTICIPACOES"] = (

          base["PART_ADE"].astype(int)

        + base["PART_PP1"].astype(int)

        + base["PART_PP2"].astype(int)

        + base["PART_ADP"].astype(int)

        + base["PART_PP3"].astype(int)

    )

    return base


# ==========================================================
# BAIXA PARTICIPAÇÃO
# ==========================================================

def obter_sem_participacao(base):

    sem_participacao = (

        base

        [

            base["TOTAL_PARTICIPACOES"] < 3

        ]

        .copy()

    )

    sem_participacao = (

        sem_participacao

        .sort_values(

            [

                "TURMA_PAD",

                "NOME"

            ]

        )

        .reset_index(

            drop=True

        )

    )

    return sem_participacao
