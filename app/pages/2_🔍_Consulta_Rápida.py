"""Busca rápida de membros."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import ler_membros

st.set_page_config(page_title="Consulta Rápida", page_icon="🔍", layout="wide")
require_login()
inject_css()
st.title("🔍 Consulta Rápida")

q = st.text_input("Buscar", placeholder="Nome, telefone ou bairro")
if not q:
    st.stop()

q_lower = q.lower()
resultados = []
for m in ler_membros():
    texto = " ".join(
        str(x) for x in [m[1], m[2], m[6], m[7], m[8], m[10], m[12]] if x
    ).lower()
    if q_lower in texto:
        resultados.append(m)

st.write(f"**{len(resultados)}** resultado(s)")
for m in resultados:
    with st.expander(f"{m[1]} – {m[2]} ({m[10]})"):
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Sexo:** {m[3]}")
            st.write(f"**Nasc.:** {m[4].strftime('%d/%m/%Y') if m[4] else '—'}")
            st.write(f"**Ingresso:** {m[5].strftime('%d/%m/%Y') if m[5] else '—'}")
            st.write(f"**Consagrada:** {m[11]}")
        with c2:
            st.write(f"**Endereço:** {m[6] or '—'}")
            st.write(f"**Bairro:** {m[7] or '—'}")
            st.write(f"**Telefone:** {m[8] or '—'}")
            st.write(f"**Função:** {m[9] or '—'}")
        st.write(f"**Obs.:** {m[12]}")
        tel = str(m[8]).replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        if tel and tel[0].isdigit():
            st.link_button("WhatsApp", f"https://wa.me/55{tel}")
