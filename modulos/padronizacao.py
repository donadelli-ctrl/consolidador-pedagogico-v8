# ==========================================================
# PADRONIZAÇÃO
# Consolidador Pedagógico MVP
# ==========================================================

import re
import pandas as pd


# ==========================================================
# NORMALIZA RA
# ==========================================================

def normalizar_ra(valor):
    """
    Normaliza o RA do estudante.

    Exemplos
    --------
    351234567.0      -> 351234567
    "351234567"      -> 351234567
    "351.234.567"    -> 351234567
    NaN              -> ""
    """

    if pd.isna(valor):
        return ""

    texto = str(valor).strip()

    if texto.endswith(".0"):
        texto = texto[:-2]

    texto = "".join(c for c in texto if c.isdigit())

    return texto


# ==========================================================
# PADRONIZA NOME
# ==========================================================

def padronizar_nome(nome):
    """
    Padroniza o nome do estudante.
    """

    if pd.isna(nome):
        return ""

    nome = str(nome).upper().strip()

    nome = re.sub(r"\s+", " ", nome)

    return nome

# ==========================================================
# PADRONIZA TURMA
# ==========================================================

def padronizar_turma(turma):
    """
    Padroniza o nome da turma.

    Exemplos:
        6º Ano A                -> 6A
        7 Ano B                 -> 7B
        1ª Série A              -> 1A
        2A Administração         -> 2A ADM
        2A Desenvolvimento de Sistemas -> 2A DS
        3B Agronegócio          -> 3B AGRO
        3C Enfermagem           -> 3C ENF
        2B Logística            -> 2B LOG
        3A Vendas               -> 3A VEND
    """

    if pd.isna(turma):
        return ""

    turma = str(turma).upper().strip()

    turma = turma.replace("º", "")
    turma = turma.replace("ª", "")
    turma = re.sub(r"\s+", " ", turma)

    # Cursos técnicos
    substituicoes = {
        "ADMINISTRACAO": "ADM",
        "ADMINISTRAÇÃO": "ADM",
        "DESENVOLVIMENTO DE SISTEMAS": "DS",
        "AGRONEGOCIO": "AGRO",
        "AGRONEGÓCIO": "AGRO",
        "LOGISTICA": "LOG",
        "LOGÍSTICA": "LOG",
        "ENFERMAGEM": "ENF",
        "VENDAS": "VEND"
    }

    for origem, destino in substituicoes.items():
        turma = turma.replace(origem, destino)

    # Remove palavras desnecessárias
    turma = turma.replace("ANO", "")
    turma = turma.replace("SÉRIE", "")
    turma = turma.replace("SERIE", "")

    turma = re.sub(r"\s+", " ", turma).strip()

        # Junta número + letra (6 A -> 6A)
    turma = re.sub(r"^(\d)\s+([A-Z])", r"\1\2", turma)

    # Padroniza espaço antes da sigla do curso
    turma = turma.replace("ADM", " ADM")
    turma = turma.replace("DS", " DS")
    turma = turma.replace("LOG", " LOG")
    turma = turma.replace("AGRO", " AGRO")
    turma = turma.replace("ENF", " ENF")
    turma = turma.replace("VEND", " VEND")

    turma = re.sub(r"\s+", " ", turma)

    turma = turma.strip()

    return turma


# ==========================================================
# EXTRAI SÉRIE
# ==========================================================

def extrair_serie(turma):
    """
    Retorna:
        EF -> 6º ao 9º ano
        EM -> 1ª à 3ª série
    """

    turma = padronizar_turma(turma)

    if turma.startswith(("6", "7", "8", "9")):
        return "EF"

    if turma.startswith(("1", "2", "3")):
        return "EM"

    return ""

# ==========================================================
# CRIA CHAVE DE MERGE
# ==========================================================

def criar_chave_merge(ra, nome, turma):
    """
    Cria uma chave única para identificar o estudante.

    Prioridade:
        1. RA + TURMA
        2. NOME + TURMA (quando RA estiver vazio)
    """

    ra = normalizar_ra(ra)
    nome = padronizar_nome(nome)
    turma = padronizar_turma(turma)

    if ra:
        return f"{ra}_{turma}"

        if nome and turma:
        return f"{nome}_{turma}"

    return ""
    

# ==========================================================
# FIM DO MÓDULO
# ==========================================================

