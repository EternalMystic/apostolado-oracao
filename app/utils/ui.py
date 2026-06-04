"""Visual roxo, legível e simples — público 50+."""
from __future__ import annotations

import streamlit as st

COR_PADRAO = "#6A1B9A"
COR_ROXO_ESCURO = "#4A148C"
COR_ROXO_MEDIO = "#7B1FA2"
COR_ROXO_CLARO = "#EDE7F6"
COR_BRANCO = "#FFFFFF"


def inject_css(cor: str = COR_PADRAO) -> None:
    st.markdown(
        f"""
<style>
    /* Fundo roxo em toda a tela */
    .stApp {{
        background: linear-gradient(165deg, {COR_ROXO_ESCURO} 0%, {cor} 45%, #9C27B0 100%) !important;
    }}
    [data-testid="stAppViewContainer"] > section.main {{
        background: transparent !important;
    }}
    .main .block-container {{
        background: {COR_BRANCO} !important;
        border-radius: 20px !important;
        padding: 2rem 2.5rem 3rem !important;
        margin: 1.25rem auto 2rem !important;
        max-width: 1100px !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.25) !important;
    }}

    html, body, [class*="css"] {{
        font-size: 19px !important;
        line-height: 1.6 !important;
        color: #1a1a1a !important;
    }}
    h1 {{ font-size: 2.1rem !important; color: {cor} !important; font-weight: 700 !important; }}
    h2 {{ font-size: 1.65rem !important; color: {cor} !important; }}
    h3 {{ font-size: 1.35rem !important; color: #333 !important; }}

    /* Sidebar roxa com texto claro */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COR_ROXO_ESCURO} 0%, {cor} 100%) !important;
    }}
    [data-testid="stSidebar"] * {{
        color: #fff !important;
    }}
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {{
        color: #fff !important;
    }}
    [data-testid="stSidebarNav"] {{
        background: rgba(255,255,255,0.08) !important;
        border-radius: 12px !important;
        padding: 0.5rem !important;
    }}
    [data-testid="stSidebarNav"] span, [data-testid="stSidebarNav"] a {{
        font-size: 1.08rem !important;
        font-weight: 500 !important;
    }}

    /* Botões grandes e claros */
    .stButton > button {{
        background: linear-gradient(180deg, {cor} 0%, {COR_ROXO_ESCURO} 100%) !important;
        color: #fff !important;
        font-size: 1.2rem !important;
        min-height: 3.25rem !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(74,20,140,0.35) !important;
    }}
    .stButton > button:hover {{
        filter: brightness(1.08) !important;
    }}

    /* Links de página (atalhos) */
    [data-testid="stPageLink-Button"] {{
        background: {COR_ROXO_CLARO} !important;
        border: 2px solid {cor}44 !important;
        border-radius: 14px !important;
        min-height: 3.5rem !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: {cor} !important;
    }}

    input, textarea, [data-baseweb="select"] > div {{
        font-size: 1.12rem !important;
        border-radius: 10px !important;
    }}
    .stTextInput input {{
        min-height: 3rem !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: 2.4rem !important;
        color: {cor} !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }}
    div[data-testid="metric-container"] {{
        background: {COR_ROXO_CLARO} !important;
        border: 2px solid {cor}33 !important;
        border-radius: 14px !important;
        padding: 1rem 1.25rem !important;
    }}

    /* Alertas legíveis */
    .stAlert {{
        font-size: 1.1rem !important;
        border-radius: 12px !important;
    }}

    /* Login em tela cheia roxa */
    .login-wrap {{
        max-width: 560px;
        margin: 1rem auto 2rem;
        padding: 0;
    }}
    .cartao-login {{
        background: #fff !important;
        border-radius: 20px !important;
        padding: 2.5rem 2rem !important;
        text-align: center !important;
        box-shadow: 0 16px 48px rgba(0,0,0,0.3) !important;
        border: 3px solid rgba(255,255,255,0.5) !important;
    }}
    .cartao-login h1 {{
        font-size: 2rem !important;
        color: {cor} !important;
        margin-bottom: 0.5rem !important;
    }}
    .cartao-login .sub {{
        font-size: 1.15rem !important;
        color: #555 !important;
    }}
    .passo {{
        font-size: 1.12rem !important;
        text-align: left !important;
        margin: 0.65rem 0 !important;
        padding: 0.85rem 1rem !important;
        background: {COR_ROXO_CLARO} !important;
        border-left: 5px solid {cor} !important;
        border-radius: 0 10px 10px 0 !important;
        color: #222 !important;
    }}
    .faixa-titulo {{
        background: linear-gradient(90deg, {cor}, #9C27B0);
        color: #fff !important;
        padding: 1.25rem 1.5rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        text-align: center;
        font-size: 1.35rem;
        font-weight: 700;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }}
    .faixa-titulo * {{ color: #fff !important; }}
</style>
""",
        unsafe_allow_html=True,
    )


def faixa_titulo(texto: str, subtitulo: str = "") -> None:
    sub = f"<br><span style='font-size:1rem;font-weight:400'>{subtitulo}</span>" if subtitulo else ""
    st.markdown(
        f'<div class="faixa-titulo">{texto}{sub}</div>',
        unsafe_allow_html=True,
    )


def sidebar_ajuda() -> None:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Menu")
    st.sidebar.markdown(
        "Toque no **nome da página** abaixo para mudar de tela."
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Dúvida?")
    st.sidebar.markdown(
        "Abra **Instruções** no menu  \n"
        "ou fale com o **coordenador**."
    )


def atalhos_principais() -> None:
    st.markdown("### O que você quer fazer?")
    st.caption("Toque no botão desejado — letras grandes, fácil de ler.")
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.page_link(
            "pages/2_🔍_Consulta_Rápida.py",
            label="🔍  Buscar um membro pelo nome",
            use_container_width=True,
        )
        st.page_link(
            "pages/4_🎂_Aniversários.py",
            label="🎂  Ver aniversários do mês",
            use_container_width=True,
        )
        st.page_link(
            "pages/3_🗺️_Rota_de_Visitas.py",
            label="🗺️  Rota de visitas por bairro",
            use_container_width=True,
        )
    with c2:
        st.page_link(
            "pages/1_📋_Membros.py",
            label="📋  Lista completa de membros",
            use_container_width=True,
        )
        st.page_link(
            "pages/6_📦_Entregas.py",
            label="📦  Registrar entregas (camisa, terço…)",
            use_container_width=True,
        )
        st.page_link(
            "pages/13_📝_Instruções.py",
            label="📝  Ajuda — passo a passo",
            use_container_width=True,
        )


def rodape() -> None:
    st.markdown("---")
    st.caption(
        "Apostolado da Oração · Paróquia São Jorge · Nova Odessa – SP  \n"
        "Sagrado Coração de Jesus, confiamos em Vós."
    )
