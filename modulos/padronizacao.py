import re
import unicodedata


# ==========================================================
# PADRONIZAR NOME
# ==========================================================

def padronizar_nome(nome):

    if nome is None:
        return ""

    nome = str(nome).upper().strip()

    # Remove acentos
    nome = "".join(
        c
        for c in unicodedata.normalize("NFD", nome)
        if unicodedata.category(c) != "Mn"
    )

    # Remove espaços duplicados
    nome = re.sub(r"\s+", " ", nome)

    return nome


# ==========================================================
# PADRONIZAR TURMA
# ==========================================================

def padronizar_turma(turma):

    if turma is None:
        return ""

    turma = str(turma).upper().strip()

    turma = turma.replace(" ", "")
    turma = turma.replace("º", "")
    turma = turma.replace("°", "")
    turma = turma.replace("ª", "")
    turma = turma.replace("-", "")

    turma = re.sub(r"[^A-Z0-9]", "", turma)

    return turma
