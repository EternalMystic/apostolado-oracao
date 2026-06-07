"""Visual do Apostolado — neurodesign, acessível e claro no celular."""
from __future__ import annotations

from datetime import datetime

import streamlit as st

COR_PADRAO = "#5B21B6"
COR_ROXO_ESCURO = "#3B0764"
COR_BRANCO = "#FFFFFF"
COR_TEXTO = "#1F2937"
COR_TEXTO_SUAVE = "#4B5563"
COR_LILAS_CLARO = "#EDE9FE"
COR_DOURADO = "#B8860B"
COR_FUNDO = "#F4F1FA"
COR_BORDA = "#DDD6FE"

# Ordem = frequência de uso (menos decisões, mais ação)
ACOES_PRINCIPAIS = [
    ("pages/3_🗺️_Rota_de_Visitas.py", "🗺️", "Rota de visitas", "Sua lista do dia, ordem pelo mapa"),
    ("pages/2_🔍_Consulta_Rápida.py", "🔍", "Buscar pessoa", "Nome, telefone ou endereço"),
    ("pages/22_📖_Orações.py", "📖", "Orações", "Rosário, ladainhas e devoções"),
]

ACOES_SECUNDARIAS = [
    ("pages/1_📋_Membros.py", "📋", "Cadastro", "Membros e endereços"),
    ("pages/7_🙏_Intenções.py", "🙏", "Pedidos de oração", "Intenções da comunidade"),
    ("pages/15_📿_Espiritualidade.py", "📿", "Espiritualidade", "Oferecimento e formação"),
]

OUTRAS_FERRAMENTAS = [
    ("pages/4_🎂_Aniversários.py", "Aniversários"),
    ("pages/5_✝️_Consagrações.py", "Consagrações"),
    ("pages/6_📦_Entregas.py", "Entregas"),
    ("pages/8_📅_Agenda.py", "Agenda"),
    ("pages/9_📊_Relatórios.py", "Relatórios"),
    ("pages/10_⚠️_Inconsistências.py", "Inconsistências"),
    ("pages/11_📜_Memorial.py", "Memorial"),
    ("pages/12_⚙️_Configurações.py", "Configurações"),
    ("pages/13_📝_Instruções.py", "Instruções"),
    ("pages/14_🏠_Visitas.py", "Visitas"),
    ("pages/16_👥_Diretoria.py", "Diretoria"),
    ("pages/17_🏛️_Centros.py", "Centros"),
    ("pages/18_📢_Comunicações.py", "Comunicações"),
    ("pages/19_📒_Atas.py", "Atas"),
    ("pages/20_💬_Sugestões.py", "Sugestões"),
    ("pages/21_🎙️_Reunião_IA.py", "Reunião / ata"),
]


def ativar_modo_facil() -> None:
    if "modo_facil" not in st.session_state:
        st.session_state.modo_facil = True


def _saudacao() -> str:
    h = datetime.now().hour
    if h < 12:
        return "Bom dia"
    if h < 18:
        return "Boa tarde"
    return "Boa noite"


def _fontes() -> str:
    return """
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
    """


