"""Visual do Apostolado — foco em idosos e uso no celular."""
from __future__ import annotations

import streamlit as st

COR_PADRAO = "#6A1B9A"
COR_ROXO_ESCURO = "#3E1078"
COR_BRANCO = "#FFFFFF"
COR_TEXTO = "#1A1A1A"
COR_LILAS = "#B388FF"
COR_LILAS_CLARO = "#F3E5F5"

# Só o essencial na tela inicial — menos confusão
ATALHOS_APP = [
    ("pages/22_📖_Orações.py", "📖", "Orações"),
    ("pages/2_🔍_Consulta_Rápida.py", "🔍", "Buscar pessoa"),
    ("pages/3_🗺️_Rota_de_Visitas.py", "🗺️", "Rota de visitas"),
    ("pages/1_📋_Membros.py", "📋", "Cadastro"),
    ("pages/15_📿_Espiritualidade.py", "📿", "Espiritualidade"),
    ("pages/7_🙏_Intenções.py", "🙏", "Pedidos de oração"),
]


def ativar_modo_facil() -> None:
    if "modo_facil" not in st.session_state:
        st.session_state.modo_facil = True


def _css_idoso() -> str:
    return f"""
    /* Modo fácil — letras grandes, botões altos */
    .main .block-container p,
    .main .block-container label,
    .main .block-container span,
    .main .block-container li,
    .stTextInput label,
    .stSelectbox label {{
        font-size: 1.2rem !important;
        line-height: 1.45 !important;
    }}
    .main .block-container h1 {{
        font-size: 1.75rem !important;
        margin-bottom: 0.75rem !important;
    }}
    .main .block-container h2 {{
        font-size: 1.45rem !important;
    }}
    .stButton > button,
    button[kind="primary"],
    [data-testid="stFormSubmitButton"] button,
    button[kind="formSubmit"],
    .stLinkButton > a,
    a[data-testid="stLinkButton"] {{
        min-height: 3.75rem !important;
        font-size: 1.2rem !important;
        padding: 0.65rem 1rem !important;
        border-radius: 14px !important;
    }}
    [data-testid="stPageLink-Button"] {{
        min-height: 4rem !important;
        font-size: 1.22rem !important;
    }}
    .stTextInput input,
    .stSelectbox > div > div,
    textarea {{
        font-size: 18px !important;
        min-height: 3.25rem !important;
    }}
    [data-testid="stMetricValue"] {{
        font-size: 2rem !important;
    }}
    [data-testid="stMetricLabel"] {{
        font-size: 1.05rem !important;
    }}
    .cartao-visita {{
        background: {COR_LILAS_CLARO} !important;
        border: 3px solid {COR_PADRAO} !important;
        border-radius: 16px !important;
        padding: 1rem 1.1rem !important;
        margin-bottom: 0.85rem !important;
    }}
    .cartao-visita h3 {{
        color: {COR_PADRAO} !important;
        font-size: 1.35rem !important;
        margin: 0 0 0.35rem 0 !important;
    }}
    .cartao-visita p {{
        font-size: 1.15rem !important;
        margin: 0.2rem 0 !important;
    }}
    .barra-excel-box {{
        background: #E8F5E9 !important;
        border: 4px solid #1B5E20 !important;
        border-radius: 16px !important;
        padding: 1rem 0.85rem !important;
        margin: 1rem 0 1.25rem 0 !important;
    }}
    .barra-excel-box h3 {{
        color: #1B5E20 !important;
        font-size: 1.35rem !important;
        margin: 0 0 0.65rem 0 !important;
        font-weight: 800 !important;
    }}
    .barra-excel-box .stDownloadButton > button {{
        background: #1565C0 !important;
        color: white !important;
        border: 3px solid #0D47A1 !important;
        min-height: 4.25rem !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
    }}
    .barra-excel-box .stButton > button[kind="primary"] {{
        background: #2E7D32 !important;
        border: 3px solid #1B5E20 !important;
        min-height: 4.5rem !important;
        font-size: 1.25rem !important;
    }}
    .numero-visita {{
        display: inline-block;
        background: {COR_PADRAO};
        color: white;
        font-weight: 800;
        font-size: 1.4rem;
        width: 2.5rem;
        height: 2.5rem;
        line-height: 2.5rem;
        text-align: center;
        border-radius: 50%;
        margin-right: 0.5rem;
    }}
    /* Menos ruído visual */
    [data-testid="stCaptionContainer"] {{
        display: none !important;
    }}
    div[data-baseweb="toast"] {{
        font-size: 1.1rem !important;
    }}
    @media (max-width: 768px) {{
        .main .block-container h1 {{
            font-size: 1.55rem !important;
        }}
        [data-testid="stSidebarNav"] a {{
            font-size: 1.15rem !important;
            min-height: 3rem !important;
        }}
        .menu-app-mobile .stPageLink {{
            margin-bottom: 0.35rem !important;
        }}
    }}
    """


def _css_responsivo() -> str:
    return """
    .stApp, [data-testid="stAppViewContainer"], .main {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    .main .block-container {
        width: 100% !important;
        max-width: min(1080px, calc(100vw - 1rem)) !important;
        padding: clamp(1rem, 2.5vw, 2rem) clamp(0.85rem, 3vw, 2rem) !important;
        margin: clamp(0.5rem, 1.5vw, 1.5rem) auto !important;
    }
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 0.65rem !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
        }
    }
    """


