"""Rota de visitas — ordem pelo mapa e lista fácil no celular."""
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.auth import require_login
from utils.ui import botao_grande, cartao_visita, inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.colunas_ui import montar_column_config
from utils.crud_ui import barra_excel_downloads_topo, barra_excel_pagina_custom, mesclar_por_id
from utils.data_manager import COL_ENTREGAS, ler_config, ler_entregas, ler_membros, preparar_data_editor, preparar_dataframe, preparar_entregas_editor, salvar_entregas
from utils.dados_membros import ITENS_ENTREGA, ORDEM_BAIRROS
from utils.endereco import aplicar_filtro_endereco, linha_entrega_visita_de_membro, mesclar_endereco_de_registro
from utils.mapa_rotas import (
    ENDERECO_PAROQUIA_PADRAO,
    ordenar_por_proximidade,
    resumo_distancias,
    url_apple_maps,
    url_google_maps,
    url_rota_google,
    url_waze,
)
from utils.opcoes import ENTREGUE

st.set_page_config(
    page_title="Rota de Visitas",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed",
)
require_login()
inject_css()
st.title("🗺️ Rota de Visitas")
barra_excel_downloads_topo("rota", "Entregas")


def ordem_bairro(b: str) -> int:
    b = b or ""
    for i, nome in enumerate(ORDEM_BAIRROS):
        if nome and (b.lower() == nome.lower() or nome.lower() in b.lower()):
            return i
    return len(ORDEM_BAIRROS)


def _chave_ordenacao(m: dict) -> tuple:
    return (
        ordem_bairro(str(m.get("bairro", ""))),
        str(m.get("cep", "")),
        str(m.get("rua", "")),
        str(m.get("numero", "")),
        str(m.get("nome", "")),
    )


def _linha_rota(m: dict, eid: int) -> dict:
    end = linha_entrega_visita_de_membro(m)
    return {
        "id": eid,
        "membro_id": m["id"],
        "membro_nome": m["nome"],
        **end,
        "item": ITENS_ENTREGA[0],
        "data_entrega": pd.NaT,
        "entregue": "N",
        "observacoes": "",
    }


membros_ativos = [
    m
    for m in ler_membros()
    if m.get("situacao") in ("Ativo", "Ativo (presumido)")
]
membros = {m["id"]: m for m in membros_ativos}
df_full = ler_entregas()
cfg = ler_config()
partida = cfg.get("endereco_paroquia") or ENDERECO_PAROQUIA_PADRAO

if df_full.empty and membros:
    rows = [_linha_rota(m, i) for i, m in enumerate(sorted(membros.values(), key=_chave_ordenacao), 1)]
    df_full = preparar_entregas_editor(pd.DataFrame(rows))
    salvar_entregas(df_full)

a1, a2 = st.columns(2)
with a1:
    if botao_grande("🔄 Montar lista dos ativos", "rota_gerar"):
        rows = [_linha_rota(m, i) for i, m in enumerate(sorted(membros.values(), key=_chave_ordenacao), 1)]
        salvar_entregas(preparar_entregas_editor(pd.DataFrame(rows)))
        st.rerun()
with a2:
    if botao_grande("📍 Ordenar pelo mapa", "rota_mapa", type_btn="primary"):
        linhas = df_full.to_dict("records")
        barra = st.progress(0.0, text="Consultando mapa…")

        def _progresso(atual: int, total: int, nome: str) -> None:
            barra.progress(min(1.0, atual / max(total, 1)), text=f"Consultando mapa… {atual}/{total}: {nome}")

        ordenadas, avisos = ordenar_por_proximidade(
            linhas,
            ponto_partida=partida,
            apenas_pendentes=False,
            ao_avancar=_progresso,
        )
        barra.progress(1.0, text="Mapa pronto")
        novo = preparar_entregas_editor(pd.DataFrame(ordenadas))
        salvar_entregas(
            preparar_dataframe(
                novo,
                COL_ENTREGAS,
                id_col="id",
                colunas_data=["data_entrega"],
            )
        )
        if avisos:
            for msg in avisos[:8]:
                st.warning(msg)
        st.success("Ordem atualizada: da paróquia para o mais perto.")
        st.rerun()

pendentes_total = 0
if not df_full.empty:
    pendentes_total = int((df_full["entregue"].astype(str).str.upper() != "S").sum())
st.metric("Visitas ainda não feitas", pendentes_total)

with st.expander("Filtrar por endereço", expanded=False):
    f1, f2 = st.columns(2)
    with f1:
        filtro_cep = st.text_input("CEP", key="rota_f_cep", placeholder="Ex.: 13380")
        bairros = sorted({str(m.get("bairro", "")).strip() for m in membros_ativos if m.get("bairro")})
        filtro_bairro = st.selectbox("Bairro", ["Todos"] + bairros, key="rota_f_bairro")
    with f2:
        filtro_rua = st.text_input("Rua", key="rota_f_rua")
        cidades = sorted({str(m.get("cidade", "")).strip() for m in membros_ativos if m.get("cidade")})
        filtro_cidade = st.selectbox("Cidade", ["Todos"] + cidades, key="rota_f_cidade")
    if st.button("Limpar filtros", key="rota_limpar_filtro"):
        st.session_state["rota_f_cep"] = ""
        st.session_state["rota_f_rua"] = ""
        st.session_state["rota_f_bairro"] = "Todos"
        st.session_state["rota_f_cidade"] = "Todos"
        st.rerun()

