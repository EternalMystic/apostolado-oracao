"""Intenções de oração."""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import ler_intencoes, salvar_intencoes

st.set_page_config(page_title="Intenções", page_icon="🙏", layout="wide")
require_login()
inject_css()
st.title("🙏 Intenções de Oração")

df = ler_intencoes()
with st.form("nova_intencao"):
    data = st.date_input("Data", value=date.today())
    intencao = st.text_area("Intenção")
    solicitante = st.text_input("Solicitante")
    if st.form_submit_button("Adicionar"):
        novo = pd.DataFrame(
            [
                {
                    "id": (int(df["id"].max()) + 1) if not df.empty and df["id"].notna().any() else 1,
                    "data": data,
                    "intencao": intencao,
                    "solicitante": solicitante,
                    "status": "Pendente",
                    "observacoes": "",
                }
            ]
        )
        df = pd.concat([df, novo], ignore_index=True)
        salvar_intencoes(df)
        st.rerun()

edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
if st.button("💾 Salvar intenções"):
    salvar_intencoes(edited)
    st.success("Salvo.")
