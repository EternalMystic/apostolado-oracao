"""Editor CRUD unificado: criar, ler, editar e excluir linhas em qualquer tabela."""

from __future__ import annotations



from collections.abc import Callable

from datetime import date, datetime

from typing import Any



import pandas as pd

import streamlit as st



from utils.colunas_ui import montar_column_config

from utils.data_manager import preparar_data_editor, preparar_dataframe

from utils.excel_export import (

    bytes_excel_aba,

    bytes_excel_com_abas_atualizadas,

    bytes_excel_completo,

    nome_arquivo_aba,

    nome_arquivo_completo,

)



RID = "_rid"





def proximo_id(df: pd.DataFrame, col: str = "id") -> int:

    if df.empty or col not in df.columns:

        return 1

    nums = pd.to_numeric(df[col], errors="coerce").dropna()

    return int(nums.max()) + 1 if len(nums) else 1





def proximo_rid(df: pd.DataFrame) -> int:

    if df.empty or RID not in df.columns:

        return 1

    nums = pd.to_numeric(df[RID], errors="coerce").dropna()

    return int(nums.max()) + 1 if len(nums) else 1





def garantir_rid(df: pd.DataFrame) -> pd.DataFrame:

    """IDs de linha estáveis (não renumeram ao filtrar)."""

    out = df.copy()

    if out.empty:

        out[RID] = pd.Series(dtype=int)

        return out

    if RID not in out.columns:

        out[RID] = list(range(1, len(out) + 1))

        return out

    nums = pd.to_numeric(out[RID], errors="coerce")

    maxr = int(nums.max()) if nums.notna().any() else 0

    for i in out.index:

        if pd.isna(out.at[i, RID]):

            maxr += 1

            out.at[i, RID] = maxr

    return out





def sem_row_ids(df: pd.DataFrame) -> pd.DataFrame:

    if RID in df.columns:

        return df.drop(columns=[RID])

    return df





