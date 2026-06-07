"""Geocodificação (OpenStreetMap) e ordenação da rota pelo endereço mais próximo."""
from __future__ import annotations

import json
import math
import time
import urllib.parse
from pathlib import Path
from typing import Any, Callable

import httpx

from utils.endereco import endereco_completo_de_registro, formatar_endereco_completo, mesclar_endereco_de_registro

ENDERECO_PAROQUIA_PADRAO = (
    "Rua Salvador, 399, São Jorge, Nova Odessa, São Paulo, Brasil"
)
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "ApostoladoOracaoNovaOdessa/1.0 (uso paroquial; contato paroquia)"
_CACHE_PATH: Path | None = None


def _cache_file() -> Path:
    global _CACHE_PATH
    if _CACHE_PATH is None:
        root = Path(__file__).resolve().parent.parent.parent
        _CACHE_PATH = root / "data" / "geocache.json"
        _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return _CACHE_PATH


def _carregar_cache() -> dict[str, dict[str, Any]]:
    p = _cache_file()
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _salvar_cache(cache: dict[str, dict[str, Any]]) -> None:
    _cache_file().write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def _chave_endereco(texto: str) -> str:
    return " ".join(texto.lower().split())


def montar_query(reg: dict[str, Any]) -> str:
    completo = endereco_completo_de_registro(reg)
    if completo:
        return f"{completo}, Brasil"
    return ""


def geocodificar_texto(
    endereco: str, *, cache: dict[str, dict[str, Any]] | None = None
) -> tuple[float, float] | None:
    """Geocodifica um endereço em texto livre (ex.: paróquia)."""
    texto = (endereco or "").strip()
    if not texto:
        return None
    query = texto if "brasil" in texto.lower() else f"{texto}, Brasil"
    chave = _chave_endereco(query)
    cache = cache if cache is not None else _carregar_cache()
    if chave in cache and cache[chave].get("lat") is not None:
        return float(cache[chave]["lat"]), float(cache[chave]["lon"])
    if chave in cache and cache[chave].get("lat") is None:
        return None

    try:
        r = httpx.get(
            NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": 1, "countrycodes": "br"},
            headers={"User-Agent": USER_AGENT},
            timeout=15.0,
        )
        r.raise_for_status()
        dados = r.json()
        if not dados:
            cache[chave] = {"lat": None, "lon": None, "query": query}
            _salvar_cache(cache)
            return None
        lat = float(dados[0]["lat"])
        lon = float(dados[0]["lon"])
        cache[chave] = {"lat": lat, "lon": lon, "query": query, "display": dados[0].get("display_name", "")}
        _salvar_cache(cache)
        time.sleep(1.05)
        return lat, lon
    except Exception:
        return None


def geocodificar(
    reg: dict[str, Any],
    *,
    cache: dict[str, dict[str, Any]] | None = None,
    permitir_rede: bool = True,
) -> tuple[float, float] | None:
    """Latitude/longitude via Nominatim (gratuito, como base do OpenStreetMap)."""
    query = montar_query(reg)
    if not query.strip():
        return None
    chave = _chave_endereco(query)
    cache = cache if cache is not None else _carregar_cache()
    if chave in cache and cache[chave].get("lat") is not None:
        return float(cache[chave]["lat"]), float(cache[chave]["lon"])
    if chave in cache and cache[chave].get("lat") is None:
        return None
    if not permitir_rede:
        return None

    try:
        r = httpx.get(
            NOMINATIM_URL,
            params={"q": query, "format": "json", "limit": 1, "countrycodes": "br"},
            headers={"User-Agent": USER_AGENT},
            timeout=15.0,
        )
        r.raise_for_status()
        dados = r.json()
        if not dados:
            cache[chave] = {"lat": None, "lon": None, "query": query}
            _salvar_cache(cache)
            return None
        lat = float(dados[0]["lat"])
        lon = float(dados[0]["lon"])
        cache[chave] = {"lat": lat, "lon": lon, "query": query, "display": dados[0].get("display_name", "")}
        _salvar_cache(cache)
        time.sleep(1.05)
        return lat, lon
    except Exception:
        return None


def distancia_km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(h))


