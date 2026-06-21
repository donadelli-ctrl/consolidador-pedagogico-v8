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

    abas["PAINEL_ESCOLA"] = (

        painel_escola

        .copy()

    )

    # ======================================================
    # RESUMO GERAL
    # ======================================================

    resumo_geral = (

        base_final

        .copy()

    )

    abas["RESUMO_GERAL"] = (

        resumo_geral

    )

    # ======================================================
    # ESCOLA EM NÚMEROS
    # ======================================================

    abas["ESCOLA_EM_NUMEROS"] = (

        resumo_por_turma

        .copy()

    )

    # ======================================================
    # MONITORAMENTO AB
    # ======================================================

    monitoramento_ab = (

        prioritarios

        .copy()

    )

    abas["MONITORAMENTO_AB"] = (

        monitoramento_ab

    )

    # ======================================================
    # SEM PARTICIPAÇÃO
    # ======================================================

    abas["SEM_PARTICIPACAO"] = (

        sem_participacao

        .copy()

    )

    # ======================================================
    # EVOLUÇÃO
    # ======================================================

    abas["EVOLUCAO"] = (

        evolucao

        .copy()

    )

    # ======================================================
    # ABAS DAS TURMAS
    # ======================================================

    if (

        "TURMA_PAD"

        in

        base_final.columns

    ):

        turmas = (

            sorted(

                base_final[

                    "TURMA_PAD"

                ]

                .dropna()

                .unique()

            )

        )

        for turma in turmas:

            df_turma = (

                base_final

                [

                    base_final[

                        "TURMA_PAD"

                    ]

                    ==

                    turma

                ]

                .copy()

            )

            abas[

                str(

                    turma

                )

            ] = (

                df_turma

                .sort_values(

                    "NOME"

                )

                .reset_index(

                    drop=True

                )

            )

    return abas
