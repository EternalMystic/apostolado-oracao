"""Visual limpo, cores nítidas — uso intuitivo sem textos longos."""
from __future__ import annotations

import streamlit as st

COR_PADRAO = "#6A1B9A"
COR_ROXO_ESCURO = "#3E1078"
COR_ROXO_BORDA = "#5E1A9E"
COR_BRANCO = "#FFFFFF"
COR_TEXTO = "#0D0D0D"
COR_TEXTO_SUAVE = "#333333"


def inject_css(cor: str = COR_PADRAO) -> None:
    st.markdown(
        f"""
<style>
    .stApp {{
        background: {COR_ROXO_ESCURO} !important;
    }}
    .main .block-container {{
        background: {COR_BRANCO} !important;
        border-radius: 16px !important;
        padding: 1.75rem 2rem 2.5rem !important;
        margin: 1rem auto 1.5rem !important;
        max-width: 1080px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.35) !important;
        border: 3px solid #B388FF !important;
    }}

    html, body, [class*="css"], p, label, span {{
        color: {COR_TEXTO} !important;
    }}
    h1 {{ font-size: 2rem !important; color: {cor} !important; font-weight: 800 !important; }}
    h2 {{ font-size: 1.5rem !important; color: {cor} !important; font-weight: 700 !important; }}
    h3 {{ font-size: 1.25rem !important; color: {COR_TEXTO} !important; font-weight: 700 !important; }}

    [data-testid="stSidebar"] {{
        background: {cor} !important;
        border-right: 4px solid #B388FF !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
    [data-testid="stSidebarNav"] span {{
        color: {COR_BRANCO} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebarNav"] a {{
        color: {COR_BRANCO} !important;
        font-size: 1.05rem !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: rgba(255,255,255,0.25) !important;
        border-radius: 8px !important;
    }}

    /* Botões normais */
    .stButton > button {{
        background: {cor} !important;
        color: {COR_BRANCO} !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        min-height: 3rem !important;
        border: 3px solid {COR_ROXO_ESCURO} !important;
        border-radius: 10px !important;
    }}

    /* Botão ENTRAR (formulário) — texto sempre visível */
    .stForm button, [data-testid="stFormSubmitButton"] button,
    button[kind="formSubmit"], button[kind="primaryFormSubmit"] {{
        background: {cor} !important;
        color: {COR_BRANCO} !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        min-height: 3.5rem !important;
        border: 3px solid {COR_ROXO_ESCURO} !important;
        border-radius: 10px !important;
    }}

    /* Atalhos do menu principal */
    [data-testid="stPageLink-Button"] {{
        background: {COR_BRANCO} !important;
        color: {cor} !important;
        border: 3px solid {cor} !important;
        border-radius: 12px !important;
        min-height: 3.25rem !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
    }}
    [data-testid="stPageLink-Button"]:hover {{
        background: #F3E5F5 !important;
    }}

    .stTextInput label {{
        color: {COR_TEXTO} !important;
        font-size: 1.15rem !important;
        font-weight: 700 !important;
    }}
    .stTextInput input {{
        background: {COR_BRANCO} !important;
        color: {COR_TEXTO} !important;
        border: 3px solid {cor} !important;
        font-size: 1.15rem !important;
        min-height: 3rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 2.5rem !important;
        color: {cor} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {COR_TEXTO} !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }}
    div[data-testid="metric-container"] {{
        background: #F3E5F5 !important;
        border: 3px solid {cor} !important;
        border-radius: 12px !important;
    }}

    .stAlert {{
        font-size: 1.05rem !important;
        font-weight: 600 !important;
    }}

    .login-tela .block-container {{
        max-width: 440px !important;
        padding: 2rem !important;
    }}
    .login-titulo {{
        text-align: center;
        color: {cor} !important;
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.25rem !important;
    }}
    .login-sub {{
        text-align: center;
        color: {COR_TEXTO_SUAVE} !important;
        font-size: 1.05rem !important;
        margin-bottom: 1.5rem !important;
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
