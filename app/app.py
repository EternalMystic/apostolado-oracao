"""Apostolado da Oração – painel principal."""
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
from utils.ui import (
    atalhos_principais,
    faixa_titulo,
    inject_css,
    rodape,
    sidebar_ajuda,
)

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

st.sidebar.markdown("## ✝️ Apostolado")
st.sidebar.markdown(f"### {cfg.get('paroquia', 'Paróquia São Jorge')}")
st.sidebar.markdown(f"{cfg.get('cidade', 'Nova Odessa')} – SP")
sidebar_ajuda()

faixa_titulo(
    "Bem-vindo ao Apostolado da Oração",
    f"{cfg.get('diocese', 'Diocese de Limeira')} · {date.today().strftime('%d/%m/%Y')}",
)

atalhos_principais()
st.divider()

membros = ler_membros()
totais = total_por_situacao()
ativos = totais.get("Ativo", 0) + totais.get("Ativo (presumido)", 0)
aniv = aniversariantes_proximos(7)
criticas = len(inconsistencias_criticas_abertas())

st.markdown("### Resumo de hoje")
c1, c2, c3 = st.columns(3)
c1.metric("Membros ativos", ativos)
c2.metric("Aniversários esta semana", len(aniv))
c3.metric("Cadastros sem telefone", len(membros_sem_telefone()))

if aniv:
    st.success("🎂 Aniversariantes nos próximos 7 dias")
    for a in aniv:
        linha = f"**{a['nome']}** — {a['proximo'].strftime('%d/%m')}"
        if a["dias"] == 0:
            linha += " — **é hoje, parabéns!**"
        else:
            linha += f" — daqui a {a['dias']} dia(s)"
        tel = a.get("telefone") or ""
        if tel and "?" not in tel:
            num = "".join(c for c in tel if c.isdigit())
            linha += f' · [Abrir WhatsApp](https://wa.me/55{num})'
        st.markdown(linha)

if criticas:
    st.warning(
        "Existem **pendências importantes** no cadastro. "
        "No menu à esquerda, abra **Inconsistências**."
    )

rodape()
