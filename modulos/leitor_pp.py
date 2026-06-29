import os
import zipfile
from io import BytesIO

import pandas as pd


# ==========================================================
# CLASSIFICAÇÃO DA PROVA PAULISTA
# ==========================================================

def classificar_pp(valor):

    if pd.isna(valor):
        return ""

    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return ""

    # Caso venha em percentual (94.4)
    if valor > 1:
        valor /= 100

    if valor < 0.50:
        return "Abaixo do Básico"

    elif valor < 0.70:
        return "Básico"

    elif valor < 0.90:
        return "Adequado"

    return "Proficiente"


# ==========================================================
# NORMALIZA RA
# ==========================================================

def normalizar_ra(valor):

    if pd.isna(valor):
        return ""

    texto = str(valor).strip()

    # Remove ".0" quando o Excel converte para número
    if texto.endswith(".0"):
        texto = texto[:-2]

    # Mantém apenas os dígitos
    texto = "".join(
        c for c in texto
        if c.isdigit()
    )

    if texto == "":
        return ""

    return texto.zfill(12)

# ==========================================================
# NORMALIZA TURMA
# ==========================================================

def normalizar_turma(nome_arquivo):

    turma = os.path.splitext(
        os.path.basename(nome_arquivo)
    )[0]

    turma = (
        turma.upper()
        .replace("ª", "")
        .replace("º", "")
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )

    while "  " in turma:
        turma = turma.replace("  ", " ")

    remover = [
        "PROVA PAULISTA",
        "PP1",
        "PP2",
        "PP3",
        "1 BIMESTRE",
        "2 BIMESTRE",
        "3 BIMESTRE",
        "4 BIMESTRE"
    ]

    for texto in remover:
        turma = turma.replace(texto, "").strip()

    while "  " in turma:
        turma = turma.replace("  ", " ")

    return turma


# ==========================================================
# LEITURA DA PLANILHA
# ==========================================================

def ler_planilha(arquivo):

    bruto = pd.read_excel(
        arquivo,
        header=None
    )

    linha_cabecalho = None

    for i in range(min(15, len(bruto))):

        texto = " ".join(
            bruto.iloc[i]
            .fillna("")
            .astype(str)
            .tolist()
        ).upper()

        if (
            ("RA" in texto or "NR RA" in texto)
            and
            "NOME" in texto
        ):

            linha_cabecalho = i
            break

    if linha_cabecalho is None:

        raise ValueError(
            "Cabeçalho da Prova Paulista não encontrado."
        )

    arquivo.seek(0)

    df = pd.read_excel(
        arquivo,
        header=linha_cabecalho
    )

    df.columns = [
        str(coluna).strip()
        for coluna in df.columns
    ]

    return df

# ==========================================================
# LEITOR PRINCIPAL
# ==========================================================

def ler_PP(arquivo, prefixo):

    lista = []

    # ------------------------------------------------------
    # ARQUIVO ZIP
    # ------------------------------------------------------

    if arquivo.name.lower().endswith(".zip"):

    with zipfile.ZipFile(arquivo) as z:

        arquivos_excel = sorted(

            nome

            for nome in z.namelist()

            if (
                nome.lower().endswith(
                    (".xlsx", ".xlsm")
                )
                and
                not os.path.basename(nome).startswith("~$")
                and
                not os.path.basename(nome).startswith(".")
            )

        )

            for nome_excel in arquivos_excel:

    try:

        with z.open(nome_excel) as f:

            dados = BytesIO(f.read())

            df = ler_planilha(dados)

            df["TURMA"] = normalizar_turma(
                nome_excel
            )

            lista.append(df)

    except Exception as erro:

        print(
            f"[AVISO] Arquivo ignorado: "
            f"{nome_excel} ({erro})"
        )

    # ------------------------------------------------------
    # ARQUIVO EXCEL
    # ------------------------------------------------------

    else:

        df = ler_planilha(arquivo)

        df["TURMA"] = ""

        lista.append(df)

    # ------------------------------------------------------
    # NENHUM DADO
    # ------------------------------------------------------

    if len(lista) == 0:

        return pd.DataFrame()

    # ------------------------------------------------------
    # CONCATENAR
    # ------------------------------------------------------

    df = pd.concat(
        lista,
        ignore_index=True
    )

    # ------------------------------------------------------
    # PADRONIZAR NOMES DAS COLUNAS
    # ------------------------------------------------------

    df.columns = [

        str(c).strip().upper()

        for c in df.columns

    ]

