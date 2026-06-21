import pandas as pd
import zipfile

from io import BytesIO


# ==========================================================
# LEITOR ADE
# ==========================================================

def ler_ADE(

    arquivo

):

    nome = arquivo.name.lower()

    # ======================================================
    # ZIP
    # ======================================================

    if nome.endswith(

        ".zip"

    ):

        with zipfile.ZipFile(

            arquivo

        ) as z:

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

            if len(

                arquivos_excel

            ) == 0:

                raise Exception(

                    "Nenhum arquivo Excel encontrado dentro do ZIP."

                )

            excel = arquivos_excel[0]

            with z.open(

                excel

            ) as f:

                df = pd.read_excel(

                    BytesIO(

                        f.read()

                    )

                )

    # ======================================================
    # EXCEL
    # ======================================================

    else:

        df = pd.read_excel(

            arquivo

        )

    return df
