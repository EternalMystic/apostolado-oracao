"""Visual do Apostolado — webapp responsivo (celular nativo + desktop)."""
from __future__ import annotations

import streamlit as st

COR_PADRAO = "#6A1B9A"
COR_ROXO_ESCURO = "#3E1078"
COR_BRANCO = "#FFFFFF"
COR_TEXTO = "#1A1A1A"
COR_LILAS = "#B388FF"
COR_LILAS_CLARO = "#F3E5F5"

ATALHOS_APP = [
    ("pages/2_🔍_Consulta_Rápida.py", "🔍", "Buscar membro"),
    ("pages/4_🎂_Aniversários.py", "🎂", "Aniversários"),
    ("pages/3_🗺️_Rota_de_Visitas.py", "🗺️", "Rota de visitas"),
    ("pages/1_📋_Membros.py", "📋", "Membros"),
    ("pages/6_📦_Entregas.py", "📦", "Entregas"),
    ("pages/14_🏠_Visitas.py", "🏠", "Visitas"),
    ("pages/7_🙏_Intenções.py", "🙏", "Intenções"),
    ("pages/8_📅_Agenda.py", "📅", "Agenda"),
    ("pages/9_📊_Relatórios.py", "📊", "Relatórios"),
]


def _css_pwa_nativo() -> str:
    return f"""
    /* Sensação de app nativo */
    html {{
        -webkit-text-size-adjust: 100%;
        touch-action: manipulation;
    }}
    .stApp {{
        -webkit-tap-highlight-color: rgba(179, 136, 255, 0.35);
    }}
    [data-testid="stHeader"] {{
        background: transparent !important;
    }}
    @media (max-width: 768px) {{
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"] {{
            min-width: 48px !important;
            min-height: 48px !important;
        }}
        .main .block-container {{
            padding-bottom: max(1.25rem, env(safe-area-inset-bottom)) !important;
        }}
        [data-testid="stPageLink-Button"] {{
            min-height: 3.5rem !important;
            border-radius: 14px !important;
            box-shadow: 0 2px 8px rgba(62, 16, 120, 0.15) !important;
        }}
        [data-testid="stPageLink-Button"]:active {{
            transform: scale(0.98);
            background: {COR_LILAS_CLARO} !important;
        }}
        .stButton > button:active,
        button[kind="primary"]:active {{
            transform: scale(0.98);
        }}
        div[data-testid="metric-container"] {{
            min-height: 4.5rem !important;
        }}
        .dica-app {{
            background: {COR_LILAS_CLARO} !important;
            border: 2px solid {COR_PADRAO} !important;
            border-radius: 12px !important;
            padding: 0.85rem 1rem !important;
            margin-bottom: 1rem !important;
            font-size: 0.95rem !important;
            color: {COR_TEXTO} !important;
        }}
    }}
    @media (min-width: 769px) {{
        .menu-app-desktop {{
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 0.65rem !important;
        }}
    }}
    """


def _css_responsivo() -> str:
    return """
    .stApp,
    [data-testid="stAppViewContainer"],
    .main {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    .main .block-container {
        width: 100% !important;
        max-width: min(1080px, calc(100vw - 1.25rem)) !important;
        padding: clamp(0.85rem, 2.5vw, 2.1rem) clamp(0.75rem, 3vw, 2.1rem) !important;
        margin: clamp(0.4rem, 1.5vw, 1.6rem) auto !important;
        box-sizing: border-box !important;
    }

    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            align-items: stretch !important;
            gap: 0.6rem !important;
            width: 100% !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: 1 1 100% !important;
        }
        .main .block-container h1 {
            font-size: 1.45rem !important;
            line-height: 1.25 !important;
        }
        .main .block-container h2 {
            font-size: 1.2rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.65rem !important;
        }
        div[data-testid="metric-container"] {
            margin-bottom: 0.35rem !important;
        }
        [data-testid="stPageLink-Button"] {
            min-height: 3.5rem !important;
            font-size: 1.08rem !important;
        }
        .stButton > button,
        button[kind="primary"] {
            min-height: 3.25rem !important;
            width: 100% !important;
        }
        [data-testid="stSidebar"] {
            min-width: min(88vw, 300px) !important;
        }
        [data-testid="stSidebarNav"] a {
            font-size: 1.05rem !important;
            padding: 0.5rem 0 !important;
            min-height: 2.75rem !important;
        }
        [data-testid="stDataEditor"] > div,
        [data-testid="stDataFrame"] > div {
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
        }
        [data-testid="stRadio"] > div,
        [data-testid="stSelectbox"] > div {
            width: 100% !important;
        }
        .stTextInput input,
        .stSelectbox select,
        textarea {
            font-size: 16px !important;
        }
    }

    @media (max-width: 480px) {
        .main .block-container {
            border-radius: 12px !important;
            border-width: 2px !important;
        }
        .main .block-container h1 {
            font-size: 1.3rem !important;
        }
    }

    @media (min-width: 769px) and (max-width: 1024px) {
        .main .block-container {
            max-width: min(960px, calc(100vw - 2rem)) !important;
        }
    }

    @media (min-width: 1200px) {
        .main .block-container {
            max-width: 1100px !important;
        }
    }

    @supports (padding: max(0px)) {
        .main .block-container {
            padding-left: max(0.75rem, env(safe-area-inset-left)) !important;
            padding-right: max(0.75rem, env(safe-area-inset-right)) !important;
        }
    }
    """


