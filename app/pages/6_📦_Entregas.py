"""CRUD completo — Entregas."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import COL_ENTREGAS, ler_entregas, salvar_entregas
from utils.dados_membros import ITENS_ENTREGA
from utils.opcoes import ENTREGUE

st.set_page_config(page_title="Entregas", page_icon="📦", layout="wide")
require_login()
inject_css()
st.title("📦 Entregas")


def _filtro(df: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    modo = st.session_state.get("ent_f_modo", "Todas")
    if modo == "Pendentes":
        return df[df["entregue"].astype(str).str.upper() != "S"], True
    if modo == "Entregues":
        return df[df["entregue"].astype(str).str.upper() == "S"], True
    return df, False


st.radio("Mostrar", ["Todas", "Pendentes", "Entregues"], horizontal=True, key="ent_f_modo")

tabela_crud(
    chave="entregas",
    colunas=COL_ENTREGAS,
    carregar=ler_entregas,
    salvar=salvar_entregas,
    column_config={
        "item": st.column_config.SelectboxColumn(options=ITENS_ENTREGA),
        "entregue": st.column_config.SelectboxColumn(options=ENTREGUE),
        "data_entrega": st.column_config.DateColumn("Data entrega"),
    },
    colunas_data=["data_entrega"],
    id_col="id",
    aplicar_filtro=_filtro,
    altura=450,
)
