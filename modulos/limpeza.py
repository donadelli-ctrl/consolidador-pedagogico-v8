# ==========================================================
# LIMPEZA DA BASE
# ==========================================================

def limpar_base(base):

    # ======================================================
    # BASE VAZIA
    # ======================================================

    if base is None:

        return base

    if base.empty:

        return base

    # ======================================================
    # REMOVER COLUNAS DUPLICADAS
    # ======================================================

    base = base.loc[
        :,
        ~base.columns.duplicated()
    ]

    # ======================================================
    # REMOVER COLUNAS _X E _Y
    # ======================================================

    colunas_remover = [

        coluna

        for coluna in base.columns

        if (
            coluna.endswith("_x")
            or
            coluna.endswith("_y")
        )

    ]

    base.drop(
        columns=colunas_remover,
        errors="ignore",
        inplace=True
    )

    # ======================================================
    # REMOVER LINHAS TOTALMENTE VAZIAS
    # ======================================================

    base.dropna(
        how="all",
        inplace=True
    )

    # ======================================================
    # PADRONIZAR CAMPOS DE IDENTIFICAÇÃO
    # ======================================================

    if "RA" in base.columns:

        base["RA"] = (
            base["RA"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    if "NOME" in base.columns:

        base["NOME"] = (
            base["NOME"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.strip()
        )

    if "TURMA" in base.columns:

        base["TURMA"] = (
            base["TURMA"]
            .fillna("")
            .astype(str)
            .str.upper()
            .str.strip()
        )

    # ======================================================
    # REMOVER DUPLICIDADES
    # ======================================================

    if "CHAVE_MERGE" in base.columns:

        base = (

            base

            .drop_duplicates(

                subset="CHAVE_MERGE",

                keep="first"

            )

            .reset_index(

                drop=True

            )

        )

    # ======================================================
    # ORDENAÇÃO
    # ======================================================

    if (
        "TURMA" in base.columns
        and
        "NOME" in base.columns
    ):

        base = (

            base

            .sort_values(

                by=[
                    "TURMA",
                    "NOME"
                ]

            )

            .reset_index(

                drop=True

            )

        )

    elif "NOME" in base.columns:

        base = (

            base

            .sort_values(

                by="NOME"

            )

            .reset_index(

                drop=True

            )

        )

    else:

        base.reset_index(
            drop=True,
            inplace=True
        )

    # ======================================================
    # RETORNO
    # ======================================================

    return base


