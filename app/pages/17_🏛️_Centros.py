"""Centros pastorais do Apostolado na paróquia."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import tabela_crud
from utils.data_manager import ler_centros, ler_membros_df, listar_comunidades, salvar_centros
from utils.opcoes import ATIVO_SN
from utils.tabelas_apostolado import COL_CENTROS

st.set_page_config(page_title="Centros", page_icon="🏛️", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("🏛️ Centros Pastorais")

st.caption("Pode haver mais de um centro na paróquia (matriz, comunidades, capelas).")

tabela_crud(
    chave="centros",
    colunas=COL_CENTROS,
    carregar=ler_centros,
    salvar=salvar_centros,
    column_config={
        "comunidade": st.column_config.SelectboxColumn(
            options=listar_comunidades() or ["Matriz"]
        ),
        "ativo": st.column_config.SelectboxColumn(options=ATIVO_SN),
    },
    id_col="id",
    altura=350,
)

st.divider()
st.subheader("Membros por comunidade")
com = st.selectbox("Comunidade", ["Todas"] + listar_comunidades())
df = ler_membros_df()
if com != "Todas" and not df.empty and "comunidade" in df.columns:
    df = df[df["comunidade"].astype(str).str.contains(com, case=False, na=False)]
st.metric("Membros", len(df))
if not df.empty:
    st.dataframe(
        df[["id", "nome", "bairro", "telefone", "tipo_membro", "situacao"]].head(40),
        use_container_width=True,
        hide_index=True,
    )
