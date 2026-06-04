"""Diretoria pastoral e zeladores do Apostolado."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import ler_diretoria, ler_membros, ler_zeladores, salvar_diretoria, salvar_zeladores
from utils.opcoes import ATIVO_SN, CARGOS_DIRETORIA
from utils.tabelas_apostolado import COL_DIRETORIA, COL_ZELADORES

st.set_page_config(page_title="Diretoria", page_icon="👥", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("👥 Diretoria e Zeladores")

tab1, tab2 = st.tabs(["Diretoria", "Zeladores"])

with tab1:
    st.caption("Presidente, secretário(a), tesoureiro(a), diretor espiritual — conforme estatutos do AO.")
    tabela_crud(
        chave="diretoria",
        colunas=COL_DIRETORIA,
        carregar=ler_diretoria,
        salvar=salvar_diretoria,
        column_config={
            "cargo": st.column_config.SelectboxColumn(options=CARGOS_DIRETORIA),
            "mandato_inicio": st.column_config.DateColumn("Início mandato"),
            "ativo": st.column_config.SelectboxColumn(options=ATIVO_SN),
        },
        colunas_data=["mandato_inicio"],
        id_col="id",
        altura=320,
    )

with tab2:
    st.caption("Zeladores(as) — vínculo com membros do cadastro.")
    membros = {m[0]: m[2] for m in ler_membros() if m[10] in ("Ativo", "Ativo (presumido)")}
    tabela_crud(
        chave="zeladores",
        colunas=COL_ZELADORES,
        carregar=ler_zeladores,
        salvar=salvar_zeladores,
        column_config={
            "data_posse": st.column_config.DateColumn("Posse"),
            "ativo": st.column_config.SelectboxColumn(options=ATIVO_SN),
        },
        colunas_data=["data_posse"],
        id_col="id",
        altura=320,
    )
    if membros:
        st.markdown("**Membros ativos (referência de ID):**")
        refs = ", ".join(f"{k}={v}" for k, v in list(membros.items())[:15])
        if len(membros) > 15:
            refs += "…"
        st.write(refs)
