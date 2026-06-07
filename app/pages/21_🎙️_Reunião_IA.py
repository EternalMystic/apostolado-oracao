"""Reunião semanal: modo grátis (ditado) ou IA (áudio longo)."""
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.ai_reuniao import (
    audios_dir,
    ia_disponivel,
    ler_transcricao,
    obter_config_ia,
    processar_reuniao_completa,
    salvar_audio,
    salvar_transcricao,
    truncar_excel,
)
from utils.auth import require_login
from utils.crud_ui import proximo_id, tabela_crud
from utils.data_manager import ROOT, ler_config, ler_reunioes_ia, salvar_reunioes_ia
from utils.opcoes import STATUS_REUNIAO_IA
from utils.tabelas_apostolado import COL_REUNIOES_IA
from utils.reuniao_gratis import html_dictado_voz, resumo_sem_ia
from utils.ui import inject_css

st.set_page_config(
    page_title="Reunião IA",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
require_login()
inject_css()
st.title("🎙️ Reunião semanal")

cfg = ler_config()
ok_ia, modo_ia = ia_disponivel(cfg)
if ok_ia:
    st.markdown(f"IA disponível ({modo_ia}). Aba **Grátis** não precisa de chave.")
else:
    st.markdown("Use a aba **🆓 Grátis** — ditado no Chrome e resumo automático, sem pagar API.")

tab_gratis, tab_audio, tab_texto, tab_gravar, tab_hist, tab_ajuda = st.tabs(
    [
        "🆓 Grátis (sem IA)",
        "📤 Áudio com IA",
        "📝 Texto com IA",
        "🔴 Gravar curto",
        "📚 Histórico",
        "⚙️ Configurar IA",
    ]
)


def _registrar_linha(**campos) -> int:
    df = ler_reunioes_ia()
    rid = proximo_id(df)
    row = {c: "" for c in COL_REUNIOES_IA}
    row.update(campos)
    row["id"] = rid
    if not row.get("data"):
        row["data"] = date.today()
    salvar_reunioes_ia(pd.concat([df, pd.DataFrame([row])], ignore_index=True))
    return rid


def _salvar_resultado_gratis(
    rid: int,
    resultado: dict[str, str],
    *,
    titulo: str,
    data_reu: date,
    dur: int = 0,
) -> None:
    rel_txt = salvar_transcricao(rid, resultado["transcricao"])
    _atualizar_linha(
        rid,
        titulo=titulo,
        data=data_reu,
        duracao_min=dur,
        status="Concluído (grátis)",
        transcricao_arquivo=rel_txt,
        resumo=truncar_excel(resultado["resumo"]),
        explicacao=truncar_excel(resultado["explicacao"]),
        pontos_chave=truncar_excel(resultado["pontos_chave"]),
        observacoes="Resumo automático sem IA — revise antes de publicar.",
    )


def _atualizar_linha(rid: int, **campos) -> None:
    df = ler_reunioes_ia()
    if df.empty or "id" not in df.columns:
        return
    mask = pd.to_numeric(df["id"], errors="coerce") == rid
    if not mask.any():
        return
    for k, v in campos.items():
        df.loc[mask, k] = v
    salvar_reunioes_ia(df)


with tab_gratis:
    st.markdown(
        "### Ditado por voz (grátis)"
    )
    st.markdown(
        "No **Chrome** do celular: toque *Iniciar ditado*, fale, *Copiar texto* e cole na caixa verde."
    )
    components.html(html_dictado_voz(), height=420, scrolling=True)
    titulo_g = st.text_input("Título", "Reunião semanal", key="tit_gratis")
    data_g = st.date_input("Data", value=date.today(), key="data_gratis")
    texto_g = st.text_area(
        "Texto da reunião (cole o ditado ou digite)",
        height=220,
        key="texto_gratis",
        placeholder="Cole aqui o que foi ditado ou digitado…",
    )
    if st.button("✅ Gerar resumo grátis e salvar", type="primary", use_container_width=True):
        if not texto_g.strip():
            st.error("Escreva ou cole o texto da reunião.")
        else:
            rid = _registrar_linha(
                data=data_g,
                titulo=titulo_g,
                status="Resumindo (grátis)",
            )
            resultado = resumo_sem_ia(texto_g)
            _salvar_resultado_gratis(rid, resultado, titulo=titulo_g, data_reu=data_g)
            st.success("Salvo no histórico. Revise o resumo e copie para Atas se quiser.")
            st.markdown("### Resumo")
            st.write(resultado["resumo"])
            st.markdown("### Pontos importantes")
            st.write(resultado["pontos_chave"])

    st.divider()
    st.markdown("### Ata rápida (sem ditado)")
    presentes = st.text_input("Quem esteve presente", key="ata_presentes")
    deliberacoes = st.text_area("O que foi decidido", height=120, key="ata_delib")
    tarefas = st.text_area("Próximos passos / tarefas", height=100, key="ata_tarefas")
    if st.button("Salvar ata simples", use_container_width=True):
        partes = []
        if presentes.strip():
            partes.append(f"Presentes: {presentes.strip()}")
        if deliberacoes.strip():
            partes.append(f"Deliberações: {deliberacoes.strip()}")
        if tarefas.strip():
            partes.append(f"Tarefas: {tarefas.strip()}")
        if not partes:
            st.error("Preencha pelo menos um campo.")
        else:
            texto_ata = "\n\n".join(partes)
            rid = _registrar_linha(data=date.today(), titulo=titulo_g, status="Ata manual")
            resultado = resumo_sem_ia(texto_ata)
            _salvar_resultado_gratis(rid, resultado, titulo=titulo_g, data_reu=date.today())
            st.success("Ata salva.")

with tab_audio:
    st.markdown(
        """
        Para reuniões de **cerca de 1h10**, use o gravador do celular e envie o arquivo aqui.
        A API Whisper aceita até **25 MB** — exporte em **MP3 mono, 32–48 kbps** se o arquivo for grande.
        """
    )
    titulo = st.text_input("Título da reunião", "Reunião semanal do Apostolado")
    data_reu = st.date_input("Data", value=date.today())
    dur = st.number_input("Duração aproximada (minutos)", min_value=1, max_value=180, value=70)
    arquivo = st.file_uploader(
        "Arquivo de áudio",
        type=["mp3", "m4a", "wav", "webm", "ogg", "mpeg", "mpga"],
        help="Gravação da reunião completa",
    )
    if st.button("Transcrever e resumir com IA", type="primary", disabled=not ok_ia):
        if arquivo is None:
            st.error("Envie um arquivo de áudio.")
        else:
            rid = _registrar_linha(
                data=data_reu,
                titulo=titulo,
                duracao_min=int(dur),
                status="Transcrevendo",
                arquivo_audio="",
                transcricao_arquivo="",
            )
            try:
                dados = arquivo.getvalue()
                rel_audio = salvar_audio(rid, arquivo.name, dados)
                _atualizar_linha(rid, arquivo_audio=rel_audio, status="Transcrevendo")
                caminho = ROOT / rel_audio
                with st.spinner(
                    "Transcrevendo e resumindo… reuniões longas podem levar 5–15 minutos."
                ):
                    resultado = processar_reuniao_completa(caminho, cfg)
                rel_txt = salvar_transcricao(rid, resultado["transcricao"])
                _atualizar_linha(
                    rid,
                    status="Concluído",
                    transcricao_arquivo=rel_txt,
                    resumo=truncar_excel(resultado["resumo"]),
                    explicacao=truncar_excel(resultado["explicacao"]),
                    pontos_chave=truncar_excel(resultado["pontos_chave"]),
                )
                st.success("Pronto! Veja o histórico ou copie para Atas.")
                st.markdown("### Resumo")
                st.write(resultado["resumo"])
                st.markdown("### Explicação")
                st.write(resultado["explicacao"])
                st.markdown("### Pontos-chave")
                st.write(resultado["pontos_chave"])
                with st.expander("Transcrição completa"):
                    st.text_area("", resultado["transcricao"], height=300, disabled=True)
            except Exception as e:
                _atualizar_linha(rid, status="Erro", observacoes=str(e)[:500])
                st.error(f"Erro: {e}")

with tab_texto:
    titulo2 = st.text_input("Título", "Reunião semanal", key="tit_txt")
    data2 = st.date_input("Data", value=date.today(), key="data_txt")
    texto_livre = st.text_area("Transcrição", height=280, placeholder="Cole aqui o texto da reunião…")
    c_ia, c_gr = st.columns(2)
    with c_gr:
        if st.button("Resumo grátis (sem IA)", use_container_width=True):
            if not texto_livre.strip():
                st.error("Cole a transcrição.")
            else:
                rid = _registrar_linha(data=data2, titulo=titulo2, status="Resumindo (grátis)")
                resultado = resumo_sem_ia(texto_livre)
                _salvar_resultado_gratis(rid, resultado, titulo=titulo2, data_reu=data2)
                st.success("Salvo.")
                st.write(resultado["resumo"])
    with c_ia:
        usar_ia = st.button("Resumo com IA", type="primary", disabled=not ok_ia, use_container_width=True)
    if usar_ia:
        if not texto_livre.strip():
            st.error("Cole a transcrição.")
        else:
            rid = _registrar_linha(
                data=data2,
                titulo=titulo2,
                duracao_min=0,
                status="Resumindo",
            )
            try:
                with st.spinner("Analisando com IA…"):
                    resultado = processar_reuniao_completa(
                        Path("."),
                        cfg,
                        so_resumo=True,
                        transcricao_existente=texto_livre,
                    )
                rel_txt = salvar_transcricao(rid, resultado["transcricao"])
                _atualizar_linha(
                    rid,
                    status="Concluído",
                    transcricao_arquivo=rel_txt,
                    resumo=truncar_excel(resultado["resumo"]),
                    explicacao=truncar_excel(resultado["explicacao"]),
                    pontos_chave=truncar_excel(resultado["pontos_chave"]),
                )
                st.success("Resumo salvo no histórico.")
                st.markdown("### Resumo")
                st.write(resultado["resumo"])
                st.markdown("### Explicação")
                st.write(resultado["explicacao"])
            except Exception as e:
                _atualizar_linha(rid, status="Erro", observacoes=str(e)[:500])
                st.error(str(e))

with tab_gravar:
    st.info(
        "Gravação pelo navegador serve para **notas curtas** (o limite do celular costuma ser alguns minutos). "
        "Para a reunião completa (~1h10), grave com o app Gravador do telefone e envie na aba «Enviar áudio»."
    )
    titulo3 = st.text_input("Título", "Nota da reunião", key="tit_grav")
    gravacao = st.audio_input("Gravar áudio")
    if gravacao is not None and st.button("Processar gravação curta", disabled=not ok_ia):
        rid = _registrar_linha(data=date.today(), titulo=titulo3, status="Transcrevendo")
        try:
            rel_audio = salvar_audio(rid, "gravacao.webm", gravacao.getvalue())
            caminho = ROOT / rel_audio
            with st.spinner("Processando…"):
                resultado = processar_reuniao_completa(caminho, cfg)
            rel_txt = salvar_transcricao(rid, resultado["transcricao"])
            _atualizar_linha(
                rid,
                arquivo_audio=rel_audio,
                status="Concluído",
                transcricao_arquivo=rel_txt,
                resumo=truncar_excel(resultado["resumo"]),
                explicacao=truncar_excel(resultado["explicacao"]),
                pontos_chave=truncar_excel(resultado["pontos_chave"]),
            )
            st.success("Processado.")
            st.write(resultado["resumo"])
        except Exception as e:
            _atualizar_linha(rid, status="Erro", observacoes=str(e)[:500])
            st.error(str(e))

with tab_hist:
    hist = ler_reunioes_ia().sort_values("id", ascending=False) if not ler_reunioes_ia().empty else ler_reunioes_ia()
    if not hist.empty:
        opcoes = {
            f"{int(r['id'])} — {r.get('titulo', '')} ({r.get('data', '')})": int(r["id"])
            for _, r in hist.iterrows()
        }
        sel = st.selectbox("Ver reunião", list(opcoes.keys()))
        rid = opcoes[sel]
        row = hist[hist["id"].astype(int) == rid].iloc[0]
        st.markdown(f"**Status:** {row.get('status', '')}")
        st.markdown("### Resumo")
        st.write(row.get("resumo") or "—")
        st.markdown("### Explicação")
        st.write(row.get("explicacao") or "—")
        st.markdown("### Pontos-chave")
        st.write(row.get("pontos_chave") or "—")
        txt = ler_transcricao(row.get("transcricao_arquivo"))
        if txt:
            with st.expander("Transcrição completa"):
                st.download_button(
                    "Baixar transcrição (.txt)",
                    txt,
                    file_name=f"transcricao_{rid}.txt",
                )
                st.text_area("", txt, height=240, disabled=True, key=f"txt_{rid}")
        arq = row.get("arquivo_audio")
        if arq:
            p = ROOT / str(arq)
            if p.exists():
                st.audio(p.read_bytes(), format="audio/mp3")

    st.divider()
    tabela_crud(
        chave="reunioes_ia",
        colunas=COL_REUNIOES_IA,
        carregar=ler_reunioes_ia,
        salvar=salvar_reunioes_ia,
        column_config={
            "data": st.column_config.DateColumn("Data"),
            "status": st.column_config.SelectboxColumn(options=STATUS_REUNIAO_IA),
            "duracao_min": st.column_config.NumberColumn("Minutos", min_value=0),
        },
        colunas_data=["data"],
        id_col="id",
        altura=260,
        aba_excel="Reunioes_IA",
    )

with tab_ajuda:
    c = obter_config_ia(cfg)
    st.markdown(
        f"""
### Como ativar a IA (você paga direto à OpenAI e/ou Anthropic)

1. Crie uma chave em [platform.openai.com](https://platform.openai.com/api-keys) (Whisper + GPT).
2. Opcional: chave em [console.anthropic.com](https://console.anthropic.com/) (Claude para resumo).
3. No **Streamlit Cloud** → seu app → **Settings** → **Secrets**, cole:

```toml
OPENAI_API_KEY = "sk-..."
# opcional
ANTHROPIC_API_KEY = "sk-ant-..."
AI_PREFERENCIA = "openai"
AI_MODELO_OPENAI = "gpt-4o-mini"
AI_MODELO_ANTHROPIC = "claude-3-5-haiku-20241022"
```

4. Salve e aguarde o app reiniciar.

**Custos aproximados (reunião ~70 min):** transcrição Whisper ~US$ 0,40; resumo GPT-4o-mini ~US$ 0,05–0,15.

**Arquivos:** áudios em `{audios_dir().relative_to(ROOT)}` · transcrições em `data/transcricoes/`.
Inclua na pasta ao baixar backup do servidor.

**Nuvem:** no Streamlit Cloud os arquivos podem sumir se o app reiniciar — baixe transcrições e o Excel em Configurações.
"""
    )
    st.caption(f"Chave OpenAI detectada: {'sim' if c['openai'] else 'não'} · Anthropic: {'sim' if c['anthropic'] else 'não'}")
