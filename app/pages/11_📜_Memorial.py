"""CRUD completo — Memorial."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import COL_MEMORIAL, ler_memorial, salvar_memorial

st.set_page_config(page_title="Memorial", page_icon="📜", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("📜 Memorial")

tabela_crud(
    chave="memorial",
    colunas=COL_MEMORIAL,
    carregar=ler_memorial,
    salvar=salvar_memorial,
    column_config={
        "nasc": st.column_config.DateColumn("Nascimento"),
        "falecimento": st.column_config.DateColumn("Falecimento"),
    },
    colunas_data=["nasc", "falecimento"],
    id_col=None,
    altura=400,
    aba_excel="Memorial",
)

st.caption("Descansai em paz. R.I.P.")
