"""Registro de comunicações e envio WhatsApp."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import ler_comunicacoes, ler_config, ler_membros, salvar_comunicacoes
from utils.opcoes import TIPOS_COMUNICACAO
from utils.tabelas_apostolado import COL_COMUNICACOES

st.set_page_config(page_title="Comunicações", page_icon="📢", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("📢 Comunicações")

tabela_crud(
    chave="comunicacoes",
    colunas=COL_COMUNICACOES,
    carregar=ler_comunicacoes,
    salvar=salvar_comunicacoes,
    column_config={
        "data": st.column_config.DateColumn("Data"),
        "tipo": st.column_config.SelectboxColumn(options=TIPOS_COMUNICACAO),
    },
    colunas_data=["data"],
    id_col="id",
    altura=300,
)

st.divider()
st.subheader("WhatsApp rápido")
cfg = ler_config()
msg = st.text_area("Mensagem", "Olá! Lembrete do Apostolado da Oração – Paróquia São Jorge.")
ativos = [
    m
    for m in ler_membros()
    if m.get("situacao") in ("Ativo", "Ativo (presumido)") and str(m.get("telefone", "")).strip()
]
opcoes = {
    f"{m['nome']} ({m.get('telefone')})": m
    for m in ativos
    if "".join(c for c in str(m.get("telefone", "")) if c.isdigit())
}
sel = st.multiselect("Destinatários", list(opcoes.keys()))
if st.button("Abrir links WhatsApp") and sel:
    for nome in sel:
        m = opcoes[nome]
        num = "".join(c for c in str(m.get("telefone", "")) if c.isdigit())
        texto = msg.replace(" ", "%20")
        st.markdown(f"- [{m['nome']}](https://wa.me/55{num}?text={texto})")
elif cfg.get("whatsapp_coordenador"):
    n = "".join(c for c in cfg["whatsapp_coordenador"] if c.isdigit())
    if n:
        st.markdown(f"[WhatsApp do coordenador](https://wa.me/55{n})")
