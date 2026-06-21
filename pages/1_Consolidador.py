import streamlit as st
import pandas as pd

from io import BytesIO

from modulos.leitor_ade import ler_ADE
from modulos.leitor_pp import ler_PP

from modulos.consolidacao import consolidar_base
from modulos.limpeza import limpar_base

from modulos.participacao import (
    calcular_participacao,
    obter_sem_participacao
)

from modulos.prioritarios import (
    obter_prioritarios
)

from modulos.escola_em_numeros import (
    gerar_resumo_por_turma,
    gerar_painel_escola
)

from modulos.evolucao import (
    gerar_evolucao
)

from modulos.excel_final import (
    montar_abas
)

from modulos.formatacao_excel import (
    aplicar_cores
)
