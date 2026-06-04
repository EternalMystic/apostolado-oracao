"""Rota de visitas domiciliares por bairro."""
import re
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import ler_entregas, ler_membros, salvar_entregas
from utils.dados_membros import ITENS_ENTREGA, ORDEM_BAIRROS

st.set_page_config(page_title="Rota de Visitas", page_icon="🗺️", layout="wide")
require_login()
inject_css()
st.title("🗺️ Rota de Visitas Domiciliares")
st.caption("Ore um Pai-Nosso antes de cada visita. (São Josemaría Escrivá)")


def ordem_bairro(b: str) -> int:
    b = b or ""
    for i, nome in enumerate(ORDEM_BAIRROS):
        if nome and (b.lower() == nome.lower() or nome.lower() in b.lower()):
            return i
    return len(ORDEM_BAIRROS)


def extrair_numero(end: str) -> int:
    m = re.search(r"\b(\d+)\b", end or "")
    return int(m.group(1)) if m else 99999


membros = {
    m[0]: m
    for m in ler_membros()
    if m[10] in ("Ativo", "Ativo (presumido)")
}
df = ler_entregas()

if df.empty and membros:
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
                "data_entrega": "",
                "entregue": "N",
                "observacoes": m[7] or "",
            }
        )
    df = pd.DataFrame(rows)

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
                "data_entrega": "",
                "entregue": "N",
                "observacoes": m[7] or "",
            }
        )
    df = pd.DataFrame(rows)
    salvar_entregas(df)
    st.rerun()

bairro_f = st.selectbox(
    "Filtrar bairro",
    ["Todos"] + sorted({m[7] for m in membros.values() if m[7]}),
)
if bairro_f != "Todos":
    df = df[df["observacoes"].astype(str).str.contains(bairro_f, na=False) | df.apply(
        lambda r: membros.get(int(r["membro_id"]), (None,) * 14)[7] == bairro_f
        if pd.notna(r.get("membro_id"))
        else False,
        axis=1,
    )]

edited = st.data_editor(
    df,
    use_container_width=True,
    column_config={
        "item": st.column_config.SelectboxColumn("Item", options=ITENS_ENTREGA),
        "entregue": st.column_config.SelectboxColumn("Entregue?", options=["S", "N"]),
    },
)

pendentes = len(edited[edited["entregue"].astype(str).str.upper() != "S"])
st.metric("Visitas pendentes", pendentes)

if st.button("💾 Salvar rota"):
    salvar_entregas(edited)
    st.success("Rota salva.")

if st.button("🦀 Otimizar ordem (Rust TSP)"):
    st.info(
        "Execute `COMPILAR_RUST.bat` e depois rode o otimizador com as coordenadas. "
        "A ordenação por bairro já está aplicada."
    )
