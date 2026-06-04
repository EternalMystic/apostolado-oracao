"""Visual e atalhos pensados para pessoas 50+ (leitura fácil, botões grandes)."""
from __future__ import annotations

import streamlit as st

COR_PADRAO = "#6A1B9A"


def inject_css(cor: str = COR_PADRAO) -> None:
    st.markdown(
        f"""
<style>
    html, body, [class*="css"] {{
        font-size: 18px !important;
        line-height: 1.55 !important;
    }}
    h1 {{ font-size: 2rem !important; color: {cor}; }}
    h2 {{ font-size: 1.55rem !important; color: {cor}; }}
    h3 {{ font-size: 1.3rem !important; }}
    .stButton > button {{
        font-size: 1.15rem !important;
        min-height: 3rem !important;
        padding: 0.65rem 1.25rem !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}
    .stTextInput input, .stSelectbox div, .stTextArea textarea {{
        font-size: 1.1rem !important;
        min-height: 2.75rem !important;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 2.2rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 1.05rem !important;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {cor}18 0%, #faf7fc 100%);
    }}
    [data-testid="stSidebarNav"] span {{
        font-size: 1.05rem !important;
    }}
    div[data-testid="metric-container"] {{
        background: #fff;
        border-left: 5px solid {cor};
        padding: 0.75rem 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    .cartao-login {{
        max-width: 520px;
        margin: 2rem auto;
        padding: 2rem 2.25rem;
        background: linear-gradient(145deg, #faf7fc 0%, #fff 100%);
        border: 2px solid {cor}33;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(106,27,154,0.12);
        text-align: center;
    }}
    .cartao-login h1 {{
        font-size: 1.75rem !important;
        margin-bottom: 0.25rem;
    }}
    .cartao-login p {{
        font-size: 1.1rem;
        color: #555;
    }}
    .passo {{
        font-size: 1.05rem;
        text-align: left;
        margin: 0.5rem 0;
        padding: 0.5rem 0.75rem;
        background: #f3e5f5;
        border-radius: 8px;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


def sidebar_ajuda() -> None:
    st.sidebar.markdown("### Como navegar")
    st.sidebar.markdown(
        "1. **Menu à esquerda** — toque no nome da página  \n"
        "2. **Início** — resumo do Apostolado  \n"
        "3. **Consulta** — buscar por nome  \n"
        "4. **Instruções** — ajuda completa"
    )
    st.sidebar.caption("Funciona no celular, tablet e computador.")


def atalhos_principais() -> None:
    """Botões grandes na página inicial."""
    st.subheader("Atalhos — toque para abrir")
    c1, c2 = st.columns(2)
    with c1:
        st.page_link(
            "pages/2_🔍_Consulta_Rápida.py",
            label="Buscar um membro",
            icon="🔍",
            use_container_width=True,
        )
        st.page_link(
            "pages/4_🎂_Aniversários.py",
            label="Ver aniversários",
            icon="🎂",
            use_container_width=True,
        )
        st.page_link(
            "pages/3_🗺️_Rota_de_Visitas.py",
            label="Rota de visitas",
            icon="🗺️",
            use_container_width=True,
        )
    with c2:
        st.page_link(
            "pages/1_📋_Membros.py",
            label="Lista de membros",
            icon="📋",
            use_container_width=True,
        )
        st.page_link(
            "pages/6_📦_Entregas.py",
            label="Controle de entregas",
            icon="📦",
            use_container_width=True,
        )
        st.page_link(
            "pages/13_📝_Instruções.py",
            label="Ajuda — como usar",
            icon="📝",
            use_container_width=True,
        )
