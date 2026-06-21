from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment
)

from openpyxl.utils import get_column_letter


# ==========================================================
# FORMATAÇÃO DAS ABAS
# ==========================================================

def aplicar_cores(ws):

    # ======================================================
    # CABEÇALHO
    # ======================================================

    azul = PatternFill(

        "solid",

        fgColor="1F4E79"

    )

    for celula in ws[1]:

        celula.font = Font(

            color="FFFFFF",

            bold=True

        )

        celula.fill = azul

        celula.alignment = Alignment(

            horizontal="center",

            vertical="center"

        )

    # ======================================================
    # EVOLUÇÃO E SITUAÇÃO
    # ======================================================

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

    # ======================================================
    # CONGELAR PRIMEIRA LINHA
    # ======================================================

    ws.freeze_panes = "A2"

    # ======================================================
    # FILTRO AUTOMÁTICO
    # ======================================================

    ws.auto_filter.ref = ws.dimensions

    # ======================================================
    # AJUSTE DAS COLUNAS
    # ======================================================

    for coluna in ws.columns:

        tamanho = 0

        letra = get_column_letter(

            coluna[0].column

        )

        for celula in coluna:

            try:

                tamanho = max(

                    tamanho,

                    len(

                        str(

                            celula.value

                        )

                    )

                )

            except:

                pass

        ws.column_dimensions[

            letra

        ].width = min(

            tamanho + 3,

            40

        )
