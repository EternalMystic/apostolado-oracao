"""Visual do Apostolado — elegante, acolhedor e fácil no celular."""
from __future__ import annotations

import streamlit as st

COR_PADRAO = "#6A1B9A"
COR_ROXO_ESCURO = "#2D0A52"
COR_ROXO_MEDIO = "#4A148C"
COR_BRANCO = "#FFFFFF"
COR_TEXTO = "#1E1B2E"
COR_TEXTO_SUAVE = "#5C5470"
COR_LILAS = "#B388FF"
COR_LILAS_CLARO = "#F3E5F5"
COR_DOURADO = "#C9A227"
COR_SUPERFICIE = "#FAFAFE"

ATALHOS_APP = [
    ("pages/22_📖_Orações.py", "📖", "Orações", "Rosário, ladainhas e devoções"),
    ("pages/2_🔍_Consulta_Rápida.py", "🔍", "Buscar pessoa", "Nome, telefone ou endereço"),
    ("pages/3_🗺️_Rota_de_Visitas.py", "🗺️", "Rota de visitas", "Ordem pelo mapa e GPS"),
    ("pages/1_📋_Membros.py", "📋", "Cadastro", "Membros e endereços"),
    ("pages/15_📿_Espiritualidade.py", "📿", "Espiritualidade", "Oferecimento e formação"),
    ("pages/7_🙏_Intenções.py", "🙏", "Pedidos de oração", "Intenções da comunidade"),
]


def ativar_modo_facil() -> None:
    if "modo_facil" not in st.session_state:
        st.session_state.modo_facil = True


def _fontes_google() -> str:
    return """
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    """


