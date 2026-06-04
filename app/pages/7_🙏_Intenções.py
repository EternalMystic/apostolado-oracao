"""CRUD completo — Intenções de oração."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import COL_INTENCOES, ler_intencoes, salvar_intencoes
from utils.opcoes import STATUS_INTENCAO

st.set_page_config(page_title="Intenções", page_icon="🙏", layout="wide")
require_login()
inject_css()
st.title("🙏 Intenções")

tabela_crud(
    chave="intencoes",
    colunas=COL_INTENCOES,
    carregar=ler_intencoes,
    salvar=salvar_intencoes,
    column_config={
        "data": st.column_config.DateColumn("Data"),
        "status": st.column_config.SelectboxColumn(options=STATUS_INTENCAO),
    },
    colunas_data=["data"],
    id_col="id",
    altura=450,
)