filtrado = any(
    [
        filtro_cep.strip(),
        filtro_bairro != "Todos",
        filtro_rua.strip(),
        filtro_cidade != "Todos",
    ]
)

df = preparar_entregas_editor(df_full.copy())
if filtrado:

    def _linha_passa(r: pd.Series) -> bool:
        mid = int(r["membro_id"]) if pd.notna(r.get("membro_id")) else 0
        m = membros.get(mid)
        if not m:
            reg = {
                "cep": r.get("cep", ""),
                "rua": r.get("rua", ""),
                "numero": r.get("numero", ""),
                "bairro": r.get("bairro", ""),
                "cidade": r.get("cidade", ""),
            }
        else:
            reg = m
        return aplicar_filtro_endereco(
            reg,
            cep=filtro_cep,
            bairro=filtro_bairro,
            rua=filtro_rua,
            cidade=filtro_cidade,
        )

    df = df[df.apply(_linha_passa, axis=1)]
    if filtrado:
        st.warning("Filtro ligado: ao salvar, só muda o que aparece aqui.")

if df.empty:
    if filtrado and not df_full.empty:
        st.warning("Nenhuma visita com esse filtro. Limpe o CEP ou escolha **Todos** nos menus.")
    else:
        st.markdown("### Nenhuma visita na lista")
        st.markdown("Toque em **Montar lista dos ativos** para começar.")
else:
    ver = st.radio(
        "Como ver",
        ["Lista para sair de casa", "Tabela para editar"],
        horizontal=True,
        key="rota_modo",
    )

    if ver == "Lista para sair de casa":
        pendentes = df[df["entregue"].astype(str).str.upper() != "S"]
        lista = pendentes.to_dict("records") if not pendentes.empty else df.to_dict("records")
        resumo = resumo_distancias(lista, membros=membros)

        st.caption(f"{len(lista)} visita(s) nesta lista")
        st.info(
            "A lista aparece na hora. Toque em **Ordenar pelo mapa** para reorganizar "
            "do mais perto ao mais longe (pode levar alguns minutos na primeira vez)."
        )

        if len(lista) >= 2:
            lista_mapa = [
                {**r, **mesclar_endereco_de_registro(r, membros.get(int(r.get("membro_id") or 0)))}
                if membros.get(int(r.get("membro_id") or 0))
                else r
                for r in lista
            ]
            st.link_button(
                "🚗 Abrir rota no Google Maps",
                url_rota_google(lista_mapa),
                use_container_width=True,
            )

        st.markdown("### Próximas visitas")
        for item in resumo:
            km = item.get("km_anterior")
            km_txt = str(km) if km is not None else None
            cartao_visita(item["ordem"], item["nome"], item["endereco"], km_txt)
            m1, m2, m3 = st.columns(3)
            row = item["row"]
            with m1:
                st.link_button("Google", url_google_maps(row), use_container_width=True)
            with m2:
                st.link_button("Apple", url_apple_maps(row), use_container_width=True)
            with m3:
                st.link_button("Waze", url_waze(row), use_container_width=True)
            st.divider()

    else:
        cfg_rota = montar_column_config(
            list(df.columns),
            {
                "id": st.column_config.NumberColumn("ID", format="%d"),
                "membro_id": st.column_config.NumberColumn("ID membro", format="%d"),
                "item": st.column_config.SelectboxColumn("Material / motivo", options=ITENS_ENTREGA),
                "entregue": st.column_config.SelectboxColumn("Entregue?", options=ENTREGUE),
                "data_entrega": st.column_config.DateColumn("Data da entrega", format="DD/MM/YYYY"),
            },
        )
        df_edit, cfg_edit = preparar_data_editor(
            df,
            list(df.columns),
            colunas_data=["data_entrega"],
            id_col="id",
            column_config=cfg_rota,
        )
        edited = st.data_editor(
            df_edit,
            num_rows="dynamic",
            use_container_width=True,
            column_config=cfg_edit,
            height=400,
            hide_index=True,
        )

        merged = mesclar_por_id(df_full, edited, filtrado=filtrado)

        def _salvar_rota(df: pd.DataFrame) -> None:
            salvar_entregas(
                preparar_dataframe(
                    df,
                    COL_ENTREGAS,
                    id_col="id",
                    colunas_data=["data_entrega"],
                )
            )

        barra_excel_pagina_custom(
            chave="rota_edit",
            nome_aba="Entregas",
            df_atual=merged,
            colunas=COL_ENTREGAS,
            colunas_data=["data_entrega"],
            id_col="id",
            ao_salvar=_salvar_rota,
        )
