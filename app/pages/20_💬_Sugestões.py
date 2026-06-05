"""Sugestões e comentários sobre o sistema e o Apostolado."""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import require_login
from utils.crud_ui import proximo_id, tabela_crud
from utils.data_manager import ler_sugestoes, salvar_sugestoes
from utils.opcoes import STATUS_SUGESTAO, TIPOS_SUGESTAO
from utils.tabelas_apostolado import COL_SUGESTOES
from utils.ui import inject_css

st.set_page_config(
    page_title="Sugestões",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="auto",
)
require_login()
inject_css()
st.title("💬 Sugestões e comentários")
st.caption(
    "Espaço aberto para ideias, elogios, dúvidas ou melhorias no app e na pastoral do Apostolado."
)

with st.form("nova_sugestao", clear_on_submit=True):
    c1, c2 = st.columns(2)
    autor = c1.text_input("Seu nome", placeholder="Opcional")
    tipo = c2.selectbox("Tipo", TIPOS_SUGESTAO)
    texto = st.text_area("Mensagem", height=120, placeholder="Descreva sua sugestão ou comentário…")
    enviar = st.form_submit_button("Enviar", type="primary")
    if enviar:
        if not texto.strip():
            st.error("Escreva a mensagem antes de enviar.")
        else:
            df = ler_sugestoes()
            novo = {
                "id": proximo_id(df),
                "data": date.today(),
                "autor": autor.strip(),
                "tipo": tipo,
                "texto": texto.strip(),
                "status": "Nova",
                "resposta": "",
                "observacoes": "",
            }
            salvar_sugestoes(pd.concat([df, pd.DataFrame([novo])], ignore_index=True))
            st.success("Obrigado! Sua mensagem foi registrada.")
            st.rerun()

st.divider()
st.subheader("Todas as mensagens (coordenação)")
tabela_crud(
    chave="sugestoes",
    colunas=COL_SUGESTOES,
    carregar=ler_sugestoes,
    salvar=salvar_sugestoes,
    column_config={
        "data": st.column_config.DateColumn("Data"),
        "tipo": st.column_config.SelectboxColumn(options=TIPOS_SUGESTAO),
        "status": st.column_config.SelectboxColumn(options=STATUS_SUGESTAO),
    },
    colunas_data=["data"],
    id_col="id",
    altura=380,
    aba_excel="Sugestoes",
)
