"""Livro de atas e reuniões do Apostolado."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import ler_reunioes, salvar_reunioes
from utils.opcoes import TIPOS_REUNIAO
from utils.tabelas_apostolado import COL_REUNIOES

st.set_page_config(page_title="Atas", page_icon="📒", layout="wide", initial_sidebar_state="collapsed")
require_login()
inject_css()
st.title("📒 Atas e Reuniões")

st.caption("Livro de registro: posse da diretoria, admissão de zeladores e associados, deliberações.")

tabela_crud(
    chave="reunioes",
    colunas=COL_REUNIOES,
    carregar=ler_reunioes,
    salvar=salvar_reunioes,
    column_config={
        "data": st.column_config.DateColumn("Data"),
        "tipo": st.column_config.SelectboxColumn(options=TIPOS_REUNIAO),
    },
    colunas_data=["data"],
    id_col="id",
    altura=450,
    aba_excel="Reunioes",
)
