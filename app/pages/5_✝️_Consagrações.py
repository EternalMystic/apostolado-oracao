"""CRUD completo — Consagrações."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colunas_ui import montar_column_config
from utils.crud_ui import tabela_crud
from utils.data_manager import COL_CONSAGRACOES, ler_consagracoes, ler_membros, salvar_consagracoes

st.set_page_config(page_title="Consagrações", page_icon="✝️", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("✝️ Consagrações")

cons = [m for m in ler_membros() if str(m.get("consagrada", "")).lower() == "sim"]
st.metric("Consagrados (coluna do membro)", len(cons))

tabela_crud(
    chave="consagracoes",
    colunas=COL_CONSAGRACOES,
    carregar=ler_consagracoes,
    salvar=salvar_consagracoes,
    column_config=montar_column_config(
        COL_CONSAGRACOES,
        {"data_consagracao": st.column_config.DateColumn("Data da consagração")},
    ),
    colunas_data=["data_consagracao"],
    id_col="id",
    altura=400,
    aba_excel="Consagracoes",
)
