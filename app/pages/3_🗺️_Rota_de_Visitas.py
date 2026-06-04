"""Rota de visitas — edição com merge seguro ao filtrar."""
import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.crud_ui import mesclar_por_id
from utils.data_manager import (
    COL_ENTREGAS,
    ler_entregas,
    ler_membros,
    preparar_dataframe,
    preparar_entregas_editor,
    salvar_entregas,
)
from utils.dados_membros import ITENS_ENTREGA, ORDEM_BAIRROS
from utils.opcoes import ENTREGUE

st.set_page_config(page_title="Rota de Visitas", page_icon="🗺️", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("🗺️ Rota de Visitas")


def ordem_bairro(b: str) -> int:
    b = b or ""
    for i, nome in enumerate(ORDEM_BAIRROS):
        if nome and (b.lower() == nome.lower() or nome.lower() in b.lower()):
            return i
    return len(ORDEM_BAIRROS)


def extrair_numero(end: str) -> int:
    m = re.search(r"\b(\d+)\b", end or "")
    return int(m.group(1)) if m else 99999


membros = {m[0]: m for m in ler_membros() if m[10] in ("Ativo", "Ativo (presumido)")}
df_full = ler_entregas()

if df_full.empty and membros:
    rows = []
    for i, m in enumerate(
        sorted(membros.values(), key=lambda x: (ordem_bairro(x[7]), extrair_numero(x[6]), x[2])),
        start=1,
    ):
        rows.append(
            {
                "id": i,
                "membro_id": m[0],
                "membro_nome": m[2],
                "item": ITENS_ENTREGA[0],
                "data_entrega": pd.NaT,
                "entregue": "N",
                "observacoes": m[7] or "",
            }
        )
    df_full = preparar_entregas_editor(pd.DataFrame(rows))
    salvar_entregas(df_full)

if st.button("🔄 Gerar rota a partir dos membros ativos"):
    rows = []
    for i, m in enumerate(
        sorted(membros.values(), key=lambda x: (ordem_bairro(x[7]), extrair_numero(x[6]), x[2])),
        start=1,
    ):
        rows.append(
            {
                "id": i,
                "membro_id": m[0],
                "membro_nome": m[2],
                "item": ITENS_ENTREGA[0],
                "data_entrega": pd.NaT,
                "entregue": "N",
                "observacoes": m[7] or "",
            }
        )
    salvar_entregas(preparar_entregas_editor(pd.DataFrame(rows)))
    st.rerun()

bairro_f = st.selectbox(
    "Filtrar bairro",
    ["Todos"] + sorted({m[7] for m in membros.values() if m[7]}),
)
filtrado = bairro_f != "Todos"
df = preparar_entregas_editor(df_full.copy())
if filtrado:
    df = df[
        df.apply(
            lambda r: membros.get(int(r["membro_id"]), (None,) * 14)[7] == bairro_f
            if pd.notna(r.get("membro_id"))
            else False,
            axis=1,
        )
    ]
    st.warning("Filtro ativo: ao salvar, só altera linhas visíveis.")

st.caption(
    "Edite abaixo ou use **Entregas** para CRUD completo. "
    "➕/excluir linhas no editor; depois **Salvar rota**."
)

if df.empty:
    st.info("Nenhuma visita na rota. Clique em **Gerar rota** para criar a lista.")
    edited = df
else:
    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="%d"),
            "membro_id": st.column_config.NumberColumn("Membro", format="%d"),
            "item": st.column_config.SelectboxColumn("Item", options=ITENS_ENTREGA),
            "entregue": st.column_config.SelectboxColumn("Entregue?", options=ENTREGUE),
            "data_entrega": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
        },
        height=450,
        hide_index=True,
    )

if not df.empty:
    pendentes = len(edited[edited["entregue"].astype(str).str.upper() != "S"])
    st.metric("Visitas pendentes (nesta lista)", pendentes)

if st.button("💾 Salvar rota", type="primary", disabled=df.empty):
    try:
        merged = mesclar_por_id(df_full, edited, filtrado=filtrado)
        merged = preparar_dataframe(
            merged,
            COL_ENTREGAS,
            id_col="id",
            colunas_data=["data_entrega"],
        )
        salvar_entregas(merged)
        st.success("Rota salva no apostolado.xlsx.")
        st.rerun()
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
