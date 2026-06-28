import os
import zipfile
from io import BytesIO

import pandas as pd


# ==========================================================
# CLASSIFICAÇÃO
# ==========================================================

def classificar_pp(valor):

    if pd.isna(valor):
        return ""

    try:
        valor = float(valor)
    except:
        return ""

    if valor < 0.50:
        return "Abaixo do Básico"
    elif valor < 0.70:
        return "Básico"
    elif valor < 0.90:
        return "Adequado"
    else:
        return "Proficiente"


# ==========================================================
# LOCALIZAR CABEÇALHO
# ==========================================================

def ler_planilha(f):

    # Lê sem cabeçalho
    bruto = pd.read_excel(f, header=None)

    linha_cabecalho = None

    for i in range(min(15, len(bruto))):

        texto = " ".join(bruto.iloc[i].astype(str).tolist()).upper()

        if "NR RA" in texto and "NOME" in texto:
            linha_cabecalho = i
            break

    if linha_cabecalho is None:
        raise Exception("Não foi possível localizar o cabeçalho da Prova Paulista.")

    f.seek(0)

    return pd.read_excel(f, header=linha_cabecalho)


# ==========================================================
# LEITOR
# ==========================================================

def ler_PP(arquivo, prefixo):

    lista = []

    if arquivo.name.lower().endswith(".zip"):

        with zipfile.ZipFile(arquivo) as z:

            excels = [

                arq

                for arq in z.namelist()

                if arq.lower().endswith((".xlsx", ".xlsm"))

            ]

            for excel in excels:

                with z.open(excel) as arq:

                    dados = BytesIO(arq.read())

                    df = ler_planilha(dados)

                    turma = os.path.splitext(
                        os.path.basename(excel)
                    )[0].strip()

                    df["TURMA"] = turma

                    lista.append(df)

    else:

        df = ler_planilha(arquivo)

        df["TURMA"] = ""

        lista.append(df)

    df = pd.concat(lista, ignore_index=True)

    df.columns = [str(c).strip() for c in df.columns]

    # Renomear
    df.rename(
        columns={
            "NR RA": "RA",
            "Nome": "NOME",
        },
        inplace=True
    )

    # Converter percentuais
    df["PORT"] = pd.to_numeric(df.get("PORT"), errors="coerce")
    df["MAT"] = pd.to_numeric(df.get("MAT"), errors="coerce")

    df[f"{prefixo}_LP"] = df["PORT"]
    df[f"{prefixo}_MAT"] = df["MAT"]

    df[f"{prefixo}_LP_STATUS"] = df["PORT"].apply(classificar_pp)
    df[f"{prefixo}_MAT_STATUS"] = df["MAT"].apply(classificar_pp)

    df["RA"] = df["RA"].astype(str).str.strip()
    df["NOME"] = df["NOME"].astype(str).str.strip()
    df["TURMA"] = df["TURMA"].astype(str).str.strip()

    df["CHAVE_MERGE"] = df["RA"] + "_" + df["TURMA"]

    return df[
        [
            "RA",
            "NOME",
            "TURMA",
            f"{prefixo}_LP",
            f"{prefixo}_LP_STATUS",
            f"{prefixo}_MAT",
            f"{prefixo}_MAT_STATUS",
            "CHAVE_MERGE",
        ]
    ]
