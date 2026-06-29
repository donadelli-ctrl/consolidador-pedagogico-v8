import re
import unicodedata


# ==========================================================
# PADRONIZAR NOME
# ==========================================================

def padronizar_nome(nome):

    if nome is None:
        return ""

    nome = str(nome).upper().strip()

    nome = "".join(
        c
        for c in unicodedata.normalize("NFD", nome)
        if unicodedata.category(c) != "Mn"
    )

    nome = re.sub(r"\s+", " ", nome)

    return nome


# ==========================================================
# PADRONIZAR TURMA
# ==========================================================

def padronizar_turma(turma):

    if turma is None:
        return ""

    turma = padronizar_nome(turma)

    # Remove cópias do Windows
    turma = re.sub(r"\(\d+\)", "", turma)

    # Remove símbolos
    turma = turma.replace("º", "")
    turma = turma.replace("ª", "")
    turma = turma.replace("-", " ")

    turma = " ".join(turma.split())

    # ------------------------------------------------------
    # ENSINO FUNDAMENTAL
    # ------------------------------------------------------

    m = re.search(r"([6-9]).*ANO.*([A-Z])", turma)

    if m:

        return f"{m.group(1)}{m.group(2)}"

    # ------------------------------------------------------
    # ENSINO MÉDIO
    # ------------------------------------------------------

    m = re.search(r"([1-3]).*SERIE.*([A-Z])", turma)

    if m:

        codigo = f"{m.group(1)}{m.group(2)}"

    else:

        m = re.search(r"^([1-9])([A-Z])", turma)

        if m:

            codigo = f"{m.group(1)}{m.group(2)}"

        else:

            codigo = turma

    # ------------------------------------------------------
    # CURSOS
    # ------------------------------------------------------

    if "ADMIN" in turma:

        codigo += " ADM"

    elif "LOG" in turma:

        codigo += " LOG"

    elif "AGRO" in turma:

        codigo += " AGRO"

    elif "ENF" in turma:

        codigo += " ENF"

    elif "DESENVOLVIMENTO" in turma or " DS" in turma:

        codigo += " DS"

    elif "VEND" in turma:

        codigo += " VEND"

    return codigo.strip()
