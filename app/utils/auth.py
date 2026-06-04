"""Senha opcional para acesso na nuvem (st.secrets ou variável APP_PASSWORD)."""
from __future__ import annotations

import os

import streamlit as st


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
    """Bloqueia até informar a senha, se APP_PASSWORD estiver definida."""
    senha = _senha_configurada()
    if not senha:
        return
    if st.session_state.get("auth_ok"):
        return

    st.markdown("### Acesso ao Apostolado da Oração")
    st.caption("Paróquia São Jorge · Nova Odessa – SP")
    with st.form("login"):
        entrada = st.text_input("Senha de acesso", type="password")
        if st.form_submit_button("Entrar", type="primary", use_container_width=True):
            if entrada == senha:
                st.session_state.auth_ok = True
                st.rerun()
            else:
                st.error("Senha incorreta.")
    st.info(
        "Peça a senha ao coordenador do Apostolado. "
        "Funciona em celular, tablet e computador pelo navegador."
    )
    st.stop()
