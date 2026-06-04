"""Relatórios pastorais e exportação."""
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import (
    ROOT,
    aniversariantes_proximos,
    ler_entregas,
    ler_membros,
    membros_sem_telefone,
    total_por_situacao,
)

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")
require_login()
st.title("📊 Relatórios Pastorais")

totais = total_por_situacao()
st.subheader("Por situação")
st.bar_chart(totais)

st.subheader("Completude do cadastro")
c1, c2, c3 = st.columns(3)
sem_tel = membros_sem_telefone()
sem_end = [m for m in ler_membros() if not str(m[6]).strip()]
c1.metric("Sem telefone", len(sem_tel))
c2.metric("Sem endereço", len(sem_end))
c3.metric("Aniv. 30 dias", len(aniversariantes_proximos(30)))

ent = ler_entregas()
if not ent.empty:
    entregues = len(ent[ent["entregue"].astype(str).str.upper() == "S"])
    st.metric("Entregas concluídas", f"{entregues} / {len(ent)}")

exports = ROOT / "exports"
exports.mkdir(exist_ok=True)

if st.button("📥 Exportar resumo CSV"):
    rows = []
    for sit, q in totais.items():
        rows.append({"situacao": sit, "quantidade": q})
    path = exports / f"resumo_{datetime.now():%Y%m%d_%H%M%S}.csv"
    pd.DataFrame(rows).to_csv(path, index=False, encoding="utf-8-sig")
    st.success(f"Exportado: {path}")

st.info(
    "Relatório PDF mensal: execute `r_scripts/relatorio_mensal.R` "
    "(requer R + ggplot2)."
)
