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
    # LISTA DAS BASES
    # ======================================================

    lista = [

        df_ADE,
        df_PP1,
        df_PP2,
        df_ADP,
        df_PP3

    ]

    # ======================================================
    # ENCONTRAR A PRIMEIRA BASE VÁLIDA
    # ======================================================

    base_principal = None

    for df in lista:

        if (
            df is not None
            and
            not df.empty
            and
            "CHAVE_MERGE" in df.columns
        ):

            base_principal = df.copy()
            break

    if base_principal is None:

        return pd.DataFrame()

    # ======================================================
    # GARANTIR COLUNAS DA BASE PRINCIPAL
    # ======================================================

    colunas_identificacao = [

        "CHAVE_MERGE",
        "RA",
        "NOME",
        "TURMA"

    ]

    for coluna in colunas_identificacao:

        if coluna not in base_principal.columns:

            base_principal[coluna] = ""

    # ======================================================
    # BASE FINAL
    # ======================================================

    base = base_principal.copy()

    # ======================================================
    # MERGE DAS DEMAIS BASES
    # ======================================================

    for df in lista:

        if df is None:

            continue

        if df.empty:

            continue

        if df.equals(base_principal):

            continue

        if "CHAVE_MERGE" not in df.columns:

            continue

        # ----------------------------------------------
        # MANTER SOMENTE CHAVE + RESULTADOS
        # ----------------------------------------------

        colunas = [

            c

            for c in df.columns

            if c not in [

                "RA",
                "NOME",
                "TURMA"

            ]

        ]

        df_merge = df[colunas].copy()

        # ----------------------------------------------
        # REMOVER DUPLICADAS
        # ----------------------------------------------

        df_merge = df_merge.loc[
            :,
            ~df_merge.columns.duplicated()
        ]

        # ----------------------------------------------
        # MERGE
        # ----------------------------------------------

        base = base.merge(

            df_merge,

            on="CHAVE_MERGE",

            how="left"

        )

    # ======================================================
    # REMOVER DUPLICADOS
    # ======================================================

    base = (

        base

        .drop_duplicates(

            subset="CHAVE_MERGE"

        )

        .reset_index(

            drop=True

        )

    )

    return base
