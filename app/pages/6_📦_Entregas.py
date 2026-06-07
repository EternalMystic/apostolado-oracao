"""CRUD completo — Entregas."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colunas_ui import montar_column_config
from utils.crud_ui import tabela_crud
from utils.data_manager import COL_ENTREGAS, ler_entregas, salvar_entregas
from utils.dados_membros import ITENS_ENTREGA
from utils.endereco import aplicar_filtro_endereco
from utils.opcoes import ENTREGUE

st.set_page_config(page_title="Entregas", page_icon="📦", layout="wide", initial_sidebar_state="collapsed")
require_login()
inject_css()
st.title("📦 Entregas")


def _filtro(df: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    filtrado = False
    modo = st.session_state.get("ent_f_modo", "Todas")
    if modo == "Pendentes":
        df = df[df["entregue"].astype(str).str.upper() != "S"]
        filtrado = True
    elif modo == "Entregues":
        df = df[df["entregue"].astype(str).str.upper() == "S"]
        filtrado = True
    cep = st.session_state.get("ent_f_cep", "")
    bairro = st.session_state.get("ent_f_bairro", "Todos")
    rua = st.session_state.get("ent_f_rua", "")
    cidade = st.session_state.get("ent_f_cidade", "Todos")
    if cep or bairro != "Todos" or rua or cidade != "Todos":
        mask = df.apply(
            lambda r: aplicar_filtro_endereco(
                r.to_dict(), cep=cep, bairro=bairro, rua=rua, cidade=cidade
            ),
            axis=1,
        )
        df = df[mask]
        filtrado = True
    return df, filtrado


st.radio("Mostrar", ["Todas", "Pendentes", "Entregues"], horizontal=True, key="ent_f_modo")
st.markdown("**Filtrar endereço**")
e1, e2, e3, e4 = st.columns(4)
e1.text_input("CEP", key="ent_f_cep")
base = ler_entregas()
_b = sorted({str(x).strip() for x in base["bairro"].dropna() if str(x).strip()}) if not base.empty else []
e2.selectbox("Bairro", ["Todos"] + _b, key="ent_f_bairro")
e3.text_input("Rua", key="ent_f_rua")
_c = sorted({str(x).strip() for x in base["cidade"].dropna() if str(x).strip()}) if not base.empty else []
e4.selectbox("Cidade", ["Todos"] + _c, key="ent_f_cidade")

tabela_crud(
    chave="entregas",
    colunas=COL_ENTREGAS,
    carregar=ler_entregas,
    salvar=salvar_entregas,
    column_config=montar_column_config(
        COL_ENTREGAS,
        {
            "item": st.column_config.SelectboxColumn("Material / motivo", options=ITENS_ENTREGA),
            "entregue": st.column_config.SelectboxColumn("Entregue?", options=ENTREGUE),
            "data_entrega": st.column_config.DateColumn("Data da entrega"),
        },
    ),
    colunas_data=["data_entrega"],
    id_col="id",
    aplicar_filtro=_filtro,
    altura=450,
    aba_excel="Entregas",
)
