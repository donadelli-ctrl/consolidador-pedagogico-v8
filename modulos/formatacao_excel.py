from openpyxl.styles import Font


# ==========================================================
# FORMATAÇÃO DAS ABAS
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
    # EVOLUÇÃO
    # ------------------------------------------------------

    for linha in ws.iter_rows():

        for celula in linha:

            if celula.value == "Melhorou":

                celula.font = Font(

                    color="008000",

                    bold=True

                )

            elif celula.value == "Manteve":

                celula.font = Font(

                    color="C9A000",

                    bold=True

                )

            elif celula.value == "Piorou":

                celula.font = Font(

                    color="FF0000",

                    bold=True

                )

            elif celula.value == "Sem Comparação":

                celula.font = Font(

                    color="808080",

                    italic=True

                )

    # ------------------------------------------------------
    # SITUAÇÃO
    # ------------------------------------------------------

            elif celula.value == "Adequado":

                celula.font = Font(

                    color="008000",

                    bold=True

                )

            elif celula.value == "Acompanhamento":

                celula.font = Font(

                    color="C9A000",

                    bold=True

                )

            elif celula.value == "Atenção":

                celula.font = Font(

                    color="FF0000",

                    bold=True

                )