def _css_base(cor: str) -> str:
    return f"""
    {_fontes()}
    .stApp, [data-testid="stAppViewContainer"], .main {{
        font-family: 'DM Sans', system-ui, sans-serif !important;
        overflow-x: hidden !important;
    }}
    .stApp {{
        background: {COR_FUNDO} !important;
    }}
    .main .block-container {{
        max-width: min(720px, calc(100vw - 1rem)) !important;
        padding: 1.25rem 1rem 2rem !important;
        margin: 0.75rem auto 1.5rem !important;
        background: {COR_BRANCO} !important;
        border-radius: 20px !important;
        box-shadow: 0 4px 24px rgba(59,7,100,0.08) !important;
        border: 1px solid {COR_BORDA} !important;
    }}
    .main .block-container p,
    .main .block-container label,
    .main .block-container span,
    .main .block-container li {{
        color: {COR_TEXTO} !important;
        line-height: 1.55 !important;
    }}
    .main .block-container h1, .main .block-container h2,
    .main .block-container h3, .main .block-container h4 {{
        color: {COR_ROXO_ESCURO} !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
    }}
    hr {{
        border: none !important;
        height: 1px !important;
        background: {COR_BORDA} !important;
        margin: 1.5rem 0 !important;
    }}

    /* Sidebar — menu completo, mas discreto */
    [data-testid="stSidebar"] {{
        background: {COR_ROXO_ESCURO} !important;
        border-right: none !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1rem !important;
    }}
    [data-testid="stSidebarNav"] {{
        padding-top: 0.5rem !important;
    }}
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] a {{
        color: rgba(255,255,255,0.92) !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }}
    [data-testid="stSidebarNav"] a {{
        border-radius: 8px !important;
        padding: 0.45rem 0.65rem !important;
        margin: 1px 0 !important;
    }}
    [data-testid="stSidebarNav"] a[aria-current="page"] {{
        background: rgba(255,255,255,0.15) !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebarCollapseButton"] {{
        color: white !important;
    }}

    /* Botões — contraste garantido (corrige tema Streamlit) */
    .stButton > button,
    button[kind="primary"],
    [data-testid="stFormSubmitButton"] button {{
        background: {cor} !important;
        color: {COR_BRANCO} !important;
        -webkit-text-fill-color: {COR_BRANCO} !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 12px !important;
        min-height: 3.25rem !important;
        box-shadow: 0 2px 8px rgba(91,33,182,0.25) !important;
    }}
    .stButton > button[kind="secondary"] {{
        background: {COR_BRANCO} !important;
        color: {cor} !important;
        -webkit-text-fill-color: {cor} !important;
        border: 2px solid {COR_BORDA} !important;
        box-shadow: none !important;
    }}
    [data-testid="stPageLink-Button"],
    a[data-testid="stLinkButton"],
    .stLinkButton > a {{
        background: {COR_LILAS_CLARO} !important;
        color: {COR_ROXO_ESCURO} !important;
        -webkit-text-fill-color: {COR_ROXO_ESCURO} !important;
        border: 2px solid {COR_BORDA} !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 3rem !important;
    }}

    .stTextInput input, .stSelectbox > div > div, textarea {{
        border: 2px solid {COR_BORDA} !important;
        border-radius: 12px !important;
        background: {COR_BRANCO} !important;
        color: {COR_TEXTO} !important;
    }}
    [data-testid="stAlert"] {{
        border-radius: 12px !important;
        border-left-width: 4px !important;
    }}
    [data-testid="stExpander"] {{
        border: 1px solid {COR_BORDA} !important;
        border-radius: 12px !important;
        background: {COR_FUNDO} !important;
    }}

    /* Hero acolhedor */
    .hero-inicio {{
        text-align: center;
        padding: 1.75rem 1.25rem;
        margin-bottom: 1.75rem;
        border-radius: 16px;
        background: linear-gradient(145deg, {COR_ROXO_ESCURO} 0%, {cor} 100%);
        color: white;
    }}
    .hero-saudacao {{
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 0 0.35rem 0;
        color: white !important;
    }}
    .hero-paroquia {{
        font-size: 1.05rem;
        margin: 0 0 0.25rem 0;
        color: rgba(255,255,255,0.95) !important;
        font-weight: 600;
    }}
    .hero-data {{
        font-size: 0.95rem;
        margin: 0;
        color: rgba(255,255,255,0.75) !important;
    }}

    /* Seções — hierarquia clara */
    .secao-label {{
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: {COR_TEXTO_SUAVE} !important;
        margin: 0 0 0.75rem 0;
    }}
    .secao-dica {{
        font-size: 1rem;
        color: {COR_TEXTO_SUAVE} !important;
        margin: -0.25rem 0 1rem 0;
        line-height: 1.5 !important;
    }}

    /* Cards de ação — padrão repetível (Gestalt) */
    .acao-card {{
        background: {COR_BRANCO};
        border: 2px solid {COR_BORDA};
        border-radius: 16px;
        padding: 1.1rem 1.15rem 0.5rem;
        margin-bottom: 0.5rem;
        min-height: 7.5rem;
    }}
    .acao-card--destaque {{
        border-color: {cor};
        background: linear-gradient(180deg, {COR_LILAS_CLARO} 0%, {COR_BRANCO} 100%);
        box-shadow: 0 4px 16px rgba(91,33,182,0.12);
    }}
    .acao-emoji {{
        font-size: 2rem;
        line-height: 1;
        margin-bottom: 0.5rem;
        display: block;
    }}
    .acao-titulo {{
        font-size: 1.15rem;
        font-weight: 700;
        color: {COR_ROXO_ESCURO};
        margin: 0 0 0.25rem 0;
        line-height: 1.25;
    }}
    .acao-desc {{
        font-size: 0.95rem;
        color: {COR_TEXTO_SUAVE};
        margin: 0;
        line-height: 1.4;
    }}

    /* Métricas — escaneáveis */
    .metricas-grid {{
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 0.75rem;
        margin: 1.5rem 0;
    }}
    @media (min-width: 640px) {{
        .metricas-grid {{ grid-template-columns: repeat(4, 1fr); }}
    }}
    .metrica-card {{
        background: {COR_FUNDO};
        border: 1px solid {COR_BORDA};
        border-radius: 14px;
        padding: 0.85rem 0.75rem;
        text-align: center;
    }}
    .metrica-icone {{ font-size: 1.35rem; display: block; margin-bottom: 0.25rem; }}
    .metrica-valor {{
        font-size: 1.65rem;
        font-weight: 800;
        color: {cor};
        line-height: 1.1;
        display: block;
    }}
    .metrica-rotulo {{
        font-size: 0.82rem;
        font-weight: 600;
        color: {COR_TEXTO_SUAVE};
        margin-top: 0.2rem;
        display: block;
        line-height: 1.25;
    }}

    .sidebar-marca {{
        padding: 0.25rem 0.75rem 1rem;
        border-bottom: 1px solid rgba(255,255,255,0.12);
        margin-bottom: 0.5rem;
    }}
    .sidebar-marca p {{
        color: rgba(255,255,255,0.85) !important;
        font-size: 0.9rem !important;
        margin: 0.15rem 0 0 0 !important;
        line-height: 1.35 !important;
    }}
    .sidebar-marca strong {{
        color: white !important;
        font-size: 1rem !important;
        display: block;
    }}
    .sidebar-dica {{
        font-size: 0.78rem;
        color: rgba(255,255,255,0.55) !important;
        padding: 0.5rem 0.75rem;
        line-height: 1.4;
    }}

    .visita-card {{
        display: flex;
        gap: 1rem;
        align-items: flex-start;
        background: {COR_FUNDO};
        border: 1px solid {COR_BORDA};
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.65rem;
    }}
    .visita-num {{
        flex-shrink: 0;
        width: 2.5rem;
        height: 2.5rem;
        line-height: 2.5rem;
        text-align: center;
        border-radius: 50%;
        background: {cor};
        color: white;
        font-weight: 800;
        font-size: 1.05rem;
    }}
    .visita-body h4 {{
        margin: 0 0 0.25rem 0 !important;
        font-size: 1.1rem !important;
    }}
    .visita-body p {{
        margin: 0 !important;
        color: {COR_TEXTO_SUAVE} !important;
        font-size: 0.98rem !important;
    }}
    .visita-km {{
        display: inline-block;
        margin-top: 0.4rem;
        padding: 0.15rem 0.6rem;
        border-radius: 999px;
        background: {COR_LILAS_CLARO};
        color: {cor};
        font-size: 0.82rem;
        font-weight: 700;
    }}

    .barra-excel-box {{
        background: #F0FDF4 !important;
        border: 1px solid #BBF7D0 !important;
        border-radius: 14px !important;
        padding: 1rem !important;
        margin: 1rem 0 !important;
    }}
    .barra-excel-box h3 {{
        color: #166534 !important;
        font-size: 1.05rem !important;
        margin: 0 0 0.65rem 0 !important;
    }}

    .destaque-papa {{
        background: {COR_LILAS_CLARO};
        border-left: 4px solid {COR_DOURADO};
        border-radius: 0 12px 12px 0;
        padding: 0.85rem 1rem;
        margin: 1rem 0;
    }}
    .destaque-papa p {{ margin: 0 !important; line-height: 1.5 !important; }}

    .rodape-app p {{
        text-align: center;
        color: {COR_TEXTO_SUAVE} !important;
        font-size: 0.82rem;
        margin: 2rem 0 0 0;
        padding-top: 1rem;
        border-top: 1px solid {COR_BORDA};
    }}

    @media (max-width: 768px) {{
        [data-testid="stHorizontalBlock"] {{
            flex-direction: column !important;
            gap: 0.5rem !important;
        }}
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
            width: 100% !important;
            min-width: 100% !important;
        }}
        .acao-card {{ min-height: auto; }}
    }}
    """