def ordenar_por_proximidade(
    linhas: list[dict[str, Any]],
    *,
    ponto_partida: str | None = None,
    apenas_pendentes: bool = True,
    ao_avancar: Callable[[int, int, str], None] | None = None,
) -> tuple[list[dict[str, Any]], list[str]]:
    """
    Ordena visitas do mais perto ao mais longe (vizinho mais próximo).
    Retorna (linhas ordenadas, avisos).
    """
    avisos: list[str] = []
    cache = _carregar_cache()
    partida_txt = (ponto_partida or ENDERECO_PAROQUIA_PADRAO).strip()

    candidatas = [
        r
        for r in linhas
        if not (apenas_pendentes and str(r.get("entregue", "N")).upper() == "S")
    ]
    total = len(candidatas) + 1

    if ao_avancar:
        ao_avancar(0, total, "Paróquia")
    origem = geocodificar_texto(partida_txt, cache=cache)
    if not origem:
        avisos.append("Não foi possível localizar o ponto de partida (paróquia). Usando primeira visita.")
        origem = None

    sem_mapa: list[dict[str, Any]] = []
    trabalho: list[tuple[dict[str, Any], tuple[float, float]]] = []
    for i, row in enumerate(candidatas, start=1):
        if ao_avancar:
            ao_avancar(i, total, str(row.get("membro_nome", "membro")))
        coords = geocodificar(row, cache=cache)
        if coords:
            trabalho.append((row, coords))
        else:
            sem_mapa.append(row)
            avisos.append(f"Sem mapa: {row.get('membro_nome', 'membro')}")

    if not trabalho:
        return linhas, avisos or ["Nenhuma visita pendente para ordenar."]

    if origem is None:
        origem = trabalho[0][1]

    ordenados: list[dict[str, Any]] = []
    restante = trabalho.copy()
    atual = origem

    while restante:
        restante.sort(key=lambda x: distancia_km(atual, x[1]))
        prox_row, prox_coord = restante.pop(0)
        ordenados.append(prox_row)
        atual = prox_coord

    ordenados.extend(sem_mapa)

    if not apenas_pendentes:
        return ordenados, avisos

    entregues = [r for r in linhas if str(r.get("entregue", "")).upper() == "S"]
    return entregues + ordenados, avisos


def url_google_maps(ponto: dict[str, Any]) -> str:
    q = montar_query(ponto) or endereco_completo_de_registro(ponto)
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote(q)


def url_apple_maps(ponto: dict[str, Any]) -> str:
    q = montar_query(ponto) or endereco_completo_de_registro(ponto)
    return "http://maps.apple.com/?q=" + urllib.parse.quote(q)


def url_waze(ponto: dict[str, Any]) -> str:
    q = montar_query(ponto) or endereco_completo_de_registro(ponto)
    return "https://waze.com/ul?q=" + urllib.parse.quote(q) + "&navigate=yes"


def url_rota_google(paradas: list[dict[str, Any]], *, max_paradas: int = 9) -> str:
    """Rota com várias paradas no Google Maps (limite de waypoints na URL)."""
    enderecos: list[str] = []
    for p in paradas[: max_paradas + 2]:
        q = montar_query(p) or endereco_completo_de_registro(p)
        if q:
            enderecos.append(q)
    if len(enderecos) < 2:
        if paradas:
            return url_google_maps(paradas[0])
        return "https://www.google.com/maps"
    origem = urllib.parse.quote(enderecos[0])
    destino = urllib.parse.quote(enderecos[-1])
    url = f"https://www.google.com/maps/dir/?api=1&origin={origem}&destination={destino}&travelmode=driving"
    meio = enderecos[1:-1]
    if meio:
        wp = "|".join(urllib.parse.quote(e) for e in meio)
        url += "&waypoints=" + wp
    return url


def resumo_distancias(
    linhas: list[dict[str, Any]],
    *,
    permitir_rede: bool = False,
    membros: dict[int, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Para exibir km entre paradas consecutivas (só cache, salvo se permitir_rede)."""
    cache = _carregar_cache()
    out = []
    prev: tuple[float, float] | None = None
    for i, row in enumerate(linhas, start=1):
        fallback = None
        if membros:
            mid = int(row.get("membro_id") or 0)
            fallback = membros.get(mid)
        endereco = endereco_completo_de_registro(row, fallback, uma_linha=False)
        row_mapa = {**row, **mesclar_endereco_de_registro(row, fallback)} if fallback else row
        c = geocodificar(row_mapa, cache=cache, permitir_rede=permitir_rede)
        km = None
        if c and prev:
            km = round(distancia_km(prev, c), 1)
        if c:
            prev = c
        out.append(
            {
                "ordem": i,
                "nome": row.get("membro_nome", ""),
                "endereco": endereco,
                "km_anterior": km,
                "row": row_mapa,
            }
        )
    return out
