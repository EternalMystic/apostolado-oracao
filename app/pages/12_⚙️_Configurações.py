"""Configurações do sistema — CRUD da tabela Config."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import require_login
from utils.ui import inject_css
from utils.crud_ui import tabela_crud
from utils.data_manager import (
    BACKUPS_DIR,
    COL_CONFIG,
    EXCEL_PATH,
    ler_config_df,
    salvar_config_df,
)
from utils.inicializar_excel import criar_workbook_inicial

st.set_page_config(page_title="Configurações", page_icon="⚙️", layout="wide", initial_sidebar_state="auto")
require_login()
inject_css()
st.title("⚙️ Configurações")

st.subheader("Parâmetros (chave / valor)")
tabela_crud(
    chave="config",
    colunas=COL_CONFIG,
    carregar=ler_config_df,
    salvar=salvar_config_df,
    id_col=None,
    altura=350,
)

st.divider()
st.warning("Recriar Excel apaga alterações não salvas em backup.")
if st.button("🔄 Recriar apostolado.xlsx do seed"):
    criar_workbook_inicial()
    st.success(f"Recriado: {EXCEL_PATH}")

st.caption(f"Arquivo de dados: {EXCEL_PATH}")

st.divider()
with st.expander("🤖 Inteligência artificial (reunião semanal)"):
    st.markdown(
        """
Configure no **Streamlit Cloud → Settings → Secrets**:

```toml
OPENAI_API_KEY = "sk-..."
ANTHROPIC_API_KEY = "sk-ant-..."  # opcional
AI_PREFERENCIA = "openai"
```

Use a página **Reunião IA** para enviar o áudio (~1h10) ou colar a transcrição.
Não grave a chave na tabela Config abaixo (risco de vazamento).
"""
    )

st.divider()
st.subheader("☁️ Backup na nuvem (importante)")
st.caption(
    "No acesso pela internet, baixe uma cópia do Excel periodicamente "
    "e guarde no computador da paróquia."
)
if EXCEL_PATH.exists():
    st.download_button(
        "⬇️ Baixar apostolado.xlsx agora",
        data=EXCEL_PATH.read_bytes(),
        file_name="apostolado_backup.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
    )
upload = st.file_uploader("⬆️ Restaurar de um backup (.xlsx)", type=["xlsx"])
if upload is not None:
    if st.button("Aplicar arquivo enviado"):
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        if EXCEL_PATH.exists():
            import shutil
            from datetime import datetime

            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            shutil.copy2(EXCEL_PATH, BACKUPS_DIR / f"pre_upload_{stamp}.xlsx")
        EXCEL_PATH.write_bytes(upload.getvalue())
        st.success("Dados restaurados. Atualize a página (F5).")
        st.rerun()
