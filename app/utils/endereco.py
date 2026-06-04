"""Endereço completo: rua, número, bairro, CEP, cidade."""
from __future__ import annotations

import re
from typing import Any

CIDADE_PADRAO = "Nova Odessa"
UF_PADRAO = "SP"


def extrair_numero_da_rua(rua: str) -> tuple[str, str]:
    """Separa número no fim ou após vírgula (ex.: 'Rua X, 47')."""
    texto = (rua or "").strip()
    if not texto:
        return "", ""
    m = re.search(r",\s*n[º°o\.]*\s*(\S+)", texto, re.IGNORECASE)
    if m:
        return texto[: m.start()].strip(), m.group(1)
    m2 = re.search(r"\b(n[º°o\.]*\s*)?(\d+\w*)\s*$", texto, re.IGNORECASE)
    if m2:
        return texto[: m2.start()].strip().rstrip(",").strip(), m2.group(2)
    return texto, ""


def separar_endereco_legacy(endereco: str, bairro: str, cidade: str = "") -> dict[str, str]:
    rua, numero = extrair_numero_da_rua(endereco or "")
    return {
        "rua": rua,
        "numero": numero,
        "bairro": (bairro or "").strip(),
        "cep": "",
        "cidade": (cidade or "").strip() or CIDADE_PADRAO,
    }


def campos_endereco_de_registro(reg: dict[str, Any] | Any) -> dict[str, str]:
    """Lê campos de endereço de um membro (dict ou Series)."""
    if hasattr(reg, "to_dict"):
        reg = reg.to_dict()
    rua = str(reg.get("rua") or reg.get("endereco") or "").strip()
    numero = str(reg.get("numero") or "").strip()
    if not numero and rua:
        rua, numero = extrair_numero_da_rua(rua)
    return {
        "cep": str(reg.get("cep") or "").strip(),
        "rua": rua,
        "numero": numero,
        "bairro": str(reg.get("bairro") or "").strip(),
        "cidade": str(reg.get("cidade") or "").strip() or CIDADE_PADRAO,
    }


def formatar_endereco_completo(
    cep: str = "",
    rua: str = "",
    numero: str = "",
    bairro: str = "",
    cidade: str = "",
    *,
    uma_linha: bool = True,
) -> str:
    partes: list[str] = []
    if rua:
        linha = rua
        if numero:
            linha += f", {numero}" if not re.search(r"\d", rua) else f" — nº {numero}"
        partes.append(linha)
    if bairro:
        partes.append(bairro)
    if cidade:
        partes.append(cidade)
    if cep:
        c = cep.strip()
        if len(c) == 8 and c.isdigit():
            c = f"{c[:5]}-{c[5:]}"
        partes.append(f"CEP {c}")
    if not partes:
        return ""
    sep = " · " if uma_linha else "\n"
    return sep.join(partes)


def endereco_completo_de_registro(reg: dict[str, Any]) -> str:
    c = campos_endereco_de_registro(reg)
    return formatar_endereco_completo(**c)


def linha_entrega_visita_de_membro(reg: dict[str, Any]) -> dict[str, str]:
    """Campos de endereço para abas Entregas e Visitas."""
    c = campos_endereco_de_registro(reg)
    return {
        "cep": c["cep"],
        "rua": c["rua"],
        "numero": c["numero"],
        "bairro": c["bairro"],
        "cidade": c["cidade"],
    }


def texto_busca_endereco(reg: dict[str, Any]) -> str:
    c = campos_endereco_de_registro(reg)
    return " ".join(
        x
        for x in [
            c["cep"],
            c["rua"],
            c["numero"],
            c["bairro"],
            c["cidade"],
            endereco_completo_de_registro(reg),
        ]
        if x
    ).lower()


def aplicar_filtro_endereco(
    reg: dict[str, Any],
    *,
    cep: str = "",
    bairro: str = "",
    rua: str = "",
    cidade: str = "",
) -> bool:
    c = campos_endereco_de_registro(reg)
    if cep and cep.strip().replace("-", "") not in c["cep"].replace("-", ""):
        return False
    if bairro and bairro != "Todos" and bairro.lower() not in c["bairro"].lower():
        return False
    if cidade and cidade != "Todos" and cidade.lower() not in c["cidade"].lower():
        return False
    if rua and rua.strip().lower() not in c["rua"].lower():
        return False
    return True
