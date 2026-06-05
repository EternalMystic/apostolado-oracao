"""Reunião sem IA paga: dictado no navegador e resumo automático simples (grátis)."""
from __future__ import annotations

import re
from typing import Any

# Palavras que costumam indicar decisão ou tarefa em atas de paróquia
_MARCADORES = (
    "decidimos",
    "decidiu",
    "combinamos",
    "ficou",
    "ficou definido",
    "próximo",
    "proximo",
    "tarefa",
    "responsável",
    "responsavel",
    "vamos",
    "precisa",
    "oração",
    "oracao",
    "intenção",
    "intencao",
    "visita",
    "entrega",
    "zelador",
    "diretoria",
)


def _frases(texto: str) -> list[str]:
    bruto = re.split(r"(?<=[.!?])\s+|\n+", texto.strip())
    return [f.strip() for f in bruto if len(f.strip()) > 8]


def _linhas_destaque(texto: str) -> list[str]:
    out: list[str] = []
    for linha in texto.splitlines():
        t = linha.strip()
        if not t or len(t) < 12:
            continue
        if t.startswith(("-", "•", "*")) or re.match(r"^\d+[\.\)]\s", t):
            out.append(t.lstrip("-•* ").strip())
            continue
        low = t.lower()
        if any(m in low for m in _MARCADORES):
            out.append(t)
    return out[:25]


def resumo_sem_ia(texto: str) -> dict[str, str]:
    """
    Resumo extractivo (sem API): frases iniciais + linhas com decisões/tarefas.
    """
    texto = (texto or "").strip()
    if not texto:
        return {
            "transcricao": "",
            "resumo": "Nenhum texto para resumir.",
            "explicacao": "",
            "pontos_chave": "",
        }

    frases = _frases(texto)
    destaques = _linhas_destaque(texto)

    resumo_partes = frases[:4]
    if len(frases) > 6:
        resumo_partes.append("…")
        resumo_partes.extend(frases[-2:])
    resumo = " ".join(resumo_partes)
    if len(resumo) > 1200:
        resumo = resumo[:1197] + "…"

    explicacao = (
        f"Resumo automático (sem IA): {len(frases)} trechos no texto, "
        f"cerca de {len(texto.split())} palavras. "
        "Revise e complete na aba Atas se precisar."
    )

    if destaques:
        pontos = "\n".join(f"• {p}" for p in destaques[:15])
    else:
        pontos = "\n".join(f"• {f}" for f in frases[4:14]) if len(frases) > 4 else "• (Revise o texto e marque decisões manualmente.)"

    return {
        "transcricao": texto,
        "resumo": resumo,
        "explicacao": explicacao,
        "pontos_chave": pontos,
    }


def html_dictado_voz(altura: int = 320) -> str:
    """Chrome/Edge no celular: ditado em português (Web Speech API, grátis)."""
    return f"""
<div style="font-family: system-ui; max-width: 100%;">
  <p style="font-size: 1.1rem; margin: 0 0 0.5rem 0;">
    Toque <b>Iniciar ditado</b>, fale devagar, depois <b>Copiar texto</b> e cole na caixa abaixo do quadro.
  </p>
  <button type="button" id="btnStart" style="font-size:1.2rem;padding:0.75rem 1.2rem;margin:0.25rem;
    background:#2E7D32;color:white;border:none;border-radius:12px;font-weight:bold;">
    🎤 Iniciar ditado
  </button>
  <button type="button" id="btnStop" style="font-size:1.2rem;padding:0.75rem 1.2rem;margin:0.25rem;
    background:#C62828;color:white;border:none;border-radius:12px;font-weight:bold;">
    ⏹ Parar
  </button>
  <button type="button" id="btnCopy" style="font-size:1.2rem;padding:0.75rem 1.2rem;margin:0.25rem;
    background:#1565C0;color:white;border:none;border-radius:12px;font-weight:bold;">
    📋 Copiar texto
  </button>
  <textarea id="saidas" rows="10" style="width:100%;font-size:1.15rem;margin-top:0.75rem;padding:0.5rem;
    border:3px solid #6A1B9A;border-radius:12px;min-height:{altura}px;"
    placeholder="O que você falar aparece aqui…"></textarea>
  <p id="status" style="font-size:1rem;color:#333;"></p>
</div>
<script>
(function() {{
  const area = document.getElementById('saidas');
  const status = document.getElementById('status');
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) {{
    status.textContent = 'Este navegador não tem ditado. Use Chrome no Android ou cole o texto manualmente.';
    return;
  }}
  const rec = new SR();
  rec.lang = 'pt-BR';
  rec.continuous = true;
  rec.interimResults = true;
  let ativo = false;
  rec.onresult = function(e) {{
    let fin = '', tmp = '';
    for (let i = e.resultIndex; i < e.results.length; i++) {{
      const t = e.results[i][0].transcript;
      if (e.results[i].isFinal) fin += t + ' ';
      else tmp += t;
    }}
    if (fin) area.value += fin;
    status.textContent = tmp ? 'Ouvindo: ' + tmp : 'Gravando ditado…';
  }};
  rec.onerror = function(e) {{ status.textContent = 'Erro: ' + e.error; ativo = false; }};
  rec.onend = function() {{ if (ativo) try {{ rec.start(); }} catch(x) {{}} }};
  document.getElementById('btnStart').onclick = function() {{
    ativo = true;
    try {{ rec.start(); status.textContent = 'Ditado ligado — fale agora'; }} catch(x) {{
      status.textContent = 'Já está gravando ou microfone bloqueado.';
    }}
  }};
  document.getElementById('btnStop').onclick = function() {{
    ativo = false;
    rec.stop();
    status.textContent = 'Ditado parado.';
  }};
  document.getElementById('btnCopy').onclick = function() {{
    area.select();
    document.execCommand('copy');
    status.textContent = 'Copiado! Cole na caixa verde abaixo deste quadro.';
  }};
}})();
</script>
"""
