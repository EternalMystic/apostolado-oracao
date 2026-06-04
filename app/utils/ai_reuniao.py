"""Transcrição (Whisper) e resumo (GPT / Claude) de reuniões do Apostolado."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Limite da API Whisper (OpenAI)
MAX_AUDIO_BYTES = 24 * 1024 * 1024
EXCEL_TEXT_MAX = 32000

PROMPT_RESUMO = """Você é secretário(a) do Apostolado da Oração de uma paróquia católica no Brasil.
Analise a transcrição de uma reunião semanal (~1h10) e responda em português brasileiro, em JSON válido, com as chaves:
- "resumo": parágrafo objetivo (8-12 linhas) do que foi tratado
- "explicacao": texto claro para quem não participou — contexto, decisões, encaminhamentos
- "pontos_chave": lista em texto, um item por linha, com tópicos principais e tarefas (quem/o quê, se mencionado)

Seja fiel ao áudio; não invente nomes ou decisões. Tom respeitoso e pastoral."""


def _root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def audios_dir() -> Path:
    p = _root() / "data" / "audios"
    p.mkdir(parents=True, exist_ok=True)
    return p


def transcricoes_dir() -> Path:
    p = _root() / "data" / "transcricoes"
    p.mkdir(parents=True, exist_ok=True)
    return p


def truncar_excel(texto: str, limite: int = EXCEL_TEXT_MAX) -> str:
    t = (texto or "").strip()
    if len(t) <= limite:
        return t
    return t[: limite - 20] + "\n… [texto completo no arquivo .txt]"


def ler_transcricao(caminho: str | Path | None) -> str:
    if not caminho:
        return ""
    p = Path(caminho)
    if not p.is_absolute():
        p = _root() / p
    if p.exists():
        return p.read_text(encoding="utf-8")
    return ""


def salvar_transcricao(registro_id: int, texto: str) -> str:
    p = transcricoes_dir() / f"reuniao_{registro_id}.txt"
    p.write_text(texto, encoding="utf-8")
    return str(p.relative_to(_root())).replace("\\", "/")


def salvar_audio(registro_id: int, nome: str, dados: bytes) -> str:
    ext = Path(nome).suffix.lower() or ".mp3"
    if ext not in (".mp3", ".m4a", ".wav", ".webm", ".ogg", ".mpeg", ".mpga"):
        ext = ".mp3"
    p = audios_dir() / f"reuniao_{registro_id}{ext}"
    p.write_bytes(dados)
    return str(p.relative_to(_root())).replace("\\", "/")


def obter_config_ia(cfg: dict[str, str]) -> dict[str, str]:
    """Chaves de API: Streamlit secrets (preferido) ou tabela Config."""
    out = {
        "openai": "",
        "anthropic": "",
        "modelo_openai": cfg.get("ai_modelo_openai", "gpt-4o-mini"),
        "modelo_anthropic": cfg.get("ai_modelo_anthropic", "claude-3-5-haiku-20241022"),
        "preferencia": cfg.get("ai_preferencia", "openai"),
    }
    try:
        import streamlit as st

        if hasattr(st, "secrets"):
            out["openai"] = (st.secrets.get("OPENAI_API_KEY") or "").strip()
            out["anthropic"] = (st.secrets.get("ANTHROPIC_API_KEY") or "").strip()
            if st.secrets.get("AI_MODELO_OPENAI"):
                out["modelo_openai"] = str(st.secrets["AI_MODELO_OPENAI"]).strip()
            if st.secrets.get("AI_MODELO_ANTHROPIC"):
                out["modelo_anthropic"] = str(st.secrets["AI_MODELO_ANTHROPIC"]).strip()
            if st.secrets.get("AI_PREFERENCIA"):
                out["preferencia"] = str(st.secrets["AI_PREFERENCIA"]).strip().lower()
    except Exception:
        pass
    if not out["openai"]:
        out["openai"] = (cfg.get("openai_api_key") or "").strip()
    if not out["anthropic"]:
        out["anthropic"] = (cfg.get("anthropic_api_key") or "").strip()
    return out


def ia_disponivel(cfg: dict[str, str]) -> tuple[bool, str]:
    c = obter_config_ia(cfg)
    if c["openai"]:
        return True, "OpenAI (Whisper + resumo)"
    if c["anthropic"]:
        return True, "Anthropic (só resumo — envie texto ou transcreva com OpenAI)"
    return False, "Nenhuma chave configurada"


def transcrever_audio(caminho: Path, api_key: str) -> str:
    tamanho = caminho.stat().st_size
    if tamanho > MAX_AUDIO_BYTES:
        mb = tamanho / (1024 * 1024)
        raise ValueError(
            f"Arquivo com {mb:.1f} MB (limite Whisper: 25 MB). "
            "Exporte o áudio em MP3 mono 32–48 kbps ou use a aba «Colar transcrição»."
        )
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    with caminho.open("rb") as f:
        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="pt",
            response_format="text",
        )
    if isinstance(resp, str):
        return resp.strip()
    return str(resp).strip()


def _parse_json_resumo(raw: str) -> dict[str, str]:
    texto = raw.strip()
    if texto.startswith("```"):
        linhas = texto.split("\n")
        texto = "\n".join(linhas[1:-1] if linhas[-1].strip() == "```" else linhas[1:])
    try:
        data = json.loads(texto)
    except json.JSONDecodeError:
        return {
            "resumo": texto[:8000],
            "explicacao": "",
            "pontos_chave": "",
        }
    return {
        "resumo": str(data.get("resumo", "")),
        "explicacao": str(data.get("explicacao", "")),
        "pontos_chave": str(data.get("pontos_chave", "")),
    }


def _texto_para_modelo(transcricao: str, max_chars: int = 110_000) -> str:
    t = transcricao.strip()
    if len(t) <= max_chars:
        return t
    return (
        t[:max_chars]
        + "\n\n[... transcrição truncada para o limite do modelo — início e fim preservados ...]\n\n"
        + t[-8000:]
    )


def resumir_openai(transcricao: str, api_key: str, modelo: str) -> dict[str, str]:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    user = f"Transcrição da reunião:\n\n{_texto_para_modelo(transcricao)}"
    resp = client.chat.completions.create(
        model=modelo,
        messages=[
            {"role": "system", "content": PROMPT_RESUMO},
            {"role": "user", "content": user},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content or "{}"
    return _parse_json_resumo(raw)


def resumir_anthropic(transcricao: str, api_key: str, modelo: str) -> dict[str, str]:
    import httpx

    user = (
        f"{PROMPT_RESUMO}\n\nTranscrição:\n\n{_texto_para_modelo(transcricao)}\n\n"
        "Responda somente com o JSON solicitado."
    )
    r = httpx.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": modelo,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": user}],
        },
        timeout=300.0,
    )
    r.raise_for_status()
    data = r.json()
    blocos = data.get("content") or []
    raw = ""
    for b in blocos:
        if b.get("type") == "text":
            raw += b.get("text", "")
    return _parse_json_resumo(raw)


def resumir_transcricao(transcricao: str, cfg: dict[str, str]) -> dict[str, str]:
    c = obter_config_ia(cfg)
    pref = c["preferencia"]
    if pref == "anthropic" and c["anthropic"]:
        return resumir_anthropic(transcricao, c["anthropic"], c["modelo_anthropic"])
    if c["openai"]:
        return resumir_openai(transcricao, c["openai"], c["modelo_openai"])
    if c["anthropic"]:
        return resumir_anthropic(transcricao, c["anthropic"], c["modelo_anthropic"])
    raise ValueError("Configure OPENAI_API_KEY ou ANTHROPIC_API_KEY nos secrets do Streamlit.")


def processar_reuniao_completa(
    caminho_audio: Path,
    cfg: dict[str, str],
    *,
    so_resumo: bool = False,
    transcricao_existente: str | None = None,
) -> dict[str, Any]:
    """Transcreve (se necessário) e gera resumo + explicação."""
    c = obter_config_ia(cfg)
    if so_resumo:
        if not transcricao_existente or not transcricao_existente.strip():
            raise ValueError("Informe a transcrição em texto.")
        texto = transcricao_existente.strip()
    else:
        if not c["openai"]:
            raise ValueError(
                "Transcrição de áudio exige OPENAI_API_KEY (Whisper). "
                "Ou cole a transcrição manualmente."
            )
        texto = transcrever_audio(caminho_audio, c["openai"])
    partes = resumir_transcricao(texto, cfg)
    return {"transcricao": texto, **partes}