def _css_base(cor: str) -> str:
    return f"""
    {_fontes_google()}
    .stApp, [data-testid="stAppViewContainer"], .main {{
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }}
    .stApp {{
        background:
            radial-gradient(ellipse 120% 80% at 10% -20%, rgba(201,162,39,0.12) 0%, transparent 55%),
            radial-gradient(ellipse 90% 60% at 100% 0%, rgba(179,136,255,0.18) 0%, transparent 50%),
            linear-gradient(165deg, {COR_ROXO_ESCURO} 0%, {cor} 42%, {COR_ROXO_MEDIO} 100%) !important;
    }}
    .main .block-container {{
        width: 100% !important;
        max-width: min(920px, calc(100vw - 1.25rem)) !important;
        padding: clamp(1.1rem, 2.5vw, 2rem) clamp(1rem, 3vw, 2rem) !important;
        margin: clamp(0.75rem, 2vw, 1.75rem) auto !important;
        background: {COR_SUPERFICIE} !important;
        border-radius: 24px !important;
        box-shadow:
            0 1px 0 rgba(255,255,255,0.6) inset,
            0 24px 48px rgba(15,5,30,0.28),
            0 8px 16px rgba(15,5,30,0.12) !important;
        border: 1px solid rgba(179,136,255,0.35) !important;
    }}
    .main .block-container p,
    .main .block-container label,
    .main .block-container span,
    .main .block-container li {{
        color: {COR_TEXTO} !important;
    }}
    .main .block-container h1 {{
        color: {cor} !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.15 !important;
        margin-bottom: 0.5rem !important;
    }}
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4 {{
        color: {COR_ROXO_ESCURO} !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }}
    hr {{
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(106,27,154,0.25), transparent) !important;
        margin: 1.25rem 0 !important;
    }}
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {COR_ROXO_ESCURO} 0%, {cor} 100%) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
    }}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] a {{
        color: {COR_BRANCO} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebarNav"] a {{
        border-radius: 10px !important;
        margin: 2px 0 !important;
        transition: background 0.15s ease !important;
    }}
    [data-testid="stSidebarNav"] a:hover {{
        background: rgba(255,255,255,0.12) !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: rgba(255,255,255,0.18) !important;
        font-weight: 700 !important;
    }}
    .stButton > button,
    button[kind="primary"],
    [data-testid="stFormSubmitButton"] button {{
        background: linear-gradient(135deg, {cor} 0%, {COR_ROXO_MEDIO} 100%) !important;
        color: {COR_BRANCO} !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 14px rgba(74,20,140,0.35) !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease !important;
    }}
    .stButton > button:hover,
    button[kind="primary"]:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(74,20,140,0.42) !important;
    }}
    .stButton > button[kind="secondary"] {{
        background: {COR_BRANCO} !important;
        color: {cor} !important;
        border: 2px solid rgba(106,27,154,0.35) !important;
        box-shadow: 0 2px 8px rgba(15,5,30,0.06) !important;
    }}
    [data-testid="stPageLink-Button"],
    a[data-testid="stLinkButton"],
    .stLinkButton > a {{
        background: {COR_BRANCO} !important;
        color: {COR_ROXO_ESCURO} !important;
        border: 1px solid rgba(106,27,154,0.2) !important;
        border-radius: 16px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 10px rgba(15,5,30,0.06) !important;
        transition: transform 0.12s ease, box-shadow 0.12s ease, border-color 0.12s ease !important;
    }}
    [data-testid="stPageLink-Button"]:hover,
    a[data-testid="stLinkButton"]:hover {{
        transform: translateY(-2px) !important;
        border-color: {cor} !important;
        box-shadow: 0 8px 24px rgba(106,27,154,0.18) !important;
    }}
    .stTextInput input,
    .stSelectbox > div > div,
    textarea {{
        border: 2px solid rgba(106,27,154,0.22) !important;
        border-radius: 12px !important;
        background: {COR_BRANCO} !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }}
    .stTextInput input:focus,
    textarea:focus {{
        border-color: {cor} !important;
        box-shadow: 0 0 0 3px rgba(106,27,154,0.15) !important;
    }}
    div[data-testid="metric-container"] {{
        background: linear-gradient(145deg, {COR_BRANCO} 0%, {COR_LILAS_CLARO} 100%) !important;
        border: 1px solid rgba(106,27,154,0.18) !important;
        border-radius: 16px !important;
        padding: 0.85rem 1rem !important;
        box-shadow: 0 4px 12px rgba(15,5,30,0.05) !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {cor} !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {COR_TEXTO_SUAVE} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stAlert"] {{
        border-radius: 14px !important;
        border: none !important;
        box-shadow: 0 2px 10px rgba(15,5,30,0.06) !important;
    }}
    [data-testid="stExpander"] {{
        border: 1px solid rgba(106,27,154,0.15) !important;
        border-radius: 14px !important;
        background: {COR_BRANCO} !important;
        overflow: hidden !important;
    }}
    [data-testid="stExpander"] summary {{
        font-weight: 700 !important;
        color: {COR_ROXO_ESCURO} !important;
    }}
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: rgba(106,27,154,0.2) !important;
        border-radius: 16px !important;
        background: {COR_BRANCO} !important;
        box-shadow: 0 2px 12px rgba(15,5,30,0.04) !important;
    }}
    [data-testid="stRadio"] label {{
        font-weight: 600 !important;
    }}
    [data-testid="stCaptionContainer"] p {{
        color: {COR_TEXTO_SUAVE} !important;
        font-size: 0.92rem !important;
    }}
    .hero-inicio {{
        text-align: center;
        padding: 1.5rem 1rem 1.25rem;
        margin: -0.25rem 0 1.25rem 0;
        border-radius: 20px;
        background: linear-gradient(135deg, {COR_ROXO_ESCURO} 0%, {cor} 55%, #7B1FA2 100%);
        color: white;
        box-shadow: 0 12px 32px rgba(45,10,82,0.35);
        position: relative;
        overflow: hidden;
    }}
    .hero-inicio::before {{
        content: '';
        position: absolute;
        top: -40%;
        right: -15%;
        width: 55%;
        height: 140%;
        background: radial-gradient(circle, rgba(201,162,39,0.22) 0%, transparent 70%);
        pointer-events: none;
    }}
    .hero-badge {{
        display: inline-block;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: rgba(255,255,255,0.85);
        margin-bottom: 0.5rem;
    }}
    .hero-inicio h1 {{
        color: white !important;
        font-size: 1.65rem !important;
        margin: 0 0 0.35rem 0 !important;
        position: relative;
    }}
    .hero-inicio p {{
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
        position: relative;
    }}
    .secao-titulo {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.5rem 0 0.85rem 0;
        font-size: 1.15rem;
        font-weight: 800;
        color: {COR_ROXO_ESCURO};
    }}
    .secao-titulo::after {{
        content: '';
        flex: 1;
        height: 2px;
        background: linear-gradient(90deg, rgba(106,27,154,0.35), transparent);
        border-radius: 2px;
    }}
    .menu-atalho-desc {{
        display: block;
        font-size: 0.82rem;
        font-weight: 500;
        color: {COR_TEXTO_SUAVE};
        margin-top: 0.15rem;
    }}
    .sidebar-marca {{
        text-align: center;
        padding: 0.5rem 0 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 0.75rem;
    }}
    .sidebar-marca h2 {{
        color: white !important;
        font-size: 1.05rem !important;
        margin: 0 !important;
        line-height: 1.3 !important;
    }}
    .sidebar-marca p {{
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.88rem !important;
        margin: 0.25rem 0 0 0 !important;
    }}
    .visita-card {{
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        background: linear-gradient(135deg, {COR_BRANCO} 0%, {COR_LILAS_CLARO} 100%);
        border: 1px solid rgba(106,27,154,0.2);
        border-radius: 18px;
        padding: 1rem 1.15rem;
        margin-bottom: 0.65rem;
        box-shadow: 0 4px 14px rgba(15,5,30,0.06);
    }}
    .visita-num {{
        flex-shrink: 0;
        width: 2.75rem;
        height: 2.75rem;
        line-height: 2.75rem;
        text-align: center;
        border-radius: 50%;
        background: linear-gradient(135deg, {cor} 0%, {COR_ROXO_MEDIO} 100%);
        color: white;
        font-weight: 800;
        font-size: 1.15rem;
        box-shadow: 0 4px 12px rgba(106,27,154,0.35);
    }}
    .visita-body h4 {{
        margin: 0 0 0.3rem 0 !important;
        font-size: 1.12rem !important;
        color: {COR_ROXO_ESCURO} !important;
    }}
    .visita-body p {{
        margin: 0 !important;
        color: {COR_TEXTO_SUAVE} !important;
        font-size: 0.98rem !important;
        line-height: 1.45 !important;
    }}
    .visita-km {{
        display: inline-block;
        margin-top: 0.45rem;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        background: rgba(106,27,154,0.1);
        color: {cor};
        font-size: 0.82rem;
        font-weight: 700;
    }}
    .barra-excel-box {{
        background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%) !important;
        border: 1px solid rgba(27,94,32,0.25) !important;
        border-radius: 18px !important;
        padding: 1rem 1rem !important;
        margin: 1rem 0 1.25rem 0 !important;
        box-shadow: 0 4px 14px rgba(27,94,32,0.08) !important;
    }}
    .barra-excel-box h3 {{
        color: #1B5E20 !important;
        font-size: 1.1rem !important;
        margin: 0 0 0.65rem 0 !important;
        font-weight: 800 !important;
    }}
    .barra-excel-box .stDownloadButton > button {{
        background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%) !important;
        color: white !important;
        border: none !important;
        min-height: 3.5rem !important;
        font-weight: 700 !important;
    }}
    .barra-excel-box .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%) !important;
        border: none !important;
        min-height: 3.5rem !important;
    }}
    .destaque-papa {{
        background: linear-gradient(135deg, {COR_LILAS_CLARO} 0%, {COR_BRANCO} 100%);
        border-left: 4px solid {COR_DOURADO};
        border-radius: 0 14px 14px 0;
        padding: 0.85rem 1rem;
        margin: 0.75rem 0;
    }}
    .destaque-papa p {{
        margin: 0 !important;
        line-height: 1.5 !important;
    }}
    @media (max-width: 768px) {{
        [data-testid="stHorizontalBlock"] {{
            flex-direction: column !important;
            gap: 0.65rem !important;
        }}
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
            width: 100% !important;
            min-width: 100% !important;
        }}
        .hero-inicio h1 {{
            font-size: 1.4rem !important;
        }}
        [data-testid="stSidebarNav"] a {{
            font-size: 1rem !important;
            min-height: 2.75rem !important;
        }}
    }}
    """