def inject_pwa_meta(cor: str = COR_PADRAO) -> None:
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
    ativar_modo_facil()
    inject_pwa_meta(cor)
    try:
        st.html(
            '<meta name="viewport" content="width=device-width, initial-scale=1, '
            'maximum-scale=5, viewport-fit=cover">',
            height=0,
        )
    except Exception:
        pass

    idoso = _css_idoso() if st.session_state.get("modo_facil", True) else ""

    st.markdown(
        f"""
<style>
    .stApp {{
        background: linear-gradient(165deg, {COR_ROXO_ESCURO} 0%, {cor} 50%, #5E35B1 100%) !important;
    }}
    .main .block-container {{
        background: {COR_BRANCO} !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 32px rgba(0,0,0,0.22) !important;
        border: 4px solid {COR_LILAS} !important;
    }}
    .main .block-container p, .main .block-container label, .main .block-container span {{
        color: {COR_TEXTO} !important;
    }}
    .main .block-container h1 {{
        color: {cor} !important;
        font-weight: 800 !important;
    }}
    .main .block-container h2, .main .block-container h3 {{
        color: {cor} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] {{
        background: {cor} !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebarNav"] span, [data-testid="stSidebarNav"] a {{
        color: {COR_BRANCO} !important;
        font-weight: 600 !important;
    }}
    .stButton > button, button[kind="primary"] {{
        background: {cor} !important;
        color: {COR_BRANCO} !important;
        font-weight: 800 !important;
        border: 3px solid {COR_ROXO_ESCURO} !important;
    }}
    [data-testid="stPageLink-Button"] {{
        background: {COR_BRANCO} !important;
        color: {cor} !important;
        border: 3px solid {cor} !important;
        font-weight: 800 !important;
    }}
    .stTextInput input {{
        border: 3px solid {cor} !important;
        border-radius: 12px !important;
    }}
    div[data-testid="metric-container"] {{
        background: {COR_LILAS_CLARO} !important;
        border: 3px solid {cor} !important;
        border-radius: 14px !important;
    }}
    {_css_responsivo()}
    {idoso}
</style>
""",
        unsafe_allow_html=True,
    )


def inject_login_css(cor: str = COR_PADRAO) -> None:
    """Tela de login — fundo roxo contínuo, sem cartão branco."""
    ativar_modo_facil()
    inject_pwa_meta(cor)
    st.markdown(
        f"""
<style>
    .stApp {{
        background: linear-gradient(165deg, {COR_ROXO_ESCURO} 0%, {cor} 50%, #5E35B1 100%) !important;
    }}
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {{
        display: none !important;
    }}
    .main .block-container {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        max-width: 420px !important;
        padding-top: 2.5rem !important;
    }}
    .main .block-container p,
    .main .block-container label,
    .main .block-container span {{
        color: {COR_BRANCO} !important;
    }}
    .login-titulo, .login-sub {{
        color: {COR_BRANCO} !important;
        text-align: center !important;
    }}
    .login-titulo {{
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.35rem !important;
    }}
    .login-sub {{
        font-size: 1.15rem !important;
        margin-bottom: 1.75rem !important;
        opacity: 0.95;
    }}
    /* Campo senha — só uma caixa branca, sem moldura extra */
    div[data-testid="stTextInput"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin-bottom: 1rem !important;
    }}
    div[data-testid="stTextInput"] label {{
        display: none !important;
    }}
    div[data-testid="stTextInput"] > div {{
        background: transparent !important;
    }}
    div[data-testid="stTextInput"] input {{
        background: {COR_BRANCO} !important;
        color: {COR_TEXTO} !important;
        border: 3px solid {COR_LILAS} !important;
        border-radius: 14px !important;
        min-height: 3.5rem !important;
        font-size: 1.2rem !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
    }}
    div[data-testid="stTextInput"] input::placeholder {{
        color: #666 !important;
    }}
    div[data-testid="stButton"] > button {{
        background: {COR_BRANCO} !important;
        color: {cor} !important;
        border: 3px solid {COR_LILAS} !important;
        min-height: 3.75rem !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.15) !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        background: {COR_LILAS_CLARO} !important;
    }}
    [data-testid="stAlert"] {{
        background: rgba(255,255,255,0.95) !important;
        border-radius: 12px !important;
    }}
    [data-testid="stCaptionContainer"] {{
        display: none !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


def sidebar_minima(paroquia: str, cidade: str) -> None:
    st.sidebar.markdown(f"## {paroquia}")
    st.sidebar.markdown(cidade)


def atalhos_principais() -> None:
    st.markdown("## O que você precisa?")
    st.markdown('<div class="menu-app-mobile">', unsafe_allow_html=True)
    for path, icone, titulo in ATALHOS_APP:
        st.page_link(path, label=f"{icone}  {titulo}", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


def botao_grande(label: str, key: str, *, type_btn: str = "secondary") -> bool:
    return st.button(label, key=key, type=type_btn, use_container_width=True)


def cartao_visita(ordem: int, nome: str, endereco: str, km: str | None = None) -> None:
    km_txt = f"<p><b>Distância da parada anterior:</b> {km} km</p>" if km else ""
    st.markdown(
        f"""
<div class="cartao-visita">
  <h3><span class="numero-visita">{ordem}</span> {nome}</h3>
  <p>{endereco or "Endereço não cadastrado"}</p>
  {km_txt}
</div>
""",
        unsafe_allow_html=True,
    )


def rodape() -> None:
    pass