def _css_idoso() -> str:
    return """
    .main .block-container p, .main .block-container label, .main .block-container span {
        font-size: 1.08rem !important;
    }
    .acao-titulo { font-size: 1.22rem !important; }
    .acao-desc { font-size: 1.02rem !important; }
    .stButton > button, button[kind="primary"] {
        min-height: 3.5rem !important;
        font-size: 1.08rem !important;
    }
    .metrica-valor { font-size: 1.85rem !important; }
    .metrica-rotulo { font-size: 0.92rem !important; }
    .hero-saudacao { font-size: 1.65rem !important; }
    """


def inject_pwa_meta(cor: str = COR_PADRAO) -> None:
    st.markdown(
        f"""
<link rel="manifest" href="app/static/manifest.json">
<link rel="icon" href="app/static/icon-192.svg">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="theme-color" content="{cor}">
""",
        unsafe_allow_html=True,
    )


def inject_css(cor: str = COR_PADRAO) -> None:
    ativar_modo_facil()
    inject_pwa_meta(cor)
    idoso = _css_idoso() if st.session_state.get("modo_facil", True) else ""
    st.markdown(f"<style>{_css_base(cor)}{idoso}</style>", unsafe_allow_html=True)


def inject_login_css(cor: str = COR_PADRAO) -> None:
    ativar_modo_facil()
    inject_pwa_meta(cor)
    st.markdown(
        f"""
<style>
    {_fontes()}
    .stApp {{
        font-family: 'DM Sans', system-ui, sans-serif !important;
        background: linear-gradient(160deg, {COR_ROXO_ESCURO} 0%, {cor} 100%) !important;
    }}
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {{ display: none !important; }}
    .main .block-container {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        max-width: 380px !important;
        padding-top: 3rem !important;
    }}
    .login-emblema {{ text-align: center; font-size: 2.75rem; margin-bottom: 0.75rem; }}
    .login-titulo {{
        color: white !important; text-align: center !important;
        font-size: 1.6rem !important; font-weight: 700 !important; margin-bottom: 0.25rem !important;
    }}
    .login-sub {{
        color: rgba(255,255,255,0.85) !important; text-align: center !important;
        font-size: 1rem !important; margin-bottom: 1.75rem !important;
    }}
    div[data-testid="stTextInput"] label {{ display: none !important; }}
    div[data-testid="stTextInput"] input {{
        background: white !important; color: {COR_TEXTO} !important;
        border: 2px solid {COR_BORDA} !important; border-radius: 12px !important;
        min-height: 3.25rem !important; font-size: 1.1rem !important;
    }}
    div[data-testid="stButton"] > button {{
        background: white !important; color: {cor} !important;
        -webkit-text-fill-color: {cor} !important;
        min-height: 3.5rem !important; font-size: 1.15rem !important;
        font-weight: 700 !important; border-radius: 12px !important; border: none !important;
    }}
</style>
""",
        unsafe_allow_html=True,
    )


