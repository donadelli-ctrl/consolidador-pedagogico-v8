def normalizar_ra(valor):
    """
    Normaliza o RA do estudante.

    Exemplos
    --------
    351234567.0      -> 351234567
    "351234567"      -> 351234567
    "351.234.567"    -> 351234567
    NaN              -> ""
    """

    import pandas as pd

    if pd.isna(valor):
        return ""

    texto = str(valor).strip()

    # Remove .0 do Excel
    if texto.endswith(".0"):
        texto = texto[:-2]

    # Mantém apenas números
    texto = "".join(
        c for c in texto
        if c.isdigit()
    )

    return texto