def normalizar_datas(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:

    out = df.copy()

    for c in cols:

        if c not in out.columns:

            continue

        for i in out.index:

            v = out.at[i, c]

            if v is None or v == "" or (isinstance(v, float) and pd.isna(v)):

                out.at[i, c] = None

                continue

            if isinstance(v, date) and not isinstance(v, datetime):

                continue

            if isinstance(v, datetime):

                out.at[i, c] = v.date()

                continue

            try:

                ts = pd.to_datetime(v, errors="coerce")

                out.at[i, c] = ts.date() if pd.notna(ts) else None

            except Exception:

                out.at[i, c] = None

    return out





def preencher_ids_vazios(df: pd.DataFrame, col: str = "id") -> pd.DataFrame:

    if col not in df.columns:

        return df

    out = df.copy()

    nxt = proximo_id(out, col)

    for i in out.index:

        v = out.at[i, col]

        if pd.isna(v) or v == "" or v == 0:

            out.at[i, col] = nxt

            nxt += 1

    return out





def mesclar_por_id(

    base: pd.DataFrame, editado: pd.DataFrame, id_col: str = "id", *, filtrado: bool = False

) -> pd.DataFrame:

    editado = preencher_ids_vazios(editado, id_col)

    if not filtrado:

        return editado.reset_index(drop=True)

    eids = set(pd.to_numeric(editado[id_col], errors="coerce").dropna().astype(int))

    base_ids = pd.to_numeric(base[id_col], errors="coerce")

    restante = base[~base_ids.isin(eids)]

    return pd.concat([restante, editado], ignore_index=True)





def mesclar_por_rid(base: pd.DataFrame, editado: pd.DataFrame, filtrado: bool) -> pd.DataFrame:

    base = garantir_rid(base)

    editado = garantir_rid(editado)

    if not filtrado:

        return sem_row_ids(editado).reset_index(drop=True)



    out = base.copy()

    for _, row in editado.iterrows():

        rid = row[RID]

        mask = out[RID] == rid

        if mask.any():

            for c in editado.columns:

                if c != RID and c in out.columns:

                    out.loc[mask, c] = row[c]

    return sem_row_ids(out).reset_index(drop=True)





def _df_para_exportar(

    edited: pd.DataFrame,

    colunas: list[str],

    *,

    usa_rid: bool,

    base: pd.DataFrame,

    filtrado: bool,

    id_col: str | None,

) -> pd.DataFrame:

    if usa_rid:

        work = garantir_rid(edited)

        return mesclar_por_rid(base, work, filtrado)

    work = edited.copy()

    if id_col and id_col in colunas:

        work = preencher_ids_vazios(work, id_col)

    if filtrado and id_col:

        return mesclar_por_id(base, work, id_col, filtrado=True)

    return work[colunas].copy() if all(c in work.columns for c in colunas) else work





def barra_excel_downloads_topo(chave: str, nome_aba: str) -> None:

    """Downloads do arquivo já salvo (topo da página)."""

    completo = bytes_excel_completo()

    st.markdown('<div class="barra-excel-box">', unsafe_allow_html=True)

    st.markdown(f"### 📗 Excel — aba **{nome_aba}**")

    c1, c2 = st.columns(2)

    with c1:

        if completo:

            st.download_button(

                "⬇️ BAIXAR EXCEL COMPLETO",

                data=completo,

                file_name=nome_arquivo_completo(),

                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                key=f"{chave}_dl_full_top",

                use_container_width=True,

            )

        else:

            st.button("⬇️ BAIXAR EXCEL COMPLETO", disabled=True, use_container_width=True)

    with c2:

        st.markdown(

            "<p style='font-size:1.05rem;margin:0.25rem 0;'>"

            "Depois de editar a tabela, use os botões <b>verdes</b> abaixo da lista "

            "para <b>salvar</b> e baixar com suas alterações.</p>",

            unsafe_allow_html=True,

        )

    st.markdown("</div>", unsafe_allow_html=True)





def _barra_excel_acoes(

    *,

    chave: str,

    nome_aba: str,

    df_export: pd.DataFrame,

    colunas: list[str],

    colunas_data: list[str],

    id_col: str | None,

) -> bool:

    """Botões salvar + baixar (abaixo da tabela). Retorna True se salvou."""

    st.markdown('<div class="barra-excel-box">', unsafe_allow_html=True)

    st.markdown("### 📗 Salvar no Excel e baixar")

    b_save, b_aba, b_full = st.columns(3)



    salvou = False

    with b_save:

        if st.button(

            "💾 SALVAR NO EXCEL",

            type="primary",

            key=f"{chave}_save",

            use_container_width=True,

        ):

            salvou = True



    df_aba = preparar_dataframe(

        df_export,

        colunas,

        id_col=id_col if id_col and id_col in colunas else None,

        colunas_data=colunas_data,

    )

    payload_aba = bytes_excel_aba(nome_aba, df_aba)



    with b_aba:

        st.download_button(

            "⬇️ BAIXAR ESTA ABA",

            data=payload_aba,

            file_name=nome_arquivo_aba(nome_aba),

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            key=f"{chave}_dl_aba",

            use_container_width=True,

            help="Planilha só desta tela, com o que está na lista agora",

        )



    completo = bytes_excel_completo()

    workbook = (

        bytes_excel_com_abas_atualizadas({nome_aba: df_aba})

        if completo

        else payload_aba

    )

    with b_full:

        st.download_button(

            "⬇️ BAIXAR TUDO (.xlsx)",

            data=workbook,

            file_name=nome_arquivo_completo(),

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            key=f"{chave}_dl_full",

            use_container_width=True,

            help="Arquivo completo; esta aba traz as alterações visíveis na tela",

        )



    st.markdown("</div>", unsafe_allow_html=True)

    return salvou





def tabela_crud(

    *,

    chave: str,

    colunas: list[str],

    carregar: Callable[[], pd.DataFrame],

    salvar: Callable[[pd.DataFrame], None],

    column_config: dict[str, Any] | None = None,

    colunas_data: list[str] | None = None,

    id_col: str | None = "id",

    aplicar_filtro: Callable[[pd.DataFrame], tuple[pd.DataFrame, bool]] | None = None,

    altura: int | None = 420,

    aba_excel: str | None = None,

) -> pd.DataFrame | None:

    colunas_data = colunas_data or []

    column_config = column_config or {}

    usa_rid = id_col is None or id_col not in colunas

    nome_aba = aba_excel or chave.replace("_", " ").title()



    if aba_excel:

        barra_excel_downloads_topo(chave, nome_aba)



    if st.button("↻ Recarregar do arquivo", key=f"{chave}_reload"):

        st.session_state.pop(f"{chave}_base", None)

        st.rerun()



    if f"{chave}_base" not in st.session_state:

        raw = carregar()

        for c in colunas:

            if c not in raw.columns:

                raw[c] = ""

        raw = raw[colunas].copy()

        if usa_rid:

            raw = garantir_rid(raw)

        st.session_state[f"{chave}_base"] = raw



    base: pd.DataFrame = st.session_state[f"{chave}_base"].copy()



    filtrado = False

    exibir = base

    if aplicar_filtro:

        exibir, filtrado = aplicar_filtro(base)



    cols_editor = colunas.copy()

    cfg = montar_column_config(colunas, column_config)

    if usa_rid:

        exibir = garantir_rid(exibir)

        cols_editor = [RID] + colunas

        cfg[RID] = st.column_config.NumberColumn("Ref.", disabled=True, width="small")



    c1, _ = st.columns([1, 3])

    if c1.button("➕ Nova linha", key=f"{chave}_add"):

        nova = {c: "" for c in colunas}

        if id_col and id_col in colunas:

            nova[id_col] = proximo_id(base, id_col)

        row_df = pd.DataFrame([nova])

        if usa_rid:

            row_df = garantir_rid(row_df)

            row_df.at[0, RID] = proximo_rid(base)

        st.session_state[f"{chave}_base"] = pd.concat([base, row_df], ignore_index=True)

        st.rerun()



    if filtrado:

        st.warning("Filtro ativo: linhas ocultas não serão apagadas ao salvar.")



    if not st.session_state.get("modo_facil", True):

        st.caption(

            f"{len(exibir)} linha(s) visíveis · {len(base)} no cadastro · "

            "Toque na célula para editar"

        )



    df_editor, cfg_editor = preparar_data_editor(
        exibir[cols_editor].copy(),
        cols_editor,
        colunas_data=colunas_data,
        id_col=id_col if id_col and id_col in cols_editor else None,
        column_config=cfg,
    )

    edited = st.data_editor(

        df_editor,

        num_rows="dynamic",

        use_container_width=True,

        column_config=cfg_editor,

        height=altura,

        key=f"{chave}_editor",

    )



    df_export = _df_para_exportar(

        edited,

        colunas,

        usa_rid=usa_rid,

        base=base,

        filtrado=filtrado,

        id_col=id_col,

    )



    quer_salvar = _barra_excel_acoes(

        chave=chave,

        nome_aba=nome_aba,

        df_export=df_export,

        colunas=colunas,

        colunas_data=colunas_data,

        id_col=id_col,

    )



    if quer_salvar:

        try:

            if usa_rid:

                work = garantir_rid(edited)

                resultado = mesclar_por_rid(base, work, filtrado)

            else:

                work = normalizar_datas(edited.copy(), colunas_data)

                resultado = mesclar_por_id(base, work, id_col or "id", filtrado=filtrado)

                resultado = normalizar_datas(resultado, colunas_data)



            resultado = preparar_dataframe(

                resultado,

                colunas,

                id_col=id_col if id_col in colunas else None,

                colunas_data=colunas_data,

            )

            salvar(resultado)

            st.session_state.pop(f"{chave}_base", None)

            st.success("Salvo no apostolado.xlsx · cópia em backups/")

            st.rerun()

            return resultado

        except Exception as e:

            st.error(f"Erro ao salvar: {e}")



    return None





def barra_excel_pagina_custom(

    *,

    chave: str,

    nome_aba: str,

    df_atual: pd.DataFrame,

    colunas: list[str],

    colunas_data: list[str] | None = None,

    id_col: str | None = "id",

    ao_salvar: Callable[[pd.DataFrame], None] | None = None,

) -> bool:

    """Para páginas que não usam tabela_crud (ex.: Rota de Visitas)."""

    colunas_data = colunas_data or []

    _barra_excel_topo(chave, nome_aba)



    df_export = preparar_dataframe(

        df_atual,

        colunas,

        id_col=id_col if id_col and id_col in colunas else None,

        colunas_data=colunas_data,

    )



    st.markdown('<div class="barra-excel-box">', unsafe_allow_html=True)

    st.markdown("### 📗 Salvar no Excel e baixar")

    b_save, b_aba, b_full = st.columns(3)

    salvou = False

    with b_save:

        if st.button(

            "💾 SALVAR NO EXCEL",

            type="primary",

            key=f"{chave}_save_custom",

            use_container_width=True,

        ):

            salvou = True

    payload_aba = bytes_excel_aba(nome_aba, df_export)

    with b_aba:

        st.download_button(

            "⬇️ BAIXAR ESTA ABA",

            data=payload_aba,

            file_name=nome_arquivo_aba(nome_aba),

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            key=f"{chave}_dl_aba_c",

            use_container_width=True,

        )

    workbook = bytes_excel_com_abas_atualizadas({nome_aba: df_export})

    with b_full:

        st.download_button(

            "⬇️ BAIXAR TUDO (.xlsx)",

            data=workbook,

            file_name=nome_arquivo_completo(),

            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

            key=f"{chave}_dl_full_c",

            use_container_width=True,

        )

    st.markdown("</div>", unsafe_allow_html=True)



    if salvou and ao_salvar:

        try:

            ao_salvar(df_export)

            st.success("Salvo no apostolado.xlsx · cópia em backups/")

            st.rerun()

            return True

        except Exception as e:

            st.error(f"Erro ao salvar: {e}")

    return salvou


