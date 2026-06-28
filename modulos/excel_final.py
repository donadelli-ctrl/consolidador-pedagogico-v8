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
    # PAINEL ESCOLA
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
    # ESTUDANTES PRIORITÁRIOS
    # ======================================================

    abas["ESTUDANTES_PRIORITARIOS"] = prioritarios.copy()

    # ======================================================
    # SEM PARTICIPAÇÃO
    # ======================================================

    abas["SEM_PARTICIPACAO"] = sem_participacao.copy()

    # ======================================================
    # ABAS DAS TURMAS
    # ======================================================

    coluna_turma = "TURMA_PAD"

    if coluna_turma not in base_final.columns:

        coluna_turma = "TURMA"

    if coluna_turma in base_final.columns:

        turmas = sorted(

            base_final[coluna_turma]

            .dropna()

            .unique()

        )

        for turma in turmas:

            df_turma = (

                base_final[

                    base_final[coluna_turma] == turma

                ]

                .copy()

            )

            if "NOME" in df_turma.columns:

                df_turma = (

                    df_turma

                    .sort_values(

                        "NOME"

                    )

                    .reset_index(

                        drop=True

                    )

                )

            abas[str(turma)] = df_turma

    return abas
