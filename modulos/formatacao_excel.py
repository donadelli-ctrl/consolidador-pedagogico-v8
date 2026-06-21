from openpyxl.styles import Font


# ==========================================================
# FORMATAÇÃO
# ==========================================================

def aplicar_cores(ws):

    # ------------------------------------------------------
    # CABEÇALHO
    # ------------------------------------------------------

    for celula in ws[1]:

        celula.font = Font(

            bold=True

        )

    # ------------------------------------------------------
    # COLORIR CÉLULAS
    # ------------------------------------------------------

    for linha in ws.iter_rows():

        for celula in linha:

            valor = str(

                celula.value

            )

            # EVOLUÇÃO

            if valor == "Melhorou":

                celula.font = Font(

                    color="008000",

                    bold=True

                )

            elif valor == "Manteve":

                celula.font = Font(

                    color="C9A000",

                    bold=True

                )

            elif valor == "Piorou":

                celula.font = Font(

                    color="FF0000",

                    bold=True

                )

            elif valor == "Sem Comparação":

                celula.font = Font(

                    color="808080",

                    italic=True

                )

            # SITUAÇÃO

            elif valor == "Adequado":

                celula.font = Font(

                    color="008000",

                    bold=True

                )

            elif valor == "Acompanhamento":

                celula.font = Font(

                    color="C9A000",

                    bold=True

                )

            elif valor == "Atenção":

                celula.font = Font(

                    color="FF0000",

                    bold=True

                )
