"""Apostolado da Oração – painel principal (otimizado para 50+)."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

from utils.auth import require_login
from utils.data_manager import (
    aniversariantes_proximos,
    inconsistencias_criticas_abertas,
    ler_config,
    ler_membros,
    membros_sem_telefone,
    total_por_situacao,
)
from utils.ui import atalhos_principais, inject_css, sidebar_ajuda

st.set_page_config(
    page_title="Apostolado da Oração",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_login()

cfg = ler_config()
cor = cfg.get("tema_cor", "#6A1B9A")
inject_css(cor)

st.sidebar.title("✝️ Apostolado")
st.sidebar.markdown(f"**{cfg.get('paroquia', 'Paróquia São Jorge')}**")
st.sidebar.caption(f"{cfg.get('cidade', 'Nova Odessa')} – SP")
sidebar_ajuda()

st.title("Bem-vindo ao Apostolado da Oração")
st.markdown(
    f"**{cfg.get('paroquia', 'Paróquia São Jorge')}** · "
    f"{cfg.get('diocese', 'Diocese de Limeira')} · "
    f"Hoje: {date.today().strftime('%d/%m/%Y')}"
)

atalhos_principais()
st.divider()

membros = ler_membros()
totais = total_por_situacao()
ativos = totais.get("Ativo", 0) + totais.get("Ativo (presumido)", 0)
consagrados = sum(1 for m in membros if str(m[11]).lower() == "sim")
criticas = len(inconsistencias_criticas_abertas())
aniv = aniversariantes_proximos(7)
sem_tel = len(membros_sem_telefone())

st.subheader("Resumo")
c1, c2, c3 = st.columns(3)
c1.metric("Membros ativos", ativos)
c2.metric("Aniversários esta semana", len(aniv))
c3.metric("Sem telefone no cadastro", sem_tel)

if len(aniv) > 0:
    st.success("Aniversariantes nos próximos 7 dias:")
    for a in aniv:
        tel = a.get("telefone") or ""
        linha = f"**{a['nome']}** — {a['proximo'].strftime('%d/%m')}"
        if a["dias"] == 0:
            linha += " — **hoje!**"
        else:
            linha += f" — em {a['dias']} dias"
        if tel and "?" not in tel:
            num = "".join(c for c in tel if c.isdigit())
            linha += f' — [WhatsApp](https://wa.me/55{num})'
        st.markdown(linha)

if criticas:
    st.warning("Há pendências importantes no cadastro. Abra **Inconsistências** no menu.")

st.divider()
st.markdown(
    '> *"Que o Sagrado Coração de Jesus reine em nossos lares e em nossa comunidade."*'
)
