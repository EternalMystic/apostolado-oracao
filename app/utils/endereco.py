"""Endereço completo: rua, número, bairro, CEP, cidade."""
from __future__ import annotations

import re
from typing import Any

CIDADE_PADRAO = "Nova Odessa"
UF_PADRAO = "SP"


def _campo_limpo(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, float):
        import math

        if math.isnan(val):
            return ""
    s = str(val).strip()
    if s.lower() in ("nan", "none", "nat", ""):
        return ""
    if re.match(r"^\d+\.0$", s):
        s = str(int(float(s)))
    return s


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
    rua = _campo_limpo(reg.get("rua") or reg.get("endereco"))
    numero = _campo_limpo(reg.get("numero"))
    if not numero and rua:
        rua, numero = extrair_numero_da_rua(rua)
    cidade = _campo_limpo(reg.get("cidade")) or CIDADE_PADRAO
    return {
        "cep": _campo_limpo(reg.get("cep")),
        "rua": rua,
        "numero": numero,
        "bairro": _campo_limpo(reg.get("bairro")),
        "cidade": cidade,
    }


def endereco_tem_logradouro(campos: dict[str, str]) -> bool:
    return bool(campos.get("rua") or campos.get("bairro") or campos.get("cep"))


def mesclar_endereco_de_registro(
    principal: dict[str, Any],
    fallback: dict[str, Any] | None = None,
) -> dict[str, str]:
    """Usa cadastro do membro quando a linha de entrega/visita está só com a cidade."""
    cp = campos_endereco_de_registro(principal)
    if not fallback:
        return cp
    cf = campos_endereco_de_registro(fallback)
    if not endereco_tem_logradouro(cp) and endereco_tem_logradouro(cf):
        return cf
    out: dict[str, str] = {}
    for k in ("cep", "rua", "numero", "bairro", "cidade"):
        out[k] = cp[k] if cp[k] else cf[k]
    if not out["cidade"]:
        out["cidade"] = CIDADE_PADRAO
    return out


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
    if len(partes) == 1 and partes[0] == CIDADE_PADRAO:
        return ""
    sep = " · " if uma_linha else "\n"
    return sep.join(partes)


def endereco_completo_de_registro(
    reg: dict[str, Any],
    fallback: dict[str, Any] | None = None,
    *,
    uma_linha: bool = True,
) -> str:
    c = mesclar_endereco_de_registro(reg, fallback) if fallback else campos_endereco_de_registro(reg)
    return formatar_endereco_completo(**c, uma_linha=uma_linha)


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