def _css_idoso() -> str:
    return """
    .main .block-container p,
    .main .block-container label,
    .main .block-container span,
    .main .block-container li,
    .stTextInput label,
    .stSelectbox label {
        font-size: 1.12rem !important;
        line-height: 1.45 !important;
    }
    .main .block-container h1 {
        font-size: 1.65rem !important;
    }
    .main .block-container h2 {
        font-size: 1.35rem !important;
    }
    .stButton > button,
    button[kind="primary"],
    [data-testid="stFormSubmitButton"] button,
    .stLinkButton > a,
    a[data-testid="stLinkButton"] {
        min-height: 3.5rem !important;
        font-size: 1.1rem !important;
        padding: 0.6rem 1rem !important;
    }
    [data-testid="stPageLink-Button"] {
        min-height: 3.75rem !important;
        font-size: 1.08rem !important;
    }
    .stTextInput input,
    .stSelectbox > div > div,
    textarea {
        font-size: 17px !important;
        min-height: 3rem !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.85rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.98rem !important;
    }
    .visita-body h4 {
        font-size: 1.2rem !important;
    }
    .visita-body p {
        font-size: 1.05rem !important;
    }
    div[data-baseweb="toast"] {
        font-size: 1.05rem !important;
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
    {_css_base(cor)}
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
    {_fontes_google()}
    .stApp {{
        font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
        background:
            radial-gradient(ellipse 80% 60% at 50% -10%, rgba(201,162,39,0.15) 0%, transparent 60%),
            linear-gradient(165deg, {COR_ROXO_ESCURO} 0%, {cor} 50%, {COR_ROXO_MEDIO} 100%) !important;
    }}
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {{
        display: none !important;
    }}
    .main .block-container {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        max-width: 400px !important;
        padding-top: 3rem !important;
    }}
    .main .block-container p,
    .main .block-container label,
    .main .block-container span {{
        color: {COR_BRANCO} !important;
    }}
    .login-emblema {{
        text-align: center;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 4px 12px rgba(0,0,0,0.25));
    }}
    .login-titulo, .login-sub {{
        color: {COR_BRANCO} !important;
        text-align: center !important;
    }}
    .login-titulo {{
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.35rem !important;
        letter-spacing: -0.02em !important;
    }}
    .login-sub {{
        font-size: 1.05rem !important;
        margin-bottom: 2rem !important;
        opacity: 0.9;
    }}
    .login-linha {{
        width: 48px;
        height: 3px;
        background: linear-gradient(90deg, transparent, {COR_DOURADO}, transparent);
        margin: 0 auto 1.75rem auto;
        border-radius: 2px;
    }}
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
        border: 2px solid rgba(179,136,255,0.5) !important;
        border-radius: 14px !important;
        min-height: 3.5rem !important;
        font-size: 1.15rem !important;
        padding: 0.75rem 1rem !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.18) !important;
    }}
    div[data-testid="stTextInput"] input:focus {{
        border-color: {COR_DOURADO} !important;
        box-shadow: 0 8px 28px rgba(0,0,0,0.22), 0 0 0 3px rgba(201,162,39,0.25) !important;
    }}
    div[data-testid="stTextInput"] input::placeholder {{
        color: #888 !important;
    }}
    div[data-testid="stButton"] > button {{
        background: {COR_BRANCO} !important;
        color: {cor} !important;
        border: none !important;
        min-height: 3.75rem !important;
        font-size: 1.2rem !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2) !important;
        letter-spacing: 0.04em !important;
    }}
    div[data-testid="stButton"] > button:hover {{
        background: {COR_LILAS_CLARO} !important;
        transform: translateY(-1px);
    }}
    [data-testid="stAlert"] {{
        background: rgba(255,255,255,0.95) !important;
        border-radius: 12px !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


def sidebar_minima(paroquia: str, cidade: str) -> None:
    st.sidebar.markdown(
        f"""
