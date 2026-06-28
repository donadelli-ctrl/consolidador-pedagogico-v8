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

                .fillna("")

                .astype(str)

                .str.strip()

                != ""

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

        base[

            base["TOTAL_PARTICIPACOES"] < 3

        ]

        .copy()

    )

    # ------------------------------------------------------
    # ORDENAÇÃO
    # ------------------------------------------------------

    colunas_ordem = []

    if "TURMA_PAD" in sem_participacao.columns:

        colunas_ordem.append(

            "TURMA_PAD"

        )

    elif "TURMA" in sem_participacao.columns:

        colunas_ordem.append(

            "TURMA"

        )

    if "NOME" in sem_participacao.columns:

        colunas_ordem.append(

            "NOME"

        )

    if len(colunas_ordem) > 0:

        sem_participacao = (

            sem_participacao

            .sort_values(

                colunas_ordem

            )

            .reset_index(

                drop=True

            )

        )

    else:

        sem_participacao.reset_index(

            drop=True,

            inplace=True

        )

    return sem_participacao
