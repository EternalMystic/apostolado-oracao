"""Comunidade pastoral inferida do livro físico (por id de membro)."""
from __future__ import annotations

COMUNIDADE_POR_ID: dict[int, str] = {
    4: "Santa Luzia",
    6: "Santa Luzia",
    9: "Santa Luzia",
    10: "Santa Luzia",
    11: "Santa Luzia",
    14: "Paróquia São Jorge",
    16: "Santa Luzia",
    37: "Santa Luzia",
    40: "Santa Luzia",
    48: "Paróquia São Jorge",
    49: "Santa Luzia",
    50: "Santa Luzia",
    53: "Santa Dulce dos Pobres",
    54: "Santa Dulce dos Pobres",
    55: "Santa Luzia",
    56: "Santa Luzia",
}


def inferir_comunidade(
    membro_id: int, bairro: str, funcao: str, observacoes: str
) -> str:
    if membro_id in COMUNIDADE_POR_ID:
        return COMUNIDADE_POR_ID[membro_id]
    texto = f"{bairro} {funcao} {observacoes}".lower()
    if "santa dulce" in texto or "dulce dos pobres" in texto:
        return "Santa Dulce dos Pobres"
    if "sta. luzia" in texto or "sta luzia" in texto or "santa luzia" in texto:
        return "Santa Luzia"
    if "fátima" in texto or "fatima" in texto:
        return "N. Sra. de Fátima"
    if "são jorge" in texto or "paróquia são jorge" in texto:
        return "Paróquia São Jorge"
    return ""
