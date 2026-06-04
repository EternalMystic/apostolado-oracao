"""Visual do Apostolado — roxo, branco e leitura confortável."""
from __future__ import annotations

import streamlit as st

COR_PADRAO = "#6A1B9A"
COR_ROXO_ESCURO = "#3E1078"
COR_BRANCO = "#FFFFFF"
COR_TEXTO = "#1A1A1A"
COR_LILAS = "#B388FF"
COR_LILAS_CLARO = "#F3E5F5"


def inject_css(cor: str = COR_PADRAO) -> None:
    st.markdown(
        f"""
<style>
    .stApp {{
        background: linear-gradient(165deg, {COR_ROXO_ESCURO} 0%, {cor} 45%, #5E35B1 100%) !important;
    }}
    .main .block-container {{
        background: {COR_BRANCO} !important;
        border-radius: 18px !important;
        padding: 1.85rem 2.1rem 2.6rem !important;
        margin: 1.1rem auto 1.6rem !important;
        max-width: 1080px !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.28) !important;
        border: 3px solid {COR_LILAS} !important;
    }}

    .main .block-container p,
    .main .block-container label,
    .main .block-container span,
    .main .block-container li {{
        color: {COR_TEXTO} !important;
    }}
    .main .block-container h1 {{
        font-size: 2rem !important;
        color: {cor} !important;
        font-weight: 800 !important;
    }}
    .main .block-container h2 {{
        font-size: 1.5rem !important;
        color: {cor} !important;
        font-weight: 700 !important;
    }}
    .main .block-container h3 {{
        font-size: 1.25rem !important;
        color: {COR_TEXTO} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stSidebar"] {{
        background: {cor} !important;
        border-right: 4px solid {COR_LILAS} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] a {{
        color: {COR_BRANCO} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: rgba(255,255,255,0.22) !important;
        border-radius: 8px !important;
    }}

    .stButton > button,
    button[kind="primary"],
    [data-testid="stFormSubmitButton"] button,
    button[kind="formSubmit"] {{
        background: {cor} !important;
        color: {COR_BRANCO} !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        min-height: 3rem !important;
        border: 3px solid {COR_ROXO_ESCURO} !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(62,16,120,0.35) !important;
    }}
    .stButton > button p,
    .stButton > button span,
    button[kind="primary"] p,
    button[kind="primary"] span {{
        color: {COR_BRANCO} !important;
    }}

    [data-testid="stPageLink-Button"] {{
        background: {COR_BRANCO} !important;
        color: {cor} !important;
        border: 3px solid {cor} !important;
        border-radius: 12px !important;
        min-height: 3.2rem !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        transition: background 0.15s ease !important;
    }}
    [data-testid="stPageLink-Button"]:hover {{
        background: {COR_LILAS_CLARO} !important;
    }}
    [data-testid="stPageLink-Button"] p,
    [data-testid="stPageLink-Button"] span {{
        color: {cor} !important;
    }}

    .stTextInput label {{
        color: {COR_TEXTO} !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }}
    .stTextInput input {{
        background: {COR_BRANCO} !important;
        color: {COR_TEXTO} !important;
        border: 3px solid {cor} !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        min-height: 3rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 2.4rem !important;
        color: {cor} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {COR_TEXTO} !important;
        font-weight: 700 !important;
    }}
    div[data-testid="metric-container"] {{
        background: {COR_LILAS_CLARO} !important;
        border: 3px solid {cor} !important;
        border-radius: 14px !important;
        padding: 0.35rem 0.5rem !important;
    }}

    [data-testid="stDataEditor"],
    [data-testid="stDataFrame"] {{
        border-radius: 10px !important;
        overflow: hidden !important;
    }}

    .stAlert {{
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}
    .stCaption {{
        color: #555 !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


def inject_login_css(cor: str = COR_PADRAO) -> None:
    """Login: título e paróquia em branco no roxo; formulário em cartão branco."""
    inject_css(cor)
    st.markdown(
        f"""
<style>
    .main .block-container {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        max-width: 460px !important;
        padding-top: 2.5rem !important;
    }}

    .main .block-container .login-titulo,
    .main .block-container .login-sub,
    p.login-titulo,
    p.login-sub {{
        color: {COR_BRANCO} !important;
    }}
    .login-titulo {{
        text-align: center !important;
        color: {COR_BRANCO} !important;
        font-size: 2.15rem !important;
        font-weight: 800 !important;
        margin: 0 0 0.4rem 0 !important;
        letter-spacing: 0.02em !important;
        text-shadow: 0 2px 12px rgba(0,0,0,0.35) !important;
    }}
    .login-sub {{
        text-align: center !important;
        font-size: 1.12rem !important;
        font-weight: 600 !important;
        margin: 0 0 2rem 0 !important;
        text-shadow: 0 1px 8px rgba(0,0,0,0.3) !important;
    }}

    div[data-testid="stTextInput"] {{
        background: {COR_BRANCO} !important;
        border-radius: 14px !important;
        padding: 0.75rem 1rem 1.1rem !important;
        border: 3px solid {COR_LILAS} !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2) !important;
    }}
    div[data-testid="stTextInput"] label {{
        color: {cor} !important;
        font-weight: 800 !important;
    }}

    div[data-testid="stButton"] {{
        margin-top: 0.5rem !important;
    }}
    div[data-testid="stButton"] button {{
        border-radius: 12px !important;
        min-height: 3.35rem !important;
        font-size: 1.2rem !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


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
