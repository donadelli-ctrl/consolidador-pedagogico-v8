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
    # BASE INICIAL
    # ======================================================

    base = df_ADE.copy()

    # ======================================================
    # LISTA DE DATAFRAMES
    # ======================================================

    lista_bases = [

        df_PP1,

        df_PP2,

        df_ADP,

        df_PP3

    ]

    # ======================================================
    # CONSOLIDAÇÃO
    # ======================================================

    for df in lista_bases:

        if (

            df is not None

            and

            len(df) > 0

        ):

            # ----------------------------------------------
            # VERIFICAR CHAVE
            # ----------------------------------------------

            if (

                "CHAVE_MERGE"

                not in df.columns

            ):

                continue

            if (

                "CHAVE_MERGE"

                not in base.columns

            ):

                continue

            base = base.merge(

                df,

                on="CHAVE_MERGE",

                how="outer"

            )

    # ======================================================
    # REMOVER DUPLICADOS
    # ======================================================

    if (

        "CHAVE_MERGE"

        in base.columns

    ):

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
