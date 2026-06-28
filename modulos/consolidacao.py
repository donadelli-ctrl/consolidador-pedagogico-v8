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
    # DEFINIR BASE PRINCIPAL
    # ======================================================

    base = None

    for df in lista:

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
    # MERGE DAS DEMAIS BASES
    # ======================================================

    for df in lista:

        if df is None:

            continue

        if df.empty:

            continue

        if df is base:

            continue

        if "CHAVE_MERGE" not in df.columns:

            continue

        # ----------------------------------------------
        # REMOVER COLUNAS DUPLICADAS
        # ----------------------------------------------

        colunas_remover = [

            coluna

            for coluna in [

                "RA",

                "NOME",

                "TURMA"

            ]

            if coluna in df.columns

        ]

        df_merge = df.drop(

            columns=colunas_remover,

            errors="ignore"

        )

        # ----------------------------------------------
        # GARANTIR COLUNAS ÚNICAS
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

            how="outer"

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
