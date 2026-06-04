"""Referência rápida."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Instruções", page_icon="📝", layout="wide")
require_login()
inject_css()
st.title("📝 Referência")

st.markdown(
    """
| Ação | Onde |
|------|------|
| Buscar membro | **Consulta Rápida** ou **Membros** |
| Visita / entrega | **Rota de Visitas** — marque **S** quando entregar |
| Aniversário | **Aniversários** |
| Corrigir cadastro | **Inconsistências** — marque **Sim** quando resolver |
| Exportar dados | **Relatórios** |

**Dados:** `data/apostolado.xlsx` · **Backup:** pasta `backups/`

Coordenador(a) do Apostolado para senha e dúvidas.
"""
)
