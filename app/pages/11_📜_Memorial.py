"""Memorial dos membros falecidos."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.dados_membros import MEMORIAL
from utils.data_manager import ler_membros

st.set_page_config(page_title="Memorial", page_icon="📜", layout="wide")
require_login()
inject_css()
st.title("📜 Memorial – Membros Falecidos")
st.caption("Em memória dos que nos precederam no caminho da fé.")

for nome, nasc, falec, obs in MEMORIAL:
    with st.container():
        st.markdown(f"### {nome}")
        c1, c2 = st.columns(2)
        c1.write(f"**Nascimento:** {nasc.strftime('%d/%m/%Y') if nasc else '—'}")
        c2.write(
            f"**Falecimento:** {falec.strftime('%d/%m/%Y') if falec else 'data não registrada'}"
        )
        st.write(obs)
        st.divider()

falecidos = [m for m in ler_membros() if m[10] == "Falecida"]
if falecidos:
    st.subheader("Cadastro – situação Falecida")
    st.dataframe(
        pd.DataFrame(
            [{"nome": m[2], "obs": m[12]} for m in falecidos]
        ),
        use_container_width=True,
    )

st.markdown("---")
st.markdown("*Descansai em paz. Nossa oração vos acompanha. R.I.P.*")