def sidebar_minima(paroquia: str, cidade: str) -> None:
    st.sidebar.markdown(
        f"""
<div class="sidebar-marca">
  <strong>✝️ {paroquia}</strong>
  <p>{cidade}</p>
</div>
<p class="sidebar-dica">Toque em ☰ para ver todas as páginas.</p>
""",
        unsafe_allow_html=True,
    )


def hero_inicio(paroquia: str, cidade: str, data_fmt: str) -> None:
    st.markdown(
        f"""
<div class="hero-inicio">
  <p class="hero-saudacao">{_saudacao()} 🙏</p>
  <p class="hero-paroquia">{paroquia}</p>
  <p class="hero-data">{cidade} · {data_fmt}</p>
</div>
""",
        unsafe_allow_html=True,
    )


def _cartao_acao(path: str, icone: str, titulo: str, desc: str, key: str, *, destaque: bool = False) -> None:
    classe = "acao-card acao-card--destaque" if destaque else "acao-card"
    st.markdown(
        f"""
<div class="{classe}">
  <span class="acao-emoji">{icone}</span>
  <p class="acao-titulo">{titulo}</p>
  <p class="acao-desc">{desc}</p>
</div>
""",
        unsafe_allow_html=True,
    )
    if st.button("Abrir →", key=key, use_container_width=True, type="primary" if destaque else "secondary"):
        st.switch_page(path)


