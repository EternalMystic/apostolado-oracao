"""Configurações do sistema."""
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.auth import require_login
from utils.ui import inject_css
from utils.data_manager import BACKUPS_DIR, EXCEL_PATH, ler_config, salvar_config
from utils.dados_membros import CONFIG_PADRAO
from utils.inicializar_excel import criar_workbook_inicial

st.set_page_config(page_title="Configurações", page_icon="⚙️", layout="wide")
require_login()
inject_css()
st.title("⚙️ Configurações")

cfg = {**CONFIG_PADRAO, **ler_config()}

with st.form("config"):
    paroquia = st.text_input("Paróquia", cfg.get("paroquia", ""))
    diocese = st.text_input("Diocese", cfg.get("diocese", ""))
    cidade = st.text_input("Cidade", cfg.get("cidade", ""))
    coordenador = st.text_input("Coordenador", cfg.get("coordenador", ""))
    coordenadora = st.text_input("Coordenadora", cfg.get("coordenadora", ""))
    whatsapp = st.text_input("WhatsApp coordenador", cfg.get("whatsapp_coordenador", ""))
    tema = st.color_picker("Cor tema", cfg.get("tema_cor", "#6A1B9A"))
    backup = st.selectbox("Backup automático", ["Sim", "Não"], index=0)
    if st.form_submit_button("Salvar configurações"):
        novo = {
            **cfg,
            "paroquia": paroquia,
            "diocese": diocese,
            "cidade": cidade,
            "coordenador": coordenador,
            "coordenadora": coordenadora,
            "whatsapp_coordenador": whatsapp,
            "tema_cor": tema,
            "backup_automatico": backup,
        }
        salvar_config(novo)
        st.success("Configurações salvas.")

st.divider()
st.warning("Recriar Excel apaga alterações não salvas em backup.")
if st.button("🔄 Recriar apostolado.xlsx do seed"):
    criar_workbook_inicial()
    st.success(f"Recriado: {EXCEL_PATH}")

st.caption(f"Arquivo de dados: {EXCEL_PATH}")

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
