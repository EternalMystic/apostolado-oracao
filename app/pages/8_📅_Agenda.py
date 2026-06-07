"""CRUD completo — Agenda."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import COL_AGENDA, ler_agenda, salvar_agenda
from utils.opcoes import TIPOS_AGENDA

st.set_page_config(page_title="Agenda", page_icon="📅", layout="wide", initial_sidebar_state="collapsed")
require_login()
inject_css()
st.title("📅 Agenda")

tabela_crud(
    chave="agenda",
    colunas=COL_AGENDA,
    carregar=ler_agenda,
    salvar=salvar_agenda,
    column_config={
        "data": st.column_config.DateColumn("Data"),
        "tipo": st.column_config.SelectboxColumn(options=TIPOS_AGENDA),
    },
    colunas_data=["data"],
    id_col="id",
    altura=450,
    aba_excel="Agenda",
)
