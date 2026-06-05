"""Biblioteca de orações — Rosário tomista, ladainhas e rezas do dia."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import require_login
from utils.oracoes_catolicas import ORACOES, buscar_oracoes, listar_categorias
from utils.ui import inject_css

st.set_page_config(
    page_title="Orações",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed",
)
require_login()
inject_css()

st.markdown(
    """
<style>
.oracao-box {
  background: #F3E5F5;
  border: 3px solid #6A1B9A;
  border-radius: 16px;
  padding: 1.2rem 1.1rem;
  margin: 0.75rem 0 1.25rem 0;
  font-size: 1.2rem;
  line-height: 1.65;
}
.oracao-box p, .oracao-box li { font-size: 1.15rem !important; }
.oracao-box h3 { color: #6A1B9A; font-size: 1.35rem; }
</style>
""",
    unsafe_allow_html=True,
)

st.title("📖 Orações e rezas")

st.markdown(
    "Rosário à **maneira tomista** (mente, corpo, alma e **Espírito Santo** — sem confundir "
    "espírito com alma), **Ladainha da Humildade**, ladainhas, terços e orações do dia."
)

busca = st.text_input("Buscar oração", placeholder="Ex.: humildade, rosário, São José…")
cats = ["Todas"] + listar_categorias()
cat = st.selectbox("Categoria", cats, key="or_cat")

resultados = buscar_oracoes(busca, cat)
st.metric("Orações encontradas", len(resultados))

if not resultados:
    st.markdown("Nenhuma oração com esse filtro. Tente outra palavra ou **Todas** as categorias.")
    st.stop()

titulos = {f"{o['titulo']}  ·  {o['categoria']}": o["id"] for o in resultados}
sel = st.selectbox("Escolha a oração", list(titulos.keys()), key="or_sel")
escolhida = next(o for o in resultados if o["id"] == titulos[sel])

st.markdown(f"### {escolhida['titulo']}")
st.markdown(f"**{escolhida['categoria']}**")

st.markdown('<div class="oracao-box">', unsafe_allow_html=True)
st.markdown(escolhida["texto"])
st.markdown("</div>", unsafe_allow_html=True)

st.divider()
st.markdown("#### Outras orações nesta lista")
for o in resultados:
    if o["id"] == escolhida["id"]:
        continue
    with st.expander(o["titulo"]):
        st.markdown(o["texto"])

st.caption(f"Total no livro de orações: {len(ORACOES)} textos.")