# ------------------------------------------------------
# RENOMEAR COLUNAS
# ------------------------------------------------------

mapa = {}

for coluna in df.columns:

    nome = str(coluna).strip().upper()

    if "RA" in nome:
        mapa[coluna] = "RA"

    elif nome in [
        "NOME",
        "ESTUDANTE",
        "ALUNO"
    ]:
        mapa[coluna] = "NOME"

    elif nome in [
        "PORT",
        "LP",
        "LÍNGUA PORTUGUESA",
        "LINGUA PORTUGUESA"
    ]:
        mapa[coluna] = "PORT"

    elif nome in [
        "MAT",
        "MATEMÁTICA",
        "MATEMATICA"
    ]:
        mapa[coluna] = "MAT"

df.rename(
    columns=mapa,
    inplace=True
)

    # ------------------------------------------------------
    # GARANTIR COLUNAS
    # ------------------------------------------------------

    for coluna in [

        "RA",
        "NOME",
        "PORT",
        "MAT"

    ]:

        if coluna not in df.columns:

            df[coluna] = None

    # ------------------------------------------------------
    # NORMALIZAÇÃO
    # ------------------------------------------------------

    df["RA"] = df["RA"].apply(
        normalizar_ra
    )

    df["NOME"] = (
        df["NOME"]
        .astype(str)
        .str.strip()
    )

    df["TURMA"] = (
        df["TURMA"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # ------------------------------------------------------
    # CONVERTER NOTAS
    # ------------------------------------------------------

    df["PORT"] = pd.to_numeric(
        df["PORT"],
        errors="coerce"
    )

    df["MAT"] = pd.to_numeric(
        df["MAT"],
        errors="coerce"
    )

    # Caso venha em percentual (94,5)
    df.loc[df["PORT"] > 1, "PORT"] = (
        df.loc[df["PORT"] > 1, "PORT"] / 100
    )

    df.loc[df["MAT"] > 1, "MAT"] = (
        df.loc[df["MAT"] > 1, "MAT"] / 100
    )

    # ------------------------------------------------------
    # RESULTADOS
    # ------------------------------------------------------

    df[f"{prefixo}_LP"] = df["PORT"]

    df[f"{prefixo}_MAT"] = df["MAT"]

    df[f"{prefixo}_LP_STATUS"] = (
        df["PORT"]
        .apply(classificar_pp)
    )

    df[f"{prefixo}_MAT_STATUS"] = (
        df["MAT"]
        .apply(classificar_pp)
    )

    # ------------------------------------------------------
    # CHAVE
    # ------------------------------------------------------

    df["CHAVE_MERGE"] = (

        df["RA"]

        + "_"

        + df["TURMA"]

    )

    # ------------------------------------------------------
    # REMOVER DUPLICADOS
    # ------------------------------------------------------

    df = (

        df

        .drop_duplicates(
            subset="CHAVE_MERGE"
        )

        .reset_index(drop=True)

    )

    # ------------------------------------------------------
    # RETORNO
    # ------------------------------------------------------

    return df[

        [

            "RA",

            "NOME",

            "TURMA",

            f"{prefixo}_LP",

            f"{prefixo}_LP_STATUS",

            f"{prefixo}_MAT",

            f"{prefixo}_MAT_STATUS",

            "CHAVE_MERGE"

        ]

    ]

