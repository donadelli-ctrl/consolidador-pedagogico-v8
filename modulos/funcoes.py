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


# ==========================================================
# PADRONIZAR TURMAS
# ==========================================================

def padronizar_turma(turma):

    turma = normalizar_texto(turma)

    m = re.search(

        r"([1-9])[^A-Z]*([A-Z])",

        turma

    )

    if m:

        serie = m.group(1)

        letra = m.group(2)

        return f"{serie}{letra}"

    return ""


# ==========================================================
# CHAVE DE MERGE
# ==========================================================

def criar_chave(nome, turma):

    return (

        normalizar_texto(nome)

        +

        "_"

        +

        padronizar_turma(turma)

    )


# ==========================================================
# CLASSIFICAÇÃO
# ==========================================================

def definir_status(valor):

    if pd.isna(valor):

        return "Ausente"

    elif valor < 0.50:

        return "Abaixo do Básico"

    elif valor < 0.70:

        return "Básico"

    elif valor < 0.90:

        return "Adequado"

    else:

        return "Proficiente"
