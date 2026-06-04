"""Entrada com senha — tela simples para 50+."""
from __future__ import annotations

import os

import streamlit as st

from utils.ui import COR_PADRAO, inject_css


def _senha_configurada() -> str | None:
    try:
        p = st.secrets.get("APP_PASSWORD", None)
        if p:
            return str(p).strip()
    except Exception:
        pass
    return os.environ.get("APP_PASSWORD", "").strip() or None


def require_login() -> None:
    senha = _senha_configurada()
    if not senha:
        return
    if st.session_state.get("auth_ok"):
        return

    inject_css(COR_PADRAO)

    st.markdown('<div class="login-wrap">', unsafe_allow_html=True)
    st.markdown(
        """
<div class="cartao-login">
  <h1>✝️ Apostolado da Oração</h1>
  <p class="sub">Paróquia São Jorge · Nova Odessa – SP</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("#### Entrar no sistema")
    st.markdown(
        '<p class="passo"><b>Passo 1:</b> Peça a <b>senha</b> ao coordenador do Apostolado.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="passo"><b>Passo 2:</b> Digite abaixo e toque no botão roxo <b>Entrar</b>.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="passo"><b>No celular:</b> pode favoritar este site no Chrome ou Safari.</p>',
        unsafe_allow_html=True,
    )

    with st.form("login"):
        entrada = st.text_input(
            "Senha",
            type="password",
            placeholder="Digite a senha aqui",
        )
        entrar = st.form_submit_button(
            "✝️  Entrar no sistema",
            type="primary",
            use_container_width=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if entrar:
        if entrada == senha:
            st.session_state.auth_ok = True
            st.rerun()
        st.error("Senha incorreta. Ligue para o coordenador e tente novamente.")

    st.info("Não precisa baixar aplicativo — só abrir no navegador da internet.")
    st.stop()
