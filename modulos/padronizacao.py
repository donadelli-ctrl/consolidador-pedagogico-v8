import re


# ==========================================================
# PADRONIZAR TURMA
# ==========================================================

def padronizar_turma(turma):

    if turma is None:
        return ""

    turma = str(turma).upper().strip()

    # remover espaços
    turma = turma.replace(" ", "")

    # remover º ª °
    turma = turma.replace("º", "")
    turma = turma.replace("°", "")
    turma = turma.replace("ª", "")

    # remover hífen
    turma = turma.replace("-", "")

    # remover qualquer caractere estranho
    turma = re.sub(r"[^A-Z0-9]", "", turma)

    return turma