def atalhos_principais() -> None:
    st.markdown('<p class="secao-label">Passo 1 · o mais usado</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="secao-dica">Escolha uma ação abaixo. Cada card tem um botão <strong>Abrir</strong>.</p>',
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for i, item in enumerate(ACOES_PRINCIPAIS):
        with cols[i]:
            _cartao_acao(*item, key=f"acao_pri_{i}", destaque=True)

    st.markdown('<p class="secao-label" style="margin-top:1.5rem">Passo 2 · cadastro e oração</p>', unsafe_allow_html=True)

    cols2 = st.columns(3)
    for i, item in enumerate(ACOES_SECUNDARIAS):
        with cols2[i]:
            _cartao_acao(*item, key=f"acao_sec_{i}")


def menu_mais_ferramentas() -> None:
    with st.expander("Mais ferramentas (secretaria, relatórios…)"):
        st.caption("Para quem cuida do Excel e da organização do Apostolado.")
        cols = st.columns(2)
        for i, (path, nome) in enumerate(OUTRAS_FERRAMENTAS):
            with cols[i % 2]:
                st.page_link(path, label=nome, use_container_width=True)


def resumo_metricas(itens: list[tuple[str, str, str]]) -> None:
    st.markdown('<p class="secao-label">Resumo de hoje</p>', unsafe_allow_html=True)
    cards = "".join(
        f"""
<div class="metrica-card">
  <span class="metrica-icone">{icone}</span>
  <span class="metrica-valor">{valor}</span>
  <span class="metrica-rotulo">{rotulo}</span>
</div>
"""
        for icone, rotulo, valor in itens
    )
    st.markdown(f'<div class="metricas-grid">{cards}</div>', unsafe_allow_html=True)


def botao_grande(label: str, key: str, *, type_btn: str = "secondary") -> bool:
    return st.button(label, key=key, type=type_btn, use_container_width=True)


def cartao_visita(ordem: int, nome: str, endereco: str, km: str | None = None) -> None:
    km_html = f'<span class="visita-km">{km} km da parada anterior</span>' if km else ""
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
    st.markdown(f'<div class="destaque-papa"><p>{html}</p></div>', unsafe_allow_html=True)


def rodape() -> None:
    st.markdown(
        '<div class="rodape-app"><p>Apostolado da Oração · Paróquia São Jorge</p></div>',
        unsafe_allow_html=True,
    )


# Compatibilidade com código antigo
def secao_titulo(texto: str, icone: str = "") -> None:
    rotulo = f"{icone} {texto}".strip() if icone else texto
    st.markdown(f"#### {rotulo}")
