"""Entrada por senha."""
from __future__ import annotations

import os

import streamlit as st

from utils.ui import inject_login_css


def _senha_configurada() -> str | None:
    try:
        p = st.secrets.get("APP_PASSWORD", None)
        if p:
            return str(p).strip()
    except Exception:
        pass
    return os.environ.get("APP_PASSWORD", "").strip() or None


def _aviso_excel_se_recuperado() -> None:
    from utils.data_manager import mostrar_aviso_recuperacao_excel

    mostrar_aviso_recuperacao_excel()


def require_login() -> None:
    senha = _senha_configurada()
    if not senha:
        _aviso_excel_se_recuperado()
        return
    if st.session_state.get("auth_ok"):
        _aviso_excel_se_recuperado()
        return

    inject_login_css()

    st.markdown(
        '<p class="login-titulo">✝️ Apostolado da Oração</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="login-sub">Paróquia São Jorge · Nova Odessa – SP</p>',
        unsafe_allow_html=True,
    )

    entrada = st.text_input("Senha", type="password", placeholder="Digite a senha")
    if st.button("ENTRAR", type="primary", use_container_width=True):
        if entrada == senha:
            st.session_state.auth_ok = True
            st.rerun()
        st.error("Senha incorreta.")

    st.stop()
