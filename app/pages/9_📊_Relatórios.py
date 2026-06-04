"""Relatórios pastorais e exportação completa."""
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import (
    EXCEL_PATH,
    ROOT,
    aniversariantes_proximos,
    contar_zeladores_ativos,
    ler_centros,
    ler_diretoria,
    ler_entregas,
    ler_intencoes_papa,
    ler_membros,
    ler_membros_df,
    membros_sem_endereco,
    membros_sem_telefone,
    total_por_situacao,
)
from utils.endereco import endereco_completo_de_registro

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("📊 Relatórios")

totais = total_por_situacao()
st.subheader("Por situação")
st.bar_chart(totais)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sem telefone", len(membros_sem_telefone()))
c2.metric("Aniv. 30 dias", len(aniversariantes_proximos(30)))
c3.metric("Zeladores ativos", contar_zeladores_ativos())
c4.metric("Centros", len(ler_centros()))

ent = ler_entregas()
if not ent.empty:
    entregues = len(ent[ent["entregue"].astype(str).str.upper() == "S"])
    st.metric("Entregas concluídas", f"{entregues} / {len(ent)}")

st.divider()
st.subheader("Exportar")

exports = ROOT / "exports"
exports.mkdir(exist_ok=True)

if st.button("📥 Resumo CSV"):
    rows = [{"situacao": s, "quantidade": q} for s, q in totais.items()]
    path = exports / f"resumo_{datetime.now():%Y%m%d_%H%M%S}.csv"
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    st.success(f"Salvo: {path}")

if st.button("📥 Lista de membros CSV"):
    path = exports / f"membros_{datetime.now():%Y%m%d_%H%M%S}.csv"
    ler_membros_df().to_csv(path, index=False, encoding="utf-8-sig")
    st.success(f"Salvo: {path}")

if EXCEL_PATH.exists():
    st.download_button(
        "⬇️ Baixar Excel completo",
        data=EXCEL_PATH.read_bytes(),
        file_name=f"apostolado_{datetime.now():%Y%m%d}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

st.subheader("Imprimir / consultar")
if st.checkbox("Mostrar diretoria"):
    st.dataframe(ler_diretoria(), use_container_width=True, hide_index=True)
if st.checkbox("Mostrar intenções do Papa"):
    st.dataframe(ler_intencoes_papa(), use_container_width=True, hide_index=True)

sem_end = membros_sem_endereco()
if sem_end:
    with st.expander(f"Membros sem rua cadastrada ({len(sem_end)})"):
        for m in sem_end:
            st.write(f"• {m.get('nome')} — {m.get('situacao')}")
