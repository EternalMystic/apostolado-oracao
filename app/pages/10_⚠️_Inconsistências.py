"""CRUD completo — Inconsistências."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import (
    COL_INCONSISTENCIAS,
    inconsistencias_criticas_abertas,
    ler_inconsistencias_df,
    salvar_inconsistencias_df,
)
from utils.opcoes import PRIORIDADES, RESOLVIDA

st.set_page_config(page_title="Inconsistências", page_icon="⚠️", layout="wide", initial_sidebar_state="collapsed")
require_login()
inject_css()
st.title("⚠️ Inconsistências")

crit = inconsistencias_criticas_abertas()
if crit:
    st.error(f"{len(crit)} crítica(s) em aberto.")


def _filtro(df: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    filtrado = False
    prio = st.session_state.get("inc_f_prio", [])
    if prio:
        df = df[df["prioridade"].isin(prio)]
        filtrado = True
    if st.session_state.get("inc_f_abertas", False):
        df = df[~df["resolvida"].astype(str).str.lower().isin(("sim", "s"))]
        filtrado = True
    return df, filtrado


st.multiselect("Prioridade", PRIORIDADES, key="inc_f_prio")
st.checkbox("Somente em aberto", key="inc_f_abertas")

tabela_crud(
    chave="inconsistencias",
    colunas=COL_INCONSISTENCIAS,
    carregar=ler_inconsistencias_df,
    salvar=salvar_inconsistencias_df,
    column_config={
        "prioridade": st.column_config.SelectboxColumn(options=PRIORIDADES),
        "resolvida": st.column_config.SelectboxColumn(options=RESOLVIDA),
    },
    id_col=None,
    aplicar_filtro=_filtro,
    altura=450,
    aba_excel="Inconsistencias",
)
