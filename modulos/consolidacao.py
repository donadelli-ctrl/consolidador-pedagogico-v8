import pandas as pd


# ==========================================================
# CONSOLIDAÇÃO DAS BASES
# ==========================================================

def consolidar_base(

    df_ADE=None,
    df_PP1=None,
    df_PP2=None,
    df_ADP=None,
    df_PP3=None

):

    # ======================================================
    # ORGANIZAÇÃO DAS BASES
    # ======================================================

    bases = [

        ("ADE", df_ADE),
        ("PP1", df_PP1),
        ("PP2", df_PP2),
        ("ADP", df_ADP),
        ("PP3", df_PP3)

    ]

    # ======================================================
    # LOCALIZAR A PRIMEIRA BASE VÁLIDA
    # ======================================================

    base = None

    for nome, df in bases:

        if (
            df is not None
            and
            not df.empty
            and
            "CHAVE_MERGE" in df.columns
        ):

            base = df.copy()

            break

    if base is None:

        return pd.DataFrame()

    # ======================================================
    # GARANTIR COLUNAS BÁSICAS
    # ======================================================

    for coluna in [

        "CHAVE_MERGE",
        "RA",
        "NOME",
        "TURMA"

    ]:

        if coluna not in base.columns:

            base[coluna] = ""

    # ======================================================
    # MERGE DAS DEMAIS BASES
    # ======================================================

        # ======================================================
    # MERGE DAS DEMAIS BASES
    # ======================================================

    for nome, df in bases:

        if df is None:
            continue

        if df.empty:
            continue

        if df.equals(base):
            continue

        if "CHAVE_MERGE" not in df.columns:
            continue

        # --------------------------------------------------
        # Mantém apenas as colunas necessárias
        # --------------------------------------------------

        colunas_merge = ["CHAVE_MERGE"]

        for coluna in df.columns:

            if coluna == "CHAVE_MERGE":
                continue

            if coluna.startswith(nome):

                colunas_merge.append(coluna)

        df_merge = (
            df[colunas_merge]
            .copy()
            .loc[:, lambda x: ~x.columns.duplicated()]
        )

        # --------------------------------------------------
        # MERGE
        # --------------------------------------------------

        base = base.merge(

            df_merge,

            on="CHAVE_MERGE",

            how="outer"

        )

        # --------------------------------------------------
        # Recuperar identificação
        # --------------------------------------------------

        for coluna in ["RA", "NOME", "TURMA"]:

            coluna_x = f"{coluna}_x"
            coluna_y = f"{coluna}_y"

            if coluna_x in base.columns and coluna_y in base.columns:

                base[coluna] = (
                    base[coluna_x]
                    .combine_first(base[coluna_y])
                )

                base.drop(
                    columns=[coluna_x, coluna_y],
                    inplace=True
                )

            elif coluna_x in base.columns:

                base.rename(
                    columns={coluna_x: coluna},
                    inplace=True
                )

            elif coluna_y in base.columns:

                base.rename(
                    columns={coluna_y: coluna},
                    inplace=True
                )

            elif coluna not in base.columns:

                base[coluna] = ""

    # ======================================================
    # REMOVER DUPLICIDADES
    # ======================================================

        # ======================================================
    # REMOVER DUPLICIDADES
    # ======================================================

    # Remove registros sem chave
    base = base[
        base["CHAVE_MERGE"]
        .fillna("")
        .astype(str)
        .str.strip()
        != ""
    ]

    # Mantém apenas o primeiro registro de cada estudante
    base = (
        base
        .drop_duplicates(
            subset="CHAVE_MERGE",
            keep="first"
        )
        .reset_index(drop=True)
    )

    # Remove espaços excedentes
    for coluna in ["RA", "NOME", "TURMA", "CHAVE_MERGE"]:

        if coluna in base.columns:

            base[coluna] = (
                base[coluna]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    # ======================================================
    # ORDENAÇÃO
    # ======================================================

    colunas_ordenacao = []

    if "TURMA" in base.columns:
        colunas_ordenacao.append("TURMA")

    if "NOME" in base.columns:
        colunas_ordenacao.append("NOME")

    if colunas_ordenacao:
        base = base.sort_values(
            by=colunas_ordenacao,
            ignore_index=True
        )

    # ======================================================
    # GARANTIR COLUNAS DE IDENTIFICAÇÃO
    # ======================================================

    for coluna in [
        "RA",
        "NOME",
        "TURMA",
        "CHAVE_MERGE"
    ]:

        if coluna not in base.columns:
            base[coluna] = ""

    # ======================================================
    # RETORNO
    # ======================================================

    return base
    
