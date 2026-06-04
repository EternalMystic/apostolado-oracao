"""Tela de entrada simples (senha opcional na nuvem)."""
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
    env = os.environ.get("APP_PASSWORD", "").strip()
    return env or None


def require_login() -> None:
    senha = _senha_configurada()
    if not senha:
        return
    if st.session_state.get("auth_ok"):
        return

    inject_css(COR_PADRAO)
    st.markdown(
        """
<div class="cartao-login">
  <h1>✝️ Apostolado da Oração</h1>
  <p>Paróquia São Jorge · Nova Odessa – SP</p>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("#### Como entrar (3 passos)")
    st.markdown(
        '<p class="passo"><b>1.</b> Peça a <b>senha</b> ao coordenador do Apostolado.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="passo"><b>2.</b> Digite a senha abaixo e toque em <b>Entrar</b>.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="passo"><b>3.</b> No celular: pode salvar este site nos favoritos do navegador.</p>',
        unsafe_allow_html=True,
    )

    with st.form("login", clear_on_submit=False):
        entrada = st.text_input(
            "Senha de acesso",
            type="password",
            placeholder="Digite aqui",
        )
        entrar = st.form_submit_button(
            "Entrar no sistema",
            type="primary",
            use_container_width=True,
        )
    if entrar:
        if entrada == senha:
            st.session_state.auth_ok = True
            st.rerun()
        else:
            st.error("Senha incorreta. Confira com o coordenador e tente de novo.")

    st.caption("Não precisa instalar nada — só o navegador (Chrome, Edge ou Safari).")
    st.stop()
