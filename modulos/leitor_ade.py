import pandas as pd


# ==========================================================
# LEITOR DA ADE
# ==========================================================

def ler_ADE(caminho):

    df = pd.read_excel(caminho)

    return df
