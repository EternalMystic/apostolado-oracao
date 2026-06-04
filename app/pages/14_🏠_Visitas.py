"""CRUD completo — Visitas domiciliares."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colunas_ui import montar_column_config
from utils.crud_ui import tabela_crud
from utils.data_manager import COL_VISITAS, ler_membros, ler_visitas, salvar_visitas
from utils.dados_membros import ITENS_ENTREGA
from utils.endereco import aplicar_filtro_endereco, linha_entrega_visita_de_membro
from utils.opcoes import REALIZADA, TIPOS_VISITA

st.set_page_config(page_title="Visitas", page_icon="🏠", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("🏠 Visitas domiciliares")

membros = {m["id"]: m for m in ler_membros()}


def _filtro(df: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    filtrado = False
    cep = st.session_state.get("vis_f_cep", "")
    bairro = st.session_state.get("vis_f_bairro", "Todos")
    rua = st.session_state.get("vis_f_rua", "")
    cidade = st.session_state.get("vis_f_cidade", "Todos")
    if cep or bairro != "Todos" or rua or cidade != "Todos":
        if not df.empty:
            mask = df.apply(
                lambda r: aplicar_filtro_endereco(
                    r.to_dict(), cep=cep, bairro=bairro, rua=rua, cidade=cidade
                ),
                axis=1,
            )
            df = df[mask]
        filtrado = True
    r = st.session_state.get("vis_f_real", "Todas")
    if r == "Pendentes":
        return df[df["realizada"].astype(str).str.upper() != "S"], True
    if r == "Realizadas":
        return df[df["realizada"].astype(str).str.upper() == "S"], True
    return df, filtrado


if membros and st.button("Gerar visitas para todos os ativos"):
    ativos = [m for m in ler_membros() if m.get("situacao") in ("Ativo", "Ativo (presumido)")]
    rows = []
    for i, m in enumerate(ativos, start=1):
        end = linha_entrega_visita_de_membro(m)
        rows.append(
            {
                "id": i,
                "membro_id": m["id"],
                "membro_nome": m["nome"],
                "data_visita": "",
                **end,
                "item": ITENS_ENTREGA[-1],
                "realizada": "N",
                "tipo_visita": "Visita domiciliar",
                "nota_pastoral": "",
                "observacoes": "",
            }
        )
    salvar_visitas(pd.DataFrame(rows, columns=COL_VISITAS))
    st.session_state.pop("visitas_base", None)
    st.rerun()

st.markdown("**Filtrar endereço**")
v1, v2, v3, v4 = st.columns(4)
v1.text_input("CEP", key="vis_f_cep")
_b = sorted({str(m.get("bairro", "")).strip() for m in membros.values() if m.get("bairro")})
v2.selectbox("Bairro", ["Todos"] + _b, key="vis_f_bairro")
v3.text_input("Rua", key="vis_f_rua")
_c = sorted({str(m.get("cidade", "")).strip() for m in membros.values() if m.get("cidade")})
v4.selectbox("Cidade", ["Todos"] + _c, key="vis_f_cidade")
st.radio("Status da visita", ["Todas", "Pendentes", "Realizadas"], horizontal=True, key="vis_f_real")

tabela_crud(
    chave="visitas",
    colunas=COL_VISITAS,
    carregar=ler_visitas,
    salvar=salvar_visitas,
    column_config=montar_column_config(
        COL_VISITAS,
        {
            "item": st.column_config.SelectboxColumn("Material / motivo", options=ITENS_ENTREGA),
            "realizada": st.column_config.SelectboxColumn("Realizada?", options=REALIZADA),
            "tipo_visita": st.column_config.SelectboxColumn("Tipo de visita", options=TIPOS_VISITA),
            "data_visita": st.column_config.DateColumn("Data da visita"),
        },
    ),
    colunas_data=["data_visita"],
    id_col="id",
    aplicar_filtro=_filtro,
    altura=450,
)
