"""Apostolado da Oração – painel principal Streamlit."""
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

st.set_page_config(
    page_title="Apostolado da Oração",
    page_icon="✝️",
    layout="wide",
    initial_sidebar_state="expanded",
)

require_login()

cfg = ler_config()
cor = cfg.get("tema_cor", "#6A1B9A")

st.markdown(
    f"""
<style>
    .main {{ font-size: 1.05rem; }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {cor}22 0%, #f5f0fa 100%);
    }}
    h1, h2, h3 {{ color: {cor}; }}
    div[data-testid="metric-container"] {{
        background: #fff;
        border-left: 4px solid {cor};
        padding: 0.5rem 1rem;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .stButton>button {{
        background-color: {cor};
        color: white;
    }}
</style>
""",
    unsafe_allow_html=True,
)

st.sidebar.title("✝️ Apostolado da Oração")
st.sidebar.caption(cfg.get("paroquia", "Paróquia São Jorge"))
st.sidebar.caption(f"{cfg.get('cidade', 'Nova Odessa')} – {cfg.get('estado', 'SP')}")
st.sidebar.divider()
st.sidebar.markdown("**Navegação** – use o menu acima")
st.sidebar.info(
    "Acesso pela internet: celular, tablet ou PC. "
    "Dados em `data/apostolado.xlsx` com backup automático."
)

st.title("🏠 Início – Apostolado da Oração")
st.caption(
    f"{cfg.get('paroquia')} · {cfg.get('diocese')} · "
    f"Atualizado em {date.today().strftime('%d/%m/%Y')}"
)

membros = ler_membros()
totais = total_por_situacao()
ativos = totais.get("Ativo", 0) + totais.get("Ativo (presumido)", 0)
consagrados = sum(1 for m in membros if str(m[11]).lower() == "sim")
criticas = len(inconsistencias_criticas_abertas())
aniv = aniversariantes_proximos(7)
sem_tel = len(membros_sem_telefone())

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total membros", len(membros))
c2.metric("Ativos", ativos)
c3.metric("Consagrados", consagrados)
c4.metric("Inconsist. críticas", criticas)
c5.metric("Aniv. 7 dias", len(aniv))
c6.metric("Sem telefone", sem_tel)

st.divider()
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📊 Por situação")
    if totais:
        st.bar_chart(totais)
    else:
        st.write("Nenhum membro cadastrado.")

with col_b:
    st.subheader("🎂 Próximos aniversários (30 dias)")
    if aniversariantes_proximos(30):
        for a in aniversariantes_proximos(30)[:8]:
            st.write(
                f"**{a['nome']}** – {a['proximo'].strftime('%d/%m')} "
                f"({a['dias']} dias) · {a['telefone'] or 'sem tel.'}"
            )
    else:
        st.write("Nenhum aniversário nos próximos 30 dias.")

if criticas:
    st.warning("⚠️ Inconsistências críticas em aberto – revise a página Inconsistências.")
    for inc in inconsistencias_criticas_abertas()[:3]:
        st.write(f"• {inc[2]}")

st.divider()
st.markdown(
    f'> *"Que o Sagrado Coração de Jesus reine em nossos lares e em nossa comunidade."*'
)
st.caption(cfg.get("comunidades", ""))
