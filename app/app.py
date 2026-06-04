"""Apostolado da Oração – início."""
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
    membros_sem_telefone,
    total_por_situacao,
)
from utils.ui import atalhos_principais, inject_css, rodape, sidebar_minima

st.set_page_config(
    page_title="Apostolado da Oração",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="auto",
)

require_login()

cfg = ler_config()
cor = cfg.get("tema_cor", "#6A1B9A")
inject_css(cor)

sidebar_minima(
    cfg.get("paroquia", "Paróquia São Jorge"),
    f"{cfg.get('cidade', 'Nova Odessa')} – SP",
)

st.title("Início")
st.markdown(f"**{date.today().strftime('%d/%m/%Y')}**")

atalhos_principais()

totais = total_por_situacao()
ativos = totais.get("Ativo", 0) + totais.get("Ativo (presumido)", 0)
aniv = aniversariantes_proximos(7)

c1, c2, c3 = st.columns(3)
c1.metric("Ativos", ativos)
c2.metric("Aniversários (7 dias)", len(aniv))
c3.metric("Sem telefone", len(membros_sem_telefone()))

if aniv:
    for a in aniv:
        linha = f"**{a['nome']}** · {a['proximo'].strftime('%d/%m')}"
        if a["dias"] == 0:
            linha += " · **Hoje**"
        tel = a.get("telefone") or ""
        if tel and "?" not in tel:
            num = "".join(c for c in tel if c.isdigit())
            linha += f" · [WhatsApp](https://wa.me/55{num})"
        st.markdown(linha)

if inconsistencias_criticas_abertas():
    st.warning("Cadastro com pendências → menu **Inconsistências**")

rodape()
