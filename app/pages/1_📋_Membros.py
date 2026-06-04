"""CRUD completo — Membros."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import COL_MEMBROS, ler_membros_df, salvar_membros_df
from utils.opcoes import CONSAGRADA, SEXOS, SITUACOES

st.set_page_config(page_title="Membros", page_icon="📋", layout="wide")
require_login()
inject_css()
st.title("📋 Membros")

_cfg = {
    "id": st.column_config.NumberColumn("ID", min_value=1, step=1),
    "nasc": st.column_config.DateColumn("Nascimento"),
    "ingresso": st.column_config.DateColumn("Ingresso"),
    "sexo": st.column_config.SelectboxColumn("Sexo", options=SEXOS),
    "situacao": st.column_config.SelectboxColumn("Situação", options=SITUACOES),
    "consagrada": st.column_config.SelectboxColumn("Consagrada", options=CONSAGRADA),
}


def _filtro(df: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    filtrado = False
    nome = st.session_state.get("membros_f_nome", "")
    if nome:
        df = df[df["nome"].astype(str).str.contains(nome, case=False, na=False)]
        filtrado = True
    sits = st.session_state.get("membros_f_sit", [])
    if sits:
        df = df[df["situacao"].isin(sits)]
        filtrado = True
    return df, filtrado


st.text_input("Buscar nome", key="membros_f_nome")
base0 = ler_membros_df()
st.multiselect(
    "Situação",
    sorted(base0["situacao"].dropna().unique()) if not base0.empty else SITUACOES,
    key="membros_f_sit",
)

tabela_crud(
    chave="membros",
    colunas=COL_MEMBROS,
    carregar=ler_membros_df,
    salvar=salvar_membros_df,
    column_config=_cfg,
    colunas_data=["nasc", "ingresso"],
    id_col="id",
    aplicar_filtro=_filtro,
    altura=500,
)
