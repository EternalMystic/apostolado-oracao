"""Tema roxo + branco, alto contraste."""
from __future__ import annotations

import streamlit as st

ROXO = "#4A148C"
ROXO_ESCURO = "#311B92"
BRANCO = "#FFFFFF"


def inject_css(cor: str = ROXO) -> None:
    st.markdown(
        f"""
<style>
    /* Fundo geral: roxo */
    .stApp, [data-testid="stAppViewContainer"] {{
        background: {ROXO_ESCURO} !important;
    }}

    /* Painel principal: branco */
    [data-testid="stAppViewContainer"] .main .block-container {{
        background: {BRANCO} !important;
        border-radius: 14px !important;
        padding: 1.75rem 2rem 2.5rem !important;
        margin: 1rem auto 1.5rem !important;
        max-width: 1080px !important;
        border: 4px solid {BRANCO} !important;
        box-shadow: 0 6px 24px rgba(0,0,0,0.45) !important;
    }}

    /* Texto dentro do painel branco: roxo */
    .main .block-container,
    .main .block-container p,
    .main .block-container label,
    .main .block-container span,
    .main .block-container li,
    .main .block-container td,
    .main .block-container th,
    .main .block-container [data-testid="stMarkdownContainer"] {{
        color: {ROXO} !important;
    }}
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3 {{
        color: {ROXO} !important;
        font-weight: 800 !important;
    }}
    .main .block-container h1 {{ font-size: 2rem !important; }}
    .main .block-container h2 {{ font-size: 1.5rem !important; }}

    /* Sidebar: roxo com texto branco */
    [data-testid="stSidebar"] {{
        background: {ROXO} !important;
        border-right: 4px solid {BRANCO} !important;
    }}
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebarNav"] a,
    [data-testid="stSidebarNav"] span {{
        color: {BRANCO} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: {BRANCO} !important;
        color: {ROXO} !important;
        border-radius: 8px !important;
        font-weight: 800 !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] span {{
        color: {ROXO} !important;
    }}

    /* Botões: roxo + texto branco */
    .stButton > button,
    button[kind="primary"],
    button[kind="secondary"],
    [data-testid="stFormSubmitButton"] button {{
        background: {ROXO} !important;
        color: {BRANCO} !important;
        border: 3px solid {ROXO_ESCURO} !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        min-height: 3rem !important;
        border-radius: 10px !important;
    }}
    .stButton > button p,
    .stButton > button span,
    button[kind="primary"] p,
    button[kind="primary"] span {{
        color: {BRANCO} !important;
    }}

    /* Links / atalhos: branco com borda roxa */
    [data-testid="stPageLink-Button"] {{
        background: {BRANCO} !important;
        color: {ROXO} !important;
        border: 3px solid {ROXO} !important;
        font-weight: 800 !important;
        min-height: 3rem !important;
    }}
    [data-testid="stPageLink-Button"] p,
    [data-testid="stPageLink-Button"] span {{
        color: {ROXO} !important;
    }}

    /* Campos de texto */
    .stTextInput label {{
        color: {ROXO} !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }}
    .stTextInput input {{
        background: {BRANCO} !important;
        color: {ROXO} !important;
        border: 3px solid {ROXO} !important;
        font-size: 1.1rem !important;
    }}

    /* Métricas */
    div[data-testid="metric-container"] {{
        background: {BRANCO} !important;
        border: 3px solid {ROXO} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {ROXO} !important;
        font-weight: 800 !important;
        font-size: 2.25rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {ROXO} !important;
        font-weight: 700 !important;
    }}

    /* Tabelas / editor */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {{
        border: 2px solid {ROXO} !important;
    }}

    .stCaption {{
        color: {ROXO} !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


def inject_login_css() -> None:
    """Login: cartão branco centralizado sobre fundo roxo."""
    st.markdown(
        f"""
<style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background: {ROXO_ESCURO} !important;
    }}
    [data-testid="stAppViewContainer"] .main .block-container {{
        background: {BRANCO} !important;
        max-width: 420px !important;
        margin: 3rem auto !important;
        padding: 2.5rem 2rem !important;
        border: 4px solid {BRANCO} !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5) !important;
    }}
    .main .block-container p,
    .main .block-container label,
    .main .block-container span,
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3 {{
        color: {ROXO} !important;
    }}
    .login-titulo {{
        text-align: center !important;
        font-size: 1.9rem !important;
        font-weight: 800 !important;
        color: {ROXO} !important;
        margin: 0 0 0.35rem 0 !important;
    }}
    .login-sub {{
        text-align: center !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: {ROXO} !important;
        margin: 0 0 1.75rem 0 !important;
    }}
    .stTextInput label {{
        color: {ROXO} !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
    }}
    .stTextInput input {{
        background: {BRANCO} !important;
        color: {ROXO} !important;
        border: 3px solid {ROXO} !important;
    }}
    .stButton > button,
    button[kind="primary"] {{
        background: {ROXO} !important;
        color: {BRANCO} !important;
        border: 3px solid {ROXO_ESCURO} !important;
        font-size: 1.25rem !important;
        font-weight: 800 !important;
        min-height: 3.25rem !important;
    }}
    .stButton > button p,
    .stButton > button span,
    button[kind="primary"] p,
    button[kind="primary"] span {{
        color: {BRANCO} !important;
    }}
    div[data-testid="stAlert"] {{
        color: {ROXO} !important;
        border: 2px solid {ROXO} !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


# Compatibilidade com imports antigos
COR_PADRAO = ROXO


def sidebar_minima(paroquia: str, cidade: str) -> None:
    st.sidebar.markdown(f"## {paroquia}")
    st.sidebar.markdown(cidade)


def atalhos_principais() -> None:
    st.markdown("## Menu rápido")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.page_link("pages/2_🔍_Consulta_Rápida.py", label="Buscar membro", use_container_width=True)
        st.page_link("pages/4_🎂_Aniversários.py", label="Aniversários", use_container_width=True)
    with c2:
        st.page_link("pages/1_📋_Membros.py", label="Membros", use_container_width=True)
        st.page_link("pages/3_🗺️_Rota_de_Visitas.py", label="Rota de visitas", use_container_width=True)
        st.page_link("pages/14_🏠_Visitas.py", label="Visitas", use_container_width=True)
    with c3:
        st.page_link("pages/6_📦_Entregas.py", label="Entregas", use_container_width=True)
        st.page_link("pages/9_📊_Relatórios.py", label="Relatórios", use_container_width=True)


def rodape() -> None:
    st.caption("Paróquia São Jorge · Nova Odessa – SP")
