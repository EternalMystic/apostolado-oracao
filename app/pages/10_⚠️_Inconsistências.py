"""Revisão de inconsistências cadastrais."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import (
    COL_INCONSISTENCIAS,
    inconsistencias_criticas_abertas,
    ler_inconsistencias,
    salvar_inconsistencias,
)

st.set_page_config(page_title="Inconsistências", page_icon="⚠️", layout="wide")
require_login()
inject_css()
st.title("⚠️ Inconsistências – Revisão Pastoral")
st.caption("Cada inconsistência é um convite ao cuidado. Resolva com calma e caridade.")

crit = inconsistencias_criticas_abertas()
if crit:
    st.error(f"{len(crit)} inconsistência(s) crítica(s) em aberto.")
    for inc in crit:
        st.write(f"🔴 {inc[2]}")

items = ler_inconsistencias()
import pandas as pd

df = pd.DataFrame(items, columns=COL_INCONSISTENCIAS)
prio = st.multiselect("Prioridade", sorted(df["prioridade"].unique()), default=None)
if prio:
    df = df[df["prioridade"].isin(prio)]
abertas = st.checkbox("Somente em aberto", value=False)
if abertas:
    df = df[~df["resolvida"].astype(str).str.lower().isin(("sim", "s"))]

edited = st.data_editor(
    df,
    use_container_width=True,
    column_config={
        "resolvida": st.column_config.SelectboxColumn(
            options=["Não", "Em andamento", "Sim"]
        ),
    },
)

if st.button("💾 Salvar inconsistências"):
    rows = [tuple(r) for r in edited[COL_INCONSISTENCIAS].to_numpy()]
    salvar_inconsistencias(rows)
    st.success("Salvo.")
