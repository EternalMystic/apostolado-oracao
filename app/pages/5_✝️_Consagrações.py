"""Registro de consagrações."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import ler_consagracoes, ler_membros, salvar_consagracoes

st.set_page_config(page_title="Consagrações", page_icon="✝️", layout="wide")
require_login()
st.title("✝️ Consagrações")

df = ler_consagracoes()
cons = [m for m in ler_membros() if str(m[11]).lower() == "sim"]
st.metric("Consagrados no cadastro", len(cons))

for m in cons:
    st.write(f"• **{m[2]}** – {m[10]} – {m[12]}")

st.divider()
st.subheader("Registro detalhado")
edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
if st.button("💾 Salvar consagrações"):
    salvar_consagracoes(edited)
    st.success("Salvo.")
