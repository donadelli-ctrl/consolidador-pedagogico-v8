# ==========================================================
# PRIORITÁRIOS
# ==========================================================

def definir_prioridade(

    status_lp,

    status_mat

):

    lp_ab = (

        status_lp

        ==

        "Abaixo do Básico"

    )

    mat_ab = (

        status_mat

        ==

        "Abaixo do Básico"

    )

    if (

        lp_ab

        and

        mat_ab

    ):

        return "LP + MAT"

    elif lp_ab:

        return "LP"

    elif mat_ab:

        return "MAT"

    return None


# ==========================================================
# FILTRO
# ==========================================================

def obter_prioritarios(

    base,

    coluna_lp,

    coluna_mat

):

    base["PRIORIDADE"] = (

        base

        .apply(

            lambda x:

            definir_prioridade(

                x[coluna_lp],

                x[coluna_mat]

            ),

            axis=1

        )

    )

    prioritarios = (

        base

        [

            base["PRIORIDADE"]

            .notna()

        ]

        .copy()

    )

    prioritarios = (

        prioritarios

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

    return prioritarios
