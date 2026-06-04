"""Calendário de aniversários."""
import sys
from datetime import date
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.data_manager import aniversariantes_proximos, ler_membros

st.set_page_config(page_title="Aniversários", page_icon="🎂", layout="wide")
require_login()
inject_css()
st.title("🎂 Aniversários")
st.caption("Uma ligação no dia do aniversário é apostolado de proximidade.")

dias = st.slider("Próximos dias", 7, 90, 30)
lista = aniversariantes_proximos(dias)

hoje = date.today()
mes_atual = [a for a in lista if a["nasc"] and a["nasc"].month == hoje.month]
st.metric(f"Aniversariantes em {hoje.strftime('%B')}", len(mes_atual))
st.metric(f"Próximos {dias} dias", len(lista))

if lista:
    for a in lista:
        cor = "🟢" if a["dias"] <= 7 else "🟡" if a["dias"] <= 14 else "⚪"
        st.write(
            f"{cor} **{a['nome']}** – {a['proximo'].strftime('%d/%m')} "
            f"({a['dias']} dias) · {a['idade'] or '?'} anos · "
            f"{a['telefone'] or 'sem telefone'} · {a['situacao']}"
        )
else:
    st.info("Nenhum aniversário no período.")

st.divider()
st.subheader("Todos com data de nascimento (exceto falecidos)")
for m in sorted(ler_membros(), key=lambda x: ((x[4].month, x[4].day) if x[4] else (13, 32))):
    if m[4] and m[10] != "Falecida":
        st.write(f"{m[4].strftime('%d/%m')} – **{m[2]}** ({m[10]})")
