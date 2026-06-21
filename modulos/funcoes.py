import pandas as pd
import unicodedata
import re


# ==========================================================
# NORMALIZAR TEXTO
# ==========================================================

def normalizar_texto(texto):

    if pd.isna(texto):
        return ""

    texto = str(texto).upper().strip()

    texto = ''.join(

        c

        for c in unicodedata.normalize(

            "NFD",

            texto

        )

        if unicodedata.category(c) != "Mn"

    )

    texto = re.sub(

        r"\s+",

        " ",

        texto

    )

    return texto
