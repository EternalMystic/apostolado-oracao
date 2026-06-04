"""Rota de visitas — endereço completo e filtros por CEP, bairro, rua e cidade."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colunas_ui import montar_column_config
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
from utils.endereco import aplicar_filtro_endereco, linha_entrega_visita_de_membro
from utils.opcoes import ENTREGUE

st.set_page_config(
    page_title="Rota de Visitas",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="auto",
)
require_login()
inject_css()
st.title("🗺️ Rota de Visitas")


def ordem_bairro(b: str) -> int:
    b = b or ""
    for i, nome in enumerate(ORDEM_BAIRROS):
        if nome and (b.lower() == nome.lower() or nome.lower() in b.lower()):
            return i
    return len(ORDEM_BAIRROS)


def _chave_ordenacao(m: dict) -> tuple:
    return (
        ordem_bairro(str(m.get("bairro", ""))),
        str(m.get("cep", "")),
        str(m.get("rua", "")),
        str(m.get("numero", "")),
        str(m.get("nome", "")),
    )


def _linha_rota(m: dict, eid: int) -> dict:
    end = linha_entrega_visita_de_membro(m)
    return {
        "id": eid,
        "membro_id": m["id"],
        "membro_nome": m["nome"],
        **end,
        "item": ITENS_ENTREGA[0],
        "data_entrega": pd.NaT,
        "entregue": "N",
        "observacoes": "",
    }


membros_ativos = [
    m
    for m in ler_membros()
    if m.get("situacao") in ("Ativo", "Ativo (presumido)")
]
membros = {m["id"]: m for m in membros_ativos}
df_full = ler_entregas()

if df_full.empty and membros:
    rows = [_linha_rota(m, i) for i, m in enumerate(sorted(membros.values(), key=_chave_ordenacao), 1)]
    df_full = preparar_entregas_editor(pd.DataFrame(rows))
    salvar_entregas(df_full)

if st.button("🔄 Gerar rota a partir dos membros ativos"):
    rows = [_linha_rota(m, i) for i, m in enumerate(sorted(membros.values(), key=_chave_ordenacao), 1)]
    salvar_entregas(preparar_entregas_editor(pd.DataFrame(rows)))
    st.rerun()

st.subheader("Filtrar endereço")
f1, f2, f3, f4 = st.columns(4)
with f1:
    filtro_cep = st.text_input("CEP", key="rota_f_cep", placeholder="Ex.: 13380")
with f2:
    bairros = sorted({str(m.get("bairro", "")).strip() for m in membros_ativos if m.get("bairro")})
    filtro_bairro = st.selectbox("Bairro", ["Todos"] + bairros, key="rota_f_bairro")
with f3:
    filtro_rua = st.text_input("Rua", key="rota_f_rua", placeholder="Parte do nome da rua")
with f4:
    cidades = sorted({str(m.get("cidade", "")).strip() for m in membros_ativos if m.get("cidade")})
    filtro_cidade = st.selectbox("Cidade", ["Todos"] + cidades, key="rota_f_cidade")

filtrado = any(
    [
        filtro_cep.strip(),
        filtro_bairro != "Todos",
        filtro_rua.strip(),
        filtro_cidade != "Todos",
    ]
)

df = preparar_entregas_editor(df_full.copy())
if filtrado:

    def _linha_passa(r: pd.Series) -> bool:
        mid = int(r["membro_id"]) if pd.notna(r.get("membro_id")) else 0
        m = membros.get(mid)
        if not m:
            reg = {
                "cep": r.get("cep", ""),
                "rua": r.get("rua", ""),
                "numero": r.get("numero", ""),
                "bairro": r.get("bairro", ""),
                "cidade": r.get("cidade", ""),
            }
        else:
            reg = m
        return aplicar_filtro_endereco(
            reg,
            cep=filtro_cep,
            bairro=filtro_bairro,
            rua=filtro_rua,
            cidade=filtro_cidade,
        )

    df = df[df.apply(_linha_passa, axis=1)]
    st.warning("Filtro ativo: ao salvar, só altera linhas visíveis.")

st.caption(
    "Colunas de endereço: CEP, rua, número, bairro e cidade. "
    "Campo **Observações** é só para notas da visita (não use para endereço)."
)

if df.empty:
    st.info("Nenhuma visita na rota. Clique em **Gerar rota** para criar a lista.")
    edited = df
else:
    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config=montar_column_config(
            list(df.columns),
            {
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "membro_id": st.column_config.NumberColumn("ID membro", format="%d"),
                "item": st.column_config.SelectboxColumn("Material / motivo", options=ITENS_ENTREGA),
                "entregue": st.column_config.SelectboxColumn("Entregue?", options=ENTREGUE),
                "data_entrega": st.column_config.DateColumn("Data da entrega", format="DD/MM/YYYY"),
            },
        ),
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
