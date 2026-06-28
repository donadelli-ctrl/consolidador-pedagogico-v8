import pandas as pd


# ==========================================================
# RESUMO POR TURMA
# ==========================================================

def gerar_resumo_por_turma(

    base,

    prioritarios

):

    # ------------------------------------------------------
    # TURMA
    # ------------------------------------------------------

    coluna_turma = "TURMA_PAD"

    if coluna_turma not in base.columns:

        coluna_turma = "TURMA"

    # ------------------------------------------------------
    # GARANTIR SITUAÇÃO
    # ------------------------------------------------------

    if "SITUACAO" not in base.columns:

        base["SITUACAO"] = ""

    # ------------------------------------------------------
    # RESUMO
    # ------------------------------------------------------

    resumo = (

        base

        .groupby(

            coluna_turma

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

        base[

            base["SITUACAO"] == "Atenção"

        ]

        .groupby(

            coluna_turma

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

        base[

            base["SITUACAO"] == "Acompanhamento"

        ]

        .groupby(

            coluna_turma

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

        base[

            base["SITUACAO"] == "Adequado"

        ]

        .groupby(

            coluna_turma

        )

        .size()

        .reset_index(

            name="ADEQUADO"

        )

    )

    # ------------------------------------------------------
    # PRIORITÁRIOS
    # ------------------------------------------------------

    if coluna_turma not in prioritarios.columns:

        prioritarios[coluna_turma] = ""

    prioridade = (

        prioritarios

        .groupby(

            coluna_turma

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

            on=coluna_turma,

            how="left"

        )

        .merge(

            acompanhamento,

            on=coluna_turma,

            how="left"

        )

        .merge(

            adequado,

            on=coluna_turma,

            how="left"

        )

        .merge(

            prioridade,

            on=coluna_turma,

            how="left"

        )

        .fillna(

            0

        )

    )

    resumo["PERC_PRIORITARIOS"] = (

        resumo["PRIORITARIOS"]

        .div(

            resumo["ESTUDANTES"]

        )

        .fillna(0)

        * 100

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

    if "SITUACAO" not in base.columns:

        base["SITUACAO"] = ""

    coluna_turma = "TURMA_PAD"

    if coluna_turma not in base.columns:

        coluna_turma = "TURMA"

    painel = pd.DataFrame({

        "INDICADOR":[

            "Total de estudantes",

            "Total de turmas",

            "Estudantes em Atenção",

            "Estudantes em Acompanhamento",

            "Estudantes Adequados"

        ],

        "QUANTIDADE":[

            len(base),

            base[coluna_turma].nunique(),

            (base["SITUACAO"]=="Atenção").sum(),

            (base["SITUACAO"]=="Acompanhamento").sum(),

            (base["SITUACAO"]=="Adequado").sum()

        ]

    })

    return painel
