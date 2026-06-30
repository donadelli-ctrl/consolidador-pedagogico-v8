import os
import zipfile
from io import BytesIO

import pandas as pd

from modulos.padronizacao import (
    padronizar_nome,
    padronizar_turma
)


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

    return texto

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

# ==========================================================
# LEITURA DA PLANILHA
# ==========================================================

def ler_planilha(arquivo):
    """
    Localiza automaticamente a linha de cabeçalho da planilha da
    Prova Paulista e devolve um DataFrame já com os nomes das
    colunas limpos.
    """

    # ------------------------------------------------------
    # Lê toda a planilha sem assumir cabeçalho
    # ------------------------------------------------------

    bruto = pd.read_excel(
        arquivo,
        header=None,
        dtype=object
    )

    linha_cabecalho = None

    # Procura o cabeçalho nas primeiras linhas
    limite = min(20, len(bruto))

    for i in range(limite):

        texto = " ".join(
            bruto.iloc[i]
            .fillna("")
            .astype(str)
            .str.upper()
            .tolist()
        )

        encontrou_ra = (
            "RA" in texto
            or "NR RA" in texto
            or "Nº RA" in texto
            or "NUMERO RA" in texto
            or "NÚMERO RA" in texto
        )

        encontrou_nome = (
            "NOME" in texto
            or "ALUNO" in texto
            or "ESTUDANTE" in texto
        )

        if encontrou_ra and encontrou_nome:
            linha_cabecalho = i
            break

    if linha_cabecalho is None:
        raise ValueError(
            "Cabeçalho da Prova Paulista não localizado."
        )

    # Volta para o início do arquivo
    arquivo.seek(0)

    df = pd.read_excel(
        arquivo,
        header=linha_cabecalho
    )

    # ------------------------------------------------------
    # Remove colunas totalmente vazias
    # ------------------------------------------------------

    df = df.dropna(
        axis=1,
        how="all"
    )

    # ------------------------------------------------------
    # Limpeza dos nomes das colunas
    # ------------------------------------------------------

    novas_colunas = []

    for coluna in df.columns:

        nome = (
            str(coluna)
            .replace("\n", " ")
            .replace("\r", " ")
            .strip()
        )

        while "  " in nome:
            nome = nome.replace("  ", " ")

        novas_colunas.append(nome)

    df.columns = novas_colunas

    # ------------------------------------------------------
    # Remove linhas completamente vazias
    # ------------------------------------------------------

    df = df.dropna(
        how="all"
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df

# ==========================================================
# LEITOR PRINCIPAL
# ==========================================================

def ler_PP(arquivo, prefixo):

    lista = []

    # ------------------------------------------------------
    # LEITURA DE ARQUIVO ZIP
    # ------------------------------------------------------

    if arquivo.name.lower().endswith(".zip"):

        with zipfile.ZipFile(arquivo) as z:

            arquivos_excel = sorted(

                nome

                for nome in z.namelist()

                if (
                    nome.lower().endswith((".xlsx", ".xlsm"))
                    and
                    not os.path.basename(nome).startswith("~$")
                    and
                    not os.path.basename(nome).startswith(".")
                )

            )

            if len(arquivos_excel) == 0:

                raise ValueError(
                    "Nenhum arquivo Excel encontrado no ZIP."
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
                        f"[AVISO] {nome_excel}: {erro}"
                    )

    # ------------------------------------------------------
    # LEITURA DE EXCEL
    # ------------------------------------------------------

    else:

        df = ler_planilha(arquivo)

    # Usa a coluna TURMA quando ela existir
    if "TURMA" in df.columns:

        df["TURMA"] = (
            df["TURMA"]
            .fillna("")
            .astype(str)
        )

    else:

        df["TURMA"] = normalizar_turma(
            arquivo.name
        )

    lista.append(df)

    # ------------------------------------------------------
    # NENHUM DADO
    # ------------------------------------------------------

    if not lista:

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

        str(coluna).strip().upper()

        for coluna in df.columns

    ]

    # ------------------------------------------------------
    # RENOMEAR COLUNAS
    # ------------------------------------------------------

    mapa = {}

    for coluna in df.columns:

        nome = str(coluna).strip().upper()

        if "RA" in nome:
            mapa[coluna] = "RA"

        elif nome in (
            "NOME",
            "ESTUDANTE",
            "ALUNO"
        ):
            mapa[coluna] = "NOME"

        elif nome in (
            "PORT",
            "LP",
            "LÍNGUA PORTUGUESA",
            "LINGUA PORTUGUESA"
        ):
            mapa[coluna] = "PORT"

        elif nome in (
            "MAT",
            "MATEMÁTICA",
            "MATEMATICA"
        ):
            mapa[coluna] = "MAT"

    df.rename(
        columns=mapa,
        inplace=True
    )

    # ------------------------------------------------------
    # GARANTIR COLUNAS
    # ------------------------------------------------------

    for coluna in (
        "RA",
        "NOME",
        "PORT",
        "MAT"
    ):

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
    .fillna("")
    .astype(str)
    .str.upper()
    .str.strip()
    )

    df["TURMA"] = (
        df["TURMA"]
        .fillna("")
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

    df.loc[df["PORT"] > 1, "PORT"] /= 100

    df.loc[df["MAT"] > 1, "MAT"] /= 100

    # ------------------------------------------------------
    # RESULTADOS
    # ------------------------------------------------------

    df[f"{prefixo}_LP"] = df["PORT"]

    df[f"{prefixo}_MAT"] = df["MAT"]

    df[f"{prefixo}_LP_STATUS"] = (
        df["PORT"].apply(classificar_pp)
    )

    df[f"{prefixo}_MAT_STATUS"] = (
        df["MAT"].apply(classificar_pp)
    )

    # ------------------------------------------------------
    # CHAVE DE MERGE
    # ------------------------------------------------------
    
    possui_ra = df["RA"] != ""

    df.loc[possui_ra, "CHAVE_MERGE"] = (
        df.loc[possui_ra, "RA"]
        + "_"
        + df.loc[possui_ra, "TURMA"]
    )

    df.loc[~possui_ra, "CHAVE_MERGE"] = (
        df.loc[~possui_ra, "NOME"]
        + "_"
        + df.loc[~possui_ra, "TURMA"]
    )

    # ------------------------------------------------------
    # REMOVER DUPLICADOS
    # ------------------------------------------------------

    df = (
        df
        .drop_duplicates(
            subset="CHAVE_MERGE",
            keep="first"
        )
        .sort_values(
            by=["TURMA", "NOME"],
            ignore_index=True
        )
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



