"""Backup diário do Excel – pode ser agendado no Agendador de Tarefas do Windows."""
from __future__ import annotations

import shutil
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "apostolado.xlsx"
BACKUPS = ROOT / "backups"
DIAS_MANTER = 30


def backup_agora() -> Path | None:
    if not DATA.exists():
        print("Arquivo não encontrado:", DATA)
        return None
    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d")
    dest = BACKUPS / f"apostolado_diario_{stamp}.xlsx"
    shutil.copy2(DATA, dest)
    print("Backup:", dest)
    limpar_antigos()
    return dest


def limpar_antigos(dias: int = DIAS_MANTER) -> None:
    limite = datetime.now() - timedelta(days=dias)
    for f in BACKUPS.glob("apostolado_*.xlsx"):
        if datetime.fromtimestamp(f.stat().st_mtime) < limite:
            f.unlink()
            print("Removido:", f.name)


if __name__ == "__main__":
    backup_agora()
