import pandas as pd


# ==========================================================
# RESUMO POR TURMA
# ==========================================================

def gerar_resumo_por_turma(

    base,

    prioritarios

):

    resumo = (

        base

        .groupby(

            "TURMA_PAD"

        )

        .size()

        .reset_index(

            name="ESTUDANTES"

        )

    )

    # ------------------------------------------------------
    # ATENÇÃO
    # ------------------------------------------------------

    atencao = (

        base

        [

            base["SITUACAO"]

            ==

            "Atenção"

        ]

        .groupby(

            "TURMA_PAD"

        )

        .size()

        .reset_index(

            name="ATENCAO"

        )

    )

    # ------------------------------------------------------
    # ACOMPANHAMENTO
    # ------------------------------------------------------

    acompanhamento = (

        base

        [

            base["SITUACAO"]

            ==

            "Acompanhamento"

        ]

        .groupby(

            "TURMA_PAD"

        )

        .size()

        .reset_index(

            name="ACOMPANHAMENTO"

        )

    )

    # ------------------------------------------------------
    # ADEQUADO
    # ------------------------------------------------------

    adequado = (

        base

        [

            base["SITUACAO"]

            ==

            "Adequado"

        ]

        .groupby(

            "TURMA_PAD"

        )

        .size()

        .reset_index(

            name="ADEQUADO"

        )

    )

    # ------------------------------------------------------
    # PRIORITÁRIOS
    # ------------------------------------------------------

    prioridade = (

        prioritarios

        .groupby(

            "TURMA_PAD"

        )

        .size()

        .reset_index(

            name="PRIORITARIOS"

        )

    )

    resumo = (

        resumo

        .merge(

            atencao,

            on="TURMA_PAD",

            how="left"

        )

        .merge(

            acompanhamento,

            on="TURMA_PAD",

            how="left"

        )

        .merge(

            adequado,

            on="TURMA_PAD",

            how="left"

        )

        .merge(

            prioridade,

            on="TURMA_PAD",

            how="left"

        )

        .fillna(

            0

        )

    )

    resumo["PERC_PRIORITARIOS"] = (

        100

        *

        resumo["PRIORITARIOS"]

        /

        resumo["ESTUDANTES"]

    ).round(

        1

    )

    return resumo


# ==========================================================
# PAINEL ESCOLA
# ==========================================================

def gerar_painel_escola(

    base,

    resumo

):

    painel = pd.DataFrame({

        "INDICADOR":[

            "Total de estudantes",

            "Total de turmas",

            "Estudantes em Atenção",

            "Estudantes em Acompanhamento",

            "Estudantes Adequados"

        ],

        "QUANTIDADE":[

            len(

                base

            ),

            base[

                "TURMA_PAD"

            ].nunique(),

            (

                base["SITUACAO"]

                ==

                "Atenção"

            ).sum(),

            (

                base["SITUACAO"]

                ==

                "Acompanhamento"

            ).sum(),

            (

                base["SITUACAO"]

                ==

                "Adequado"

            ).sum()

        ]

    })

    return painel
