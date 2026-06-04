"""Entrada por senha — uma tela só, sem instruções longas."""
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
    st.markdown('<div class="login-tela">', unsafe_allow_html=True)
    st.markdown(
        '<p class="login-titulo">✝️ Apostolado da Oração</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="login-sub">Paróquia São Jorge · Nova Odessa</p>',
        unsafe_allow_html=True,
    )

    entrada = st.text_input("Senha", type="password", label_visibility="visible")
    if st.button("ENTRAR", type="primary", use_container_width=True):
        if entrada == senha:
            st.session_state.auth_ok = True
            st.rerun()
        st.error("Senha incorreta.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()
