"""Busca rápida de membros."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import ler_membros
from utils.endereco import endereco_completo_de_registro, texto_busca_endereco

st.set_page_config(
    page_title="Consulta Rápida",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)
require_login()
inject_css()
st.title("🔍 Consulta Rápida")

q = st.text_input(
    "Buscar membro",
    placeholder="Nome, telefone, CEP, rua, bairro ou cidade",
)
if not q:
    st.stop()

q_lower = q.lower()
resultados = []
for m in ler_membros():
    texto = " ".join(
        str(x)
        for x in [
            m.get("num_orig"),
            m.get("nome"),
            m.get("telefone"),
            m.get("situacao"),
            m.get("observacoes"),
            texto_busca_endereco(m),
        ]
        if x
    ).lower()
    if q_lower in texto:
        resultados.append(m)

st.write(f"**{len(resultados)}** resultado(s)")
for m in resultados:
    with st.expander(f"{m.get('num_orig')} – {m.get('nome')} ({m.get('situacao')})"):
        c1, c2 = st.columns(2)
        with c1:
            st.write(f"**Sexo:** {m.get('sexo') or '—'}")
            nasc = m.get("nasc")
            st.write(f"**Nasc.:** {nasc.strftime('%d/%m/%Y') if nasc else '—'}")
            ing = m.get("ingresso")
            st.write(f"**Ingresso AO:** {ing.strftime('%d/%m/%Y') if ing else '—'}")
            st.write(f"**Consagrada:** {m.get('consagrada') or '—'}")
            st.write(f"**Comunidade:** {m.get('comunidade') or '—'}")
        with c2:
            st.write(f"**CEP:** {m.get('cep') or '—'}")
            st.write(f"**Rua:** {m.get('rua') or '—'}")
            st.write(f"**Número:** {m.get('numero') or '—'}")
            st.write(f"**Bairro:** {m.get('bairro') or '—'}")
            st.write(f"**Cidade:** {m.get('cidade') or '—'}")
            st.write(f"**Telefone:** {m.get('telefone') or '—'}")
            st.write(f"**Função:** {m.get('funcao') or '—'}")
        st.write(f"**Endereço completo:** {endereco_completo_de_registro(m) or '—'}")
        if m.get("observacoes"):
            st.write(f"**Observações:** {m.get('observacoes')}")
        tel = str(m.get("telefone", "")).replace("(", "").replace(")", "").replace(" ", "").replace("-", "")
        if tel and tel[0].isdigit():
            st.link_button("WhatsApp", f"https://wa.me/55{tel}")
