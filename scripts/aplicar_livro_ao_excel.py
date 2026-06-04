"""Regenera data/apostolado.xlsx a partir do livro (dados_membros.py)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))
sys.path.insert(0, str(ROOT / "app" / "utils"))

from inicializar_excel import criar_workbook_inicial  # noqa: E402

if __name__ == "__main__":
    path = criar_workbook_inicial()
    print(f"Excel atualizado com o livro: {path}")
