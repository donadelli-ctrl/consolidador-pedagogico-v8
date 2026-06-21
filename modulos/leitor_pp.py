import pandas as pd


# ==========================================================
# LEITOR UNIVERSAL DAS PROVAS PAULISTAS
# ==========================================================

def ler_PP(caminho):

    df = pd.read_excel(caminho)

    return df
