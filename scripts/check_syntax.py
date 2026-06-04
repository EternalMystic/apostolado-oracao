"""Verifica sintaxe de todos os arquivos Python do app."""
from __future__ import annotations

import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    erros: list[str] = []
    for path in sorted(ROOT.rglob("*.py")):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as e:
            erros.append(f"{path.relative_to(ROOT)}: {e.msg}")
    if erros:
        print("Erros de sintaxe encontrados:")
        for msg in erros:
            print(f"  - {msg}")
        return 1
    print("OK — sintaxe valida em todos os arquivos .py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
