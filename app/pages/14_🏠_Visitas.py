"""CRUD completo — Visitas domiciliares."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import COL_VISITAS, ler_membros, ler_visitas, salvar_visitas
from utils.dados_membros import ITENS_ENTREGA
from utils.opcoes import REALIZADA

st.set_page_config(page_title="Visitas", page_icon="🏠", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("🏠 Visitas")

membros = {m[0]: m[2] for m in ler_membros()}


def _filtro(df: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    b = st.session_state.get("vis_f_bairro", "Todos")
    if b != "Todos" and not df.empty:
        return df[df["bairro"].astype(str) == b], True
    r = st.session_state.get("vis_f_real", "Todas")
    if r == "Pendentes":
        return df[df["realizada"].astype(str).str.upper() != "S"], True
    if r == "Realizadas":
        return df[df["realizada"].astype(str).str.upper() == "S"], True
    return df, False


if membros and st.button("Gerar visitas para todos os ativos"):
    ativos = [m for m in ler_membros() if m[10] in ("Ativo", "Ativo (presumido)")]
    rows = []
    for i, m in enumerate(ativos, start=1):
        rows.append(
            {
                "id": i,
                "membro_id": m[0],
                "membro_nome": m[2],
                "data_visita": "",
                "bairro": m[7] or "",
                "item": ITENS_ENTREGA[-1],
                "realizada": "N",
                "observacoes": "",
            }
        )
    salvar_visitas(pd.DataFrame(rows, columns=COL_VISITAS))
    st.session_state.pop("visitas_base", None)
    st.rerun()

bairros = ["Todos"] + sorted({m[7] for m in ler_membros() if m[7]})
st.selectbox("Bairro", bairros, key="vis_f_bairro")
st.radio("Status", ["Todas", "Pendentes", "Realizadas"], horizontal=True, key="vis_f_real")

tabela_crud(
    chave="visitas",
    colunas=COL_VISITAS,
    carregar=ler_visitas,
    salvar=salvar_visitas,
    column_config={
        "item": st.column_config.SelectboxColumn(options=ITENS_ENTREGA),
        "realizada": st.column_config.SelectboxColumn(options=REALIZADA),
        "data_visita": st.column_config.DateColumn("Data visita"),
    },
    colunas_data=["data_visita"],
    id_col="id",
    aplicar_filtro=_filtro,
    altura=450,
)
