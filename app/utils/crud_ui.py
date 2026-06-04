"""Editor CRUD unificado: criar, ler, editar e excluir linhas em qualquer tabela."""
from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime
from typing import Any

import pandas as pd
import streamlit as st

RID = "_rid"


def proximo_id(df: pd.DataFrame, col: str = "id") -> int:
    if df.empty or col not in df.columns:
        return 1
    nums = pd.to_numeric(df[col], errors="coerce").dropna()
    return int(nums.max()) + 1 if len(nums) else 1


def com_row_ids(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if out.empty:
        out[RID] = []
        return out
    if RID not in out.columns:
        out.insert(0, RID, range(1, len(out) + 1))
    else:
        out[RID] = range(1, len(out) + 1)
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
    """Sem filtro: tabela editada substitui a base (inclui exclusões). Com filtro: só atualiza IDs visíveis."""
    editado = preencher_ids_vazios(editado, id_col)
    if not filtrado:
        return editado
    eids = set(pd.to_numeric(editado[id_col], errors="coerce").dropna().astype(int))
    base = base.copy()
    base_ids = pd.to_numeric(base[id_col], errors="coerce")
    restante = base[~base_ids.isin(eids)]
    return pd.concat([restante, editado], ignore_index=True)


def mesclar_por_rid(base: pd.DataFrame, editado: pd.DataFrame, filtrado: bool) -> pd.DataFrame:
    base = com_row_ids(base)
    editado = com_row_ids(editado)
    if not filtrado:
        editado = preencher_ids_vazios(editado, RID) if RID in editado.columns else editado
        max_rid = int(pd.to_numeric(base[RID], errors="coerce").max() or 0)
        for i in editado.index:
            if pd.isna(editado.at[i, RID]) or editado.at[i, RID] == "":
                max_rid += 1
                editado.at[i, RID] = max_rid
        return sem_row_ids(editado)

    out = base.copy()
    for _, row in editado.iterrows():
        rid = row[RID]
        if rid in out[RID].values:
            for c in editado.columns:
                if c != RID:
                    out.loc[out[RID] == rid, c] = row[c]
    return sem_row_ids(out)


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
    altura: int | None = None,
) -> pd.DataFrame | None:
    """
    Exibe tabela editável com CRUD completo.
    Retorna o DataFrame salvo ou None.
    """
    colunas_data = colunas_data or []
    column_config = column_config or {}

    if st.button("↻ Recarregar do arquivo", key=f"{chave}_reload"):
        st.session_state.pop(f"{chave}_base", None)
        st.rerun()

    if f"{chave}_base" not in st.session_state:
        st.session_state[f"{chave}_base"] = carregar()

    base: pd.DataFrame = st.session_state[f"{chave}_base"]
    if base.empty:
        base = pd.DataFrame(columns=colunas)
    for c in colunas:
        if c not in base.columns:
            base[c] = ""
    base = base[colunas].copy()

    filtrado = False
    exibir = base
    if aplicar_filtro:
        exibir, filtrado = aplicar_filtro(base)

    usa_rid = id_col is None or id_col not in colunas
    editor_df = com_row_ids(exibir) if usa_rid else exibir.copy()

    cols_editor = [RID] + [c for c in colunas if c in editor_df.columns] if usa_rid else colunas
    cfg = dict(column_config)
    if usa_rid:
        cfg[RID] = st.column_config.NumberColumn("Ref.", disabled=True, width="small")

    c1, c2, c3 = st.columns([1, 1, 2])
    if c1.button("➕ Nova linha", key=f"{chave}_add"):
        nova = {c: "" for c in colunas}
        if id_col and id_col in colunas:
            nova[id_col] = proximo_id(base, id_col)
        st.session_state[f"{chave}_base"] = pd.concat(
            [base, pd.DataFrame([nova])], ignore_index=True
        )
        st.rerun()

    if filtrado:
        c3.warning("Filtro ativo: linhas ocultas não serão apagadas ao salvar.")

    st.caption(f"{len(exibir)} linha(s) · Total no cadastro: {len(base)}")

    edited = st.data_editor(
        editor_df[cols_editor] if usa_rid else editor_df,
        num_rows="dynamic",
        use_container_width=True,
        column_config=cfg,
        height=altura,
        key=f"{chave}_editor",
    )

    if c2.button("💾 Salvar tabela", type="primary", key=f"{chave}_save"):
        work = edited.copy()
        if usa_rid:
            work = sem_row_ids(work)
            resultado = mesclar_por_rid(base, com_row_ids(work), filtrado)
        else:
            work = normalizar_datas(work, colunas_data)
            resultado = mesclar_por_id(base, work, id_col, filtrado=filtrado)
            resultado = normalizar_datas(resultado, colunas_data)
            resultado = resultado[colunas]

        salvar(resultado)
        st.session_state[f"{chave}_base"] = carregar()
        st.success("Salvo. Backup automático em backups/.")
        return resultado

    return None
