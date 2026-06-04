"""Cadastro e edição de membros."""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import COL_MEMBROS, ler_membros, salvar_membros

st.set_page_config(page_title="Membros", page_icon="📋", layout="wide")
require_login()
inject_css()
st.title("📋 Membros do Apostolado")

membros = ler_membros()
df = pd.DataFrame(membros, columns=COL_MEMBROS)

filtro = st.text_input("Buscar por nome", "")
if filtro:
    df = df[df["nome"].str.contains(filtro, case=False, na=False)]

sit = st.multiselect(
    "Situação",
    sorted(df["situacao"].dropna().unique()),
    default=None,
)
if sit:
    df = df[df["situacao"].isin(sit)]

st.caption(f"{len(df)} registro(s) exibido(s)")
edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "nasc": st.column_config.DateColumn("Nascimento"),
        "ingresso": st.column_config.DateColumn("Ingresso"),
    },
)

if st.button("💾 Salvar alterações", type="primary"):
    rows = []
    for _, r in edited.iterrows():
        nasc = r["nasc"]
        ing = r["ingresso"]
        if pd.notna(nasc) and not isinstance(nasc, date):
            nasc = pd.to_datetime(nasc).date() if pd.notna(nasc) else None
        if pd.notna(ing) and not isinstance(ing, date):
            ing = pd.to_datetime(ing).date() if pd.notna(ing) else None
        rows.append(
            (
                int(r["id"]) if pd.notna(r["id"]) else 0,
                str(r["num_orig"]),
                str(r["nome"]),
                str(r["sexo"]),
                nasc if pd.notna(nasc) else None,
                ing if pd.notna(ing) else None,
                str(r["endereco"]),
                str(r["bairro"]),
                str(r["telefone"]),
                str(r["funcao"]),
                str(r["situacao"]),
                str(r["consagrada"]),
                str(r["observacoes"]),
                str(r["pagina"]),
            )
        )
    salvar_membros(rows)
    st.success("Membros salvos. Backup criado em backups/.")
