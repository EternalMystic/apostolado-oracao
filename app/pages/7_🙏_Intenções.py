"""Mural de oração — intenções da comunidade."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colunas_ui import montar_column_config
from utils.crud_ui import tabela_crud
from utils.data_manager import COL_INTENCOES, ler_intencoes, salvar_intencoes
from utils.opcoes import CATEGORIA_INTENCAO, PRIORIDADE_INTENCAO, STATUS_INTENCAO

st.set_page_config(page_title="Intenções", page_icon="🙏", layout="wide", initial_sidebar_state="collapsed")
require_login()
inject_css()
st.title("🙏 Mural de Oração")

df = ler_intencoes()
if not df.empty:
    pend = len(df[df["status"].astype(str).str.lower() == "pendente"])
    st.metric("Pedidos em oração", pend)

tabela_crud(
    chave="intencoes",
    colunas=COL_INTENCOES,
    carregar=ler_intencoes,
    salvar=salvar_intencoes,
    column_config=montar_column_config(
        COL_INTENCOES,
        {
            "data": st.column_config.DateColumn("Data"),
            "categoria": st.column_config.SelectboxColumn("Categoria", options=CATEGORIA_INTENCAO),
            "status": st.column_config.SelectboxColumn("Status", options=STATUS_INTENCAO),
            "prioridade": st.column_config.SelectboxColumn("Prioridade", options=PRIORIDADE_INTENCAO),
        },
    ),
    colunas_data=["data"],
    id_col="id",
    altura=450,
    aba_excel="Intencoes",
)
