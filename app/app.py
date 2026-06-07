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
    contar_zeladores_ativos,
    inconsistencias_criticas_abertas,
    ler_centros,
    ler_config,
    ler_intencoes_papa,
    total_por_situacao,
)
from utils.ui import (
    atalhos_principais,
    destaque_texto,
    hero_inicio,
    inject_css,
    rodape,
    secao_titulo,
    sidebar_minima,
)

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

paroquia = cfg.get("paroquia", "Paróquia São Jorge")
cidade = f"{cfg.get('cidade', 'Nova Odessa')} – SP"

sidebar_minima(paroquia, cidade)

hero_inicio(paroquia, cidade, date.today().strftime("%d/%m/%Y"))

atalhos_principais()

st.divider()
secao_titulo("Resumo do dia", "📊")

totais = total_por_situacao()
ativos = totais.get("Ativo", 0) + totais.get("Ativo (presumido)", 0)
aniv = aniversariantes_proximos(7)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ativos", ativos)
c2.metric("Aniversários (7 dias)", len(aniv))
c3.metric("Zeladores", contar_zeladores_ativos())
c4.metric("Centros", len(ler_centros()))

papa = ler_intencoes_papa()
if not papa.empty:
    ult = papa.sort_values(["ano", "mes"], ascending=False).iloc[0]
    destaque_texto(
        f"<strong>Oração do Papa</strong> ({int(ult['mes'])}/{int(ult['ano'])}): "
        f"{ult.get('titulo', '')}"
    )

if aniv:
    secao_titulo("Próximos aniversários", "🎂")
    for a in aniv:
        linha = f"<strong>{a['nome']}</strong> · {a['proximo'].strftime('%d/%m')}"
        if a["dias"] == 0:
            linha += " · <strong>Hoje 🎉</strong>"
        tel = a.get("telefone") or ""
        if tel and "?" not in tel:
            num = "".join(c for c in tel if c.isdigit())
            linha += f' · <a href="https://wa.me/55{num}" target="_blank">WhatsApp</a>'
        st.markdown(linha, unsafe_allow_html=True)

if inconsistencias_criticas_abertas():
    st.warning("Cadastro com pendências → **Inconsistências** no menu")

rodape()
