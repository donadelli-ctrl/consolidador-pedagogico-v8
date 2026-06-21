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

    turma_pad = ""

    # Ensino Médio

    m = re.search(

        r'([1-3]).*SERIE\s+([A-Z])',

        turma

    )

    # Ensino Fundamental

    if m is None:

        m = re.search(

            r'([6-9]).*ANO\s+([A-Z])',

            turma

        )

    # Formato direto

    if m is None:

        m = re.search(

            r'^([1-9])([A-Z])',

            turma

        )

    if m:

        serie = m.group(1)

        letra = m.group(2)

        turma_pad = f"{serie}{letra}"

    else:

        turma_pad = ""

    # Cursos técnicos

    if (

        "ADMINISTRACAO" in turma

        or

        " ADM" in turma

    ):

        turma_pad += " ADM"

    elif (

        "LOGISTICA" in turma

        or

        " LOG" in turma

    ):

        turma_pad += " LOG"

    elif (

        "DESENVOLVIMENTO DE SISTEMAS" in turma

        or

        " DS" in turma

    ):

        turma_pad += " DS"

    elif (

        "ENFERMAGEM" in turma

        or

        " ENF" in turma

    ):

        turma_pad += " ENF"

    elif (

        "AGRONEGOCIO" in turma

        or

        " AGRO" in turma

    ):

        turma_pad += " AGRO"

    elif (

        "VENDAS" in turma

        or

        " VEND" in turma

    ):

        turma_pad += " VEND"

    return turma_pad.strip()


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
# CLASSIFICAÇÃO PROVA PAULISTA
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


# ==========================================================
# ORDEM DOS NÍVEIS
# ==========================================================

ordem_niveis = {

    "Abaixo do Básico":1,

    "Básico":2,

    "Adequado":3,

    "Proficiente":4

}
