# ==========================================================
# MONTAGEM DAS ABAS
# ==========================================================

def montar_abas(

    painel_escola,
    base_final,
    resumo_por_turma,
    prioritarios,
    sem_participacao,
    evolucao

):

    abas = {}

    # ======================================================
    # PAINEL DA ESCOLA
    # ======================================================

    abas["PAINEL_ESCOLA"] = painel_escola.copy()

    # ======================================================
    # RESUMO GERAL
    # ======================================================

    abas["RESUMO_GERAL"] = base_final.copy()

    # ======================================================
    # ESCOLA EM NÚMEROS
    # ======================================================

    abas["ESCOLA_EM_NUMEROS"] = resumo_por_turma.copy()

    # ======================================================
    # EVOLUÇÃO
    # ======================================================

    abas["EVOLUCAO"] = evolucao.copy()

    # ======================================================
    # MONITORAMENTO
    # ======================================================

    abas["MONITORAMENTO_AB"] = prioritarios.copy()

    # ======================================================
    # PRIORITÁRIOS
    # ======================================================

    abas["ESTUDANTES_PRIORITARIOS"] = prioritarios.copy()

    # ======================================================
    # SEM PARTICIPAÇÃO
    # ======================================================

    abas["SEM_PARTICIPACAO"] = sem_participacao.copy()

    # ======================================================
    # DEFINIR COLUNA DA TURMA
    # ======================================================

    coluna_turma = "TURMA_PAD"

    if coluna_turma not in base_final.columns:

        coluna_turma = "TURMA"

    if coluna_turma not in base_final.columns:

        return abas

    # ======================================================
    # LISTA DAS TURMAS
    # ======================================================

    turmas = (

        base_final[coluna_turma]

        .fillna("")

        .astype(str)

        .str.strip()

    )

    turmas = sorted(

        [

            turma

            for turma in turmas.unique()

            if turma != ""

        ]

    )

    # ======================================================
    # CRIAR UMA ABA PARA CADA TURMA
    # ======================================================

    for turma in turmas:

        df_turma = (

            base_final[

                base_final[coluna_turma] == turma

            ]

            .copy()

        )

        # ----------------------------------------------
        # ORDENAÇÃO
        # ----------------------------------------------

        if "NOME" in df_turma.columns:

            df_turma = (

                df_turma

                .sort_values(

                    by="NOME"

                )

                .reset_index(

                    drop=True

                )

            )

        # ----------------------------------------------
        # REMOVER COLUNAS AUXILIARES
        # ----------------------------------------------

        colunas_remover = [

            "CHAVE_MERGE"

        ]

        for coluna in colunas_remover:

            if coluna in df_turma.columns:

                df_turma.drop(

                    columns=coluna,

                    inplace=True

                )

        abas[str(turma)] = df_turma

    # ======================================================
    # ORGANIZAR AS ABAS
    # ======================================================

    ordem = [

        "PAINEL_ESCOLA",
        "RESUMO_GERAL",
        "ESCOLA_EM_NUMEROS",
        "EVOLUCAO",
        "MONITORAMENTO_AB",
        "ESTUDANTES_PRIORITARIOS",
        "SEM_PARTICIPACAO"

    ]

    abas_finais = {}

    # ------------------------------------------------------
    # ABAS FIXAS
    # ------------------------------------------------------

    for aba in ordem:

        if aba in abas:

            abas_finais[aba] = abas[aba]

    # ------------------------------------------------------
    # ABAS DAS TURMAS
    # ------------------------------------------------------

    for turma in turmas:

        if turma in abas:

            abas_finais[turma] = abas[turma]

    # ======================================================
    # RETORNO
    # ======================================================

    return abas_finais