<div class="sidebar-marca">
  <p style="font-size:1.5rem;margin:0;">✝️</p>
  <h2>{paroquia}</h2>
  <p>{cidade}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def hero_inicio(paroquia: str, cidade: str, data_fmt: str) -> None:
    st.markdown(
        f"""
<div class="hero-inicio">
  <div class="hero-badge">Apostolado da Oração</div>
  <h1>{paroquia}</h1>
  <p>{cidade} · {data_fmt}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def secao_titulo(texto: str, icone: str = "") -> None:
    rotulo = f"{icone} {texto}".strip() if icone else texto
    st.markdown(f'<div class="secao-titulo">{rotulo}</div>', unsafe_allow_html=True)


def atalhos_principais() -> None:
    secao_titulo("O que você precisa?", "✨")
    cols = st.columns(2)
    for i, (path, icone, titulo, desc) in enumerate(ATALHOS_APP):
        with cols[i % 2]:
            st.page_link(path, label=f"{icone}  {titulo}", use_container_width=True)
            st.markdown(f'<span class="menu-atalho-desc">{desc}</span>', unsafe_allow_html=True)


def botao_grande(label: str, key: str, *, type_btn: str = "secondary") -> bool:
    return st.button(label, key=key, type=type_btn, use_container_width=True)


def cartao_visita(ordem: int, nome: str, endereco: str, km: str | None = None) -> None:
    km_html = (
        f'<span class="visita-km">{km} km da parada anterior</span>' if km else ""
    )
    st.markdown(
        f"""
<div class="visita-card">
  <div class="visita-num">{ordem}</div>
  <div class="visita-body">
    <h4>{nome}</h4>
    <p>{endereco or "Endereço não cadastrado"}</p>
    {km_html}
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


def destaque_texto(html: str) -> None:
    st.markdown(f'<div class="destaque-papa">{html}</div>', unsafe_allow_html=True)


def rodape() -> None:
    st.markdown(
        """
<div style="text-align:center;margin-top:2rem;padding-top:1rem;
border-top:1px solid rgba(106,27,154,0.12);">
  <p style="color:#5C5470!important;font-size:0.85rem;margin:0;">
    Apostolado da Oração · Paróquia São Jorge
  </p>
</div>
""",
        unsafe_allow_html=True,
    )
