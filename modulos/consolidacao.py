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

    base = df_ADE.copy()

    # ------------------------------------------------------
    # PP1
    # ------------------------------------------------------

    if (

        df_PP1 is not None

        and

        len(df_PP1) > 0

    ):

        base = base.merge(

            df_PP1,

            on="CHAVE_MERGE",

            how="outer"

        )

    # ------------------------------------------------------
    # PP2
    # ------------------------------------------------------

    if (

        df_PP2 is not None

        and

        len(df_PP2) > 0

    ):

        base = base.merge(

            df_PP2,

            on="CHAVE_MERGE",

            how="outer"

        )

    # ------------------------------------------------------
    # ADP
    # ------------------------------------------------------

    if (

        df_ADP is not None

        and

        len(df_ADP) > 0

    ):

        base = base.merge(

            df_ADP,

            on="CHAVE_MERGE",

            how="outer"

        )

    # ------------------------------------------------------
    # PP3
    # ------------------------------------------------------

    if (

        df_PP3 is not None

        and

        len(df_PP3) > 0

    ):

        base = base.merge(

            df_PP3,

            on="CHAVE_MERGE",

            how="outer"

        )

    # ------------------------------------------------------
    # REMOVER DUPLICADOS
    # ------------------------------------------------------

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
