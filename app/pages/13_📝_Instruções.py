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
| Tabela | Onde editar (CRUD) |
|--------|-------------------|
| Membros | **Membros** — ➕ Nova linha · editar · excluir linha · **Salvar** |
| Entregas / rota | **Entregas** ou **Rota de Visitas** |
| Visitas | **Visitas** |
| Consagrações | **Consagrações** |
| Intenções | **Intenções** |
| Agenda | **Agenda** |
| Inconsistências | **Inconsistências** |
| Memorial | **Memorial** |
| Configuração | **Configurações** |
| Exportar | **Relatórios** |

**Dados:** `data/apostolado.xlsx` · **Backup:** pasta `backups/`

Coordenador(a) do Apostolado para senha e dúvidas.
"""
)
