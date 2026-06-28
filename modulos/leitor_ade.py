import pandas as pd
import zipfile

from io import BytesIO


# ==========================================================
# LEITOR ADE / AVD / ADP
# ==========================================================

def ler_ADE(arquivo):

    nome = arquivo.name.lower()

    # ======================================================
    # LEITURA DE ARQUIVO ZIP
    # ======================================================

    if nome.endswith(".zip"):

        lista_df = []

        with zipfile.ZipFile(arquivo) as z:

            arquivos_excel = [

                arq

                for arq in z.namelist()

                if arq.lower().endswith(

                    (

                        ".xlsx",

                        ".xlsm"

                    )

                )

            ]

            if len(arquivos_excel) == 0:

                raise Exception(

                    "Nenhum arquivo Excel encontrado dentro do ZIP."

                )

            for excel in arquivos_excel:

                with z.open(excel) as f:

                    try:

                        df = pd.read_excel(

                            BytesIO(

                                f.read()

                            )

                        )

                        lista_df.append(df)

                    except Exception:

                        continue

        if len(lista_df) == 0:

            raise Exception(

                "Nenhuma planilha válida foi encontrada no arquivo ZIP."

            )

        df = pd.concat(

            lista_df,

            ignore_index=True

        )

    # ======================================================
    # LEITURA DE EXCEL
    # ======================================================

    else:

        df = pd.read_excel(

            arquivo

        )

    # ======================================================
    # LIMPEZA
    # ======================================================

    df.dropna(

        how="all",

        inplace=True

    )

    df.reset_index(

        drop=True,

        inplace=True

    )

    # ======================================================
    # PADRONIZAÇÃO DAS COLUNAS
    # ======================================================

    df.columns = [

        str(col).strip().upper()

        for col in df.columns

    ]

    # ======================================================
    # CHAVE DE CONSOLIDAÇÃO
    # ======================================================

    if (

        "RA" in df.columns

        and

        "TURMA" in df.columns

    ):

        df["CHAVE_MERGE"] = (

            df["RA"]

            .astype(str)

            .str.strip()

            +

            "_"

            +

            df["TURMA"]

            .astype(str)

            .str.strip()

        )

    return df
