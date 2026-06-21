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
# EVOLUÇÃO
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
