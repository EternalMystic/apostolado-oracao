"""Agenda de reuniões e eventos."""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import ler_agenda, salvar_agenda

st.set_page_config(page_title="Agenda", page_icon="📅", layout="wide")
require_login()
inject_css()
st.title("📅 Agenda Pastoral")

df = ler_agenda()
with st.form("novo_evento"):
    c1, c2 = st.columns(2)
    data_ev = c1.date_input("Data", value=date.today())
    hora = c2.text_input("Hora", "19:30")
    titulo = st.text_input("Título")
    tipo = st.selectbox("Tipo", ["Reunião", "Visita", "Missa", "Formação", "Outro"])
    local = st.text_input("Local", "Paróquia São Jorge")
    responsavel = st.text_input("Responsável")
    if st.form_submit_button("Adicionar"):
        nid = (int(df["id"].max()) + 1) if not df.empty and str(df["id"].max()).isdigit() else 1
        novo = pd.DataFrame(
            [
                {
                    "id": nid,
                    "data": data_ev,
                    "hora": hora,
                    "titulo": titulo,
                    "tipo": tipo,
                    "local": local,
                    "responsavel": responsavel,
                    "observacoes": "",
                }
            ]
        )
        df = pd.concat([df, novo], ignore_index=True)
        salvar_agenda(df)
        st.rerun()

if not df.empty:
    df_sorted = df.sort_values("data")
    st.dataframe(df_sorted, use_container_width=True)

edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
if st.button("💾 Salvar agenda"):
    salvar_agenda(edited)
    st.success("Agenda salva.")