def inject_pwa_meta(cor: str = COR_PADRAO) -> None:
    """Meta tags para instalar como app na tela inicial do celular."""
    st.markdown(
        f"""
<link rel="manifest" href="app/static/manifest.json">
<link rel="icon" href="app/static/icon-192.svg">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Apostolado">
<meta name="theme-color" content="{cor}">
""",
        unsafe_allow_html=True,
    )


def inject_css(cor: str = COR_PADRAO) -> None:
    inject_pwa_meta(cor)
    try:
        st.html(
            '<meta name="viewport" content="width=device-width, initial-scale=1, '
            'maximum-scale=5, viewport-fit=cover">',
            height=0,
        )
    except Exception:
        pass

    st.markdown(
        f"""
<style>
    .stApp {{
        background: linear-gradient(165deg, {COR_ROXO_ESCURO} 0%, {cor} 45%, #5E35B1 100%) !important;
    }}
    .main .block-container {{
        background: {COR_BRANCO} !important;
        border-radius: 18px !important;
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
        font-size: clamp(1.35rem, 4vw, 2rem) !important;
        color: {cor} !important;
        font-weight: 800 !important;
    }}
    .main .block-container h2 {{
        font-size: clamp(1.15rem, 3vw, 1.5rem) !important;
        color: {cor} !important;
        font-weight: 700 !important;
    }}
    .main .block-container h3 {{
        font-size: clamp(1rem, 2.5vw, 1.25rem) !important;
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
        font-size: clamp(1rem, 2.5vw, 1.15rem) !important;
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
        border-radius: 14px !important;
        min-height: 3.25rem !important;
        font-size: clamp(1rem, 2.5vw, 1.12rem) !important;
        font-weight: 800 !important;
        transition: background 0.12s ease, transform 0.08s ease !important;
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
        font-size: 1.05rem !important;
        font-weight: 700 !important;
    }}
    .stTextInput input {{
        background: {COR_BRANCO} !important;
        color: {COR_TEXTO} !important;
        border: 3px solid {cor} !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
        min-height: 3rem !important;
        width: 100% !important;
    }}

    [data-testid="stMetricValue"] {{
        font-size: clamp(1.5rem, 5vw, 2.4rem) !important;
        color: {cor} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {COR_TEXTO} !important;
        font-weight: 700 !important;
        font-size: clamp(0.8rem, 2vw, 1rem) !important;
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
        width: 100% !important;
        overflow-x: auto !important;
    }}

    .stAlert {{
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}
    .stCaption {{
        color: #555 !important;
    }}

    {_css_responsivo()}
    {_css_pwa_nativo()}
</style>
""",
        unsafe_allow_html=True,
    )


def inject_login_css(cor: str = COR_PADRAO) -> None:
    inject_css(cor)
    st.markdown(
        f"""
<style>
    .main .block-container {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        max-width: min(460px, calc(100vw - 1.5rem)) !important;
        padding-top: clamp(1.5rem, 8vh, 2.5rem) !important;
    }}

    .main .block-container .login-titulo,
    .main .block-container .login-sub,
    p.login-titulo,
    p.login-sub {{
        color: {COR_BRANCO} !important;
    }}
    .login-titulo {{
        text-align: center !important;
        font-size: clamp(1.45rem, 6vw, 2.15rem) !important;
        font-weight: 800 !important;
        margin: 0 0 0.4rem 0 !important;
        text-shadow: 0 2px 12px rgba(0,0,0,0.35) !important;
    }}
    .login-sub {{
        text-align: center !important;
        font-size: clamp(0.9rem, 3.5vw, 1.12rem) !important;
        font-weight: 600 !important;
        margin: 0 0 clamp(1.25rem, 5vw, 2rem) 0 !important;
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
    div[data-testid="stTextInput"] input {{
        font-size: 16px !important;
    }}
    div[data-testid="stButton"] button {{
        min-height: 3.5rem !important;
        font-size: 1.2rem !important;
        width: 100% !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


def dica_app_celular() -> None:
    if "dica_app_vista" not in st.session_state:
        st.session_state.dica_app_vista = True
        st.markdown(
            '<p class="dica-app">📱 <b>No celular:</b> toque <b>☰</b> para o menu. '
            "Para atalho na tela inicial: menu do navegador → "
            "<b>Adicionar à tela inicial</b> / <b>Instalar app</b>.</p>",
            unsafe_allow_html=True,
        )


def sidebar_minima(paroquia: str, cidade: str) -> None:
    st.sidebar.markdown(f"## {paroquia}")
    st.sidebar.markdown(cidade)
    st.sidebar.caption("☰ Menu com todas as páginas")


def atalhos_principais() -> None:
    """Botões grandes estilo app — uma coluna no celular, grade no desktop."""
    st.markdown("## Acesso rápido")
    for path, icone, titulo in ATALHOS_APP:
        st.page_link(path, label=f"{icone}  {titulo}", use_container_width=True)


def rodape() -> None:
    st.caption("Paróquia São Jorge · Nova Odessa – SP")
