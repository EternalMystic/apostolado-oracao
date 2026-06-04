"""Controle de entregas de materiais."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import ler_entregas, salvar_entregas
from utils.dados_membros import ITENS_ENTREGA

st.set_page_config(page_title="Entregas", page_icon="📦", layout="wide")
require_login()
st.title("📦 Entregas de Materiais")

df = ler_entregas()
st.caption("Itens: " + ", ".join(ITENS_ENTREGA[:5]) + "...")

filtro = st.radio("Mostrar", ["Todas", "Pendentes", "Entregues"], horizontal=True)
if filtro == "Pendentes":
    df = df[df["entregue"].astype(str).str.upper() != "S"]
elif filtro == "Entregues":
    df = df[df["entregue"].astype(str).str.upper() == "S"]

edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "item": st.column_config.SelectboxColumn(options=ITENS_ENTREGA),
        "entregue": st.column_config.SelectboxColumn(options=["S", "N"]),
    },
)

c1, c2 = st.columns(2)
c1.metric("Total", len(edited))
c2.metric(
    "Entregues",
    len(edited[edited["entregue"].astype(str).str.upper() == "S"]),
)

if st.button("💾 Salvar entregas"):
    salvar_entregas(edited)
    st.success("Entregas salvas.")
