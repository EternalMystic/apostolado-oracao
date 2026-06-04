"""Espiritualidade AO: oferecimento, intenções do Papa, formação."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import ler_intencoes_papa, salvar_intencoes_papa
from utils.opcoes import DIVULGADA
from utils.tabelas_apostolado import COL_INTENCOES_PAPA, OFERECIMENTO_DIARIO

st.set_page_config(page_title="Espiritualidade", page_icon="📿", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("📿 Espiritualidade do Apostolado")

st.markdown("### Oferecimento diário")
st.markdown(OFERECIMENTO_DIARIO)

st.divider()
st.markdown("### Intenções do Papa (bilhete mensal)")
st.caption("Registre as intenções do mês conforme o Mensageiro do Coração de Jesus.")

tabela_crud(
    chave="intencoes_papa",
    colunas=COL_INTENCOES_PAPA,
    carregar=ler_intencoes_papa,
    salvar=salvar_intencoes_papa,
    column_config={
        "mes": st.column_config.NumberColumn("Mês", min_value=1, max_value=12),
        "ano": st.column_config.NumberColumn("Ano", min_value=2020, max_value=2040),
        "divulgada": st.column_config.SelectboxColumn("Divulgada?", options=DIVULGADA),
    },
    id_col="id",
    altura=280,
)

st.divider()
st.markdown("### Links úteis")
st.markdown(
    """
- [Apostolado da Oração Brasil – MEJ](https://aomej.org.br/)
- [Rede Mundial de Oração do Papa](https://www.popesprayer.va/)
- Manual do Coração de Jesus (Edições Loyola)
"""
)
