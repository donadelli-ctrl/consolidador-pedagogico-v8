# ==========================================================
# ORDEM DOS NÍVEIS
# ==========================================================

ordem_niveis = {

    "Abaixo do Básico": 1,

    "Básico": 2,

    "Adequado": 3,

    "Proficiente": 4

}


# ==========================================================
# EVOLUÇÃO ENTRE DOIS NÍVEIS
# ==========================================================

def calcular_evolucao(

    nivel_inicial,

    nivel_final

):

    if (

        nivel_inicial not in ordem_niveis

        or

        nivel_final not in ordem_niveis

    ):

        return "Sem Comparação"

    valor_inicial = ordem_niveis[nivel_inicial]

    valor_final = ordem_niveis[nivel_final]

    if valor_final > valor_inicial:

        return "Melhorou"

    elif valor_final < valor_inicial:

        return "Piorou"

    else:

        return "Manteve"


# ==========================================================
# SITUAÇÃO FINAL
# ==========================================================

def definir_situacao(

    status_lp,

    status_mat

):

    bons_niveis = [

        "Adequado",

        "Proficiente"

    ]

    if (

        status_lp in bons_niveis

        and

        status_mat in bons_niveis

    ):

        return "Adequado"

    elif (

        status_lp == "Ausente"

        or

        status_mat == "Ausente"

    ):

        return "Acompanhamento"

    else:

        return "Atenção"


# ==========================================================
# GERAR EVOLUÇÃO
# ==========================================================

def gerar_evolucao(

    base

):

    df = base.copy()

    # ------------------------------------------------------
    # LP
    # ------------------------------------------------------

    coluna_lp_final = "PP2_LP_STATUS"

    if "PP3_LP_STATUS" in df.columns:

        coluna_lp_final = "PP3_LP_STATUS"

    df["EVOL_LP"] = (

        df

        .apply(

            lambda x:

            calcular_evolucao(

                x["ADE_LP"],

                x[coluna_lp_final]

            ),

            axis=1

        )

    )

    # ------------------------------------------------------
    # MAT
    # ------------------------------------------------------

    coluna_mat_final = "PP2_MAT_STATUS"

    if "PP3_MAT_STATUS" in df.columns:

        coluna_mat_final = "PP3_MAT_STATUS"

    df["EVOL_MAT"] = (

        df

        .apply(

            lambda x:

            calcular_evolucao(

                x["ADE_MAT"],

                x[coluna_mat_final]

            ),

            axis=1

        )

    )

    # ------------------------------------------------------
    # SITUAÇÃO
    # ------------------------------------------------------

    df["SITUACAO"] = (

        df

        .apply(

            lambda x:

            definir_situacao(

                x[coluna_lp_final],

                x[coluna_mat_final]

            ),

            axis=1

        )

    )

    evolucao = (

        df

        [

            [

                "TURMA_PAD",

                "NOME",

                "EVOL_LP",

                "EVOL_MAT",

                "SITUACAO"

            ]

        ]

        .copy()

    )

    evolucao.columns = [

        "TURMA",

        "NOME",

        "EVOL LP",

        "EVOL MAT",

        "SITUAÇÃO"

    ]

    return evolucao
