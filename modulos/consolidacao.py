import pandas as pd


# ==========================================================
# CONSOLIDAÇÃO DAS BASES
# ==========================================================

def consolidar_base(

    df_ADE,

    df_PP1=None,

    df_PP2=None,

    df_ADP=None,

    df_PP3=None

):

    # ======================================================
    # LISTA DE BASES
    # ======================================================

    lista_bases = [

        df_ADE,

        df_PP1,

        df_PP2,

        df_ADP,

        df_PP3

    ]

    # ======================================================
    # DEFINIR BASE INICIAL
    # ======================================================

    base = None

    for df in lista_bases:

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
    # CONSOLIDAÇÃO
    # ======================================================

    for df in lista_bases:

        if (

            df is None

            or

            df.empty

        ):

            continue

        if df is base:

            continue

        if "CHAVE_MERGE" not in df.columns:

            continue

        base = base.merge(

            df,

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
