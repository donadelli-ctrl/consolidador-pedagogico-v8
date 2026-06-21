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
    # COLUNAS X E Y
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
    # ORDENAR
    # ------------------------------------------------------

    if "TURMA_PAD" in base.columns:

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

    return base
