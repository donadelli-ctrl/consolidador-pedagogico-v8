# ==========================================================
# LIMPEZA DA BASE
# ==========================================================

def limpar_base(base):

    # ------------------------------------------------------
    # REMOVER COLUNAS DUPLICADAS
    # ------------------------------------------------------

    base = base.loc[
        :,
        ~base.columns.duplicated()
    ]

    # ------------------------------------------------------
    # REMOVER COLUNAS _X E _Y
    # ------------------------------------------------------

    colunas_remover = [

        coluna

        for coluna in base.columns

        if (

            coluna.endswith("_x")

            or

            coluna.endswith("_y")

        )

    ]

    base = base.drop(

        columns=colunas_remover,

        errors="ignore"

    )

    # ------------------------------------------------------
    # ORDENAÇÃO
    # ------------------------------------------------------

    if (

        "TURMA_PAD" in base.columns

        and

        "NOME" in base.columns

    ):

        base = (

            base

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

    else:

        base.reset_index(

            drop=True,

            inplace=True

        )

    return base
