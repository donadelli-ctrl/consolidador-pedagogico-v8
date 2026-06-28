# ==========================================================
# PRIORITÁRIOS
# ==========================================================

def definir_prioridade(

    status_lp,

    status_mat

):

    status_lp = str(status_lp).strip().upper()
    status_mat = str(status_mat).strip().upper()

    lp_ab = (

        status_lp

        ==

        "ABAIXO DO BÁSICO".upper()

    )

    mat_ab = (

        status_mat

        ==

        "ABAIXO DO BÁSICO".upper()

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

    # ------------------------------------------------------
    # GARANTIR EXISTÊNCIA DAS COLUNAS
    # ------------------------------------------------------

    if coluna_lp not in base.columns:

        base[coluna_lp] = ""

    if coluna_mat not in base.columns:

        base[coluna_mat] = ""

    # ------------------------------------------------------
    # PRIORIDADE
    # ------------------------------------------------------

    base["PRIORIDADE"] = (

        base.apply(

            lambda x:

            definir_prioridade(

                x[coluna_lp],

                x[coluna_mat]

            ),

            axis=1

        )

    )

    prioritarios = (

        base[

            base["PRIORIDADE"].notna()

        ]

        .copy()

    )

    # ------------------------------------------------------
    # ORDENAÇÃO
    # ------------------------------------------------------

    colunas_ordem = []

    if "TURMA_PAD" in prioritarios.columns:

        colunas_ordem.append(

            "TURMA_PAD"

        )

    elif "TURMA" in prioritarios.columns:

        colunas_ordem.append(

            "TURMA"

        )

    if "NOME" in prioritarios.columns:

        colunas_ordem.append(

            "NOME"

        )

    if len(colunas_ordem) > 0:

        prioritarios = (

            prioritarios

            .sort_values(

                colunas_ordem

            )

            .reset_index(

                drop=True

            )

        )

    else:

        prioritarios.reset_index(

            drop=True,

            inplace=True

        )

    return prioritarios
