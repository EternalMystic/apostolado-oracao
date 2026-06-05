"""Exportar e baixar o apostolado.xlsx — uma aba ou arquivo completo."""
from __future__ import annotations

from datetime import datetime
from io import BytesIO

import pandas as pd

from utils.data_manager import EXCEL_PATH


def _stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M")


def nome_arquivo_completo() -> str:
    return f"apostolado_completo_{_stamp()}.xlsx"


def nome_arquivo_aba(aba: str) -> str:
    seguro = "".join(c if c.isalnum() or c in " _-" else "_" for c in aba).strip() or "aba"
    return f"apostolado_{seguro}_{_stamp()}.xlsx"


def bytes_excel_completo() -> bytes | None:
    if not EXCEL_PATH.exists():
        return None
    return EXCEL_PATH.read_bytes()


def bytes_excel_aba(nome_aba: str, df: pd.DataFrame) -> bytes:
    """Gera um .xlsx só com esta aba (útil para abrir no Excel)."""
    buf = BytesIO()
    aba = (nome_aba or "Dados")[:31]
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=aba, index=False)
    return buf.getvalue()


def bytes_excel_com_abas_atualizadas(atualizacoes: dict[str, pd.DataFrame]) -> bytes:
    """Cópia do workbook com uma ou mais abas substituídas (sem gravar no servidor)."""
    if EXCEL_PATH.exists():
        todas = pd.read_excel(EXCEL_PATH, sheet_name=None, engine="openpyxl")
    else:
        todas = {}
    for nome, df in atualizacoes.items():
        todas[nome] = df
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        for nome, sdf in todas.items():
            sdf.to_excel(writer, sheet_name=str(nome)[:31], index=False)
    return buf.getvalue()
