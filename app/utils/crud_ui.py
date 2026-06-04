"""Editor CRUD unificado: criar, ler, editar e excluir linhas em qualquer tabela."""
from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime
from typing import Any

import pandas as pd
import streamlit as st

from utils.data_manager import preparar_dataframe

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
) -> pd.DataFrame | None:
    colunas_data = colunas_data or []
    column_config = column_config or {}
    usa_rid = id_col is None or id_col not in colunas

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
    cfg = dict(column_config)
    if usa_rid:
        exibir = garantir_rid(exibir)
        cols_editor = [RID] + colunas
        cfg[RID] = st.column_config.NumberColumn("Ref.", disabled=True, width="small")

    c1, c2, _ = st.columns([1, 1, 1])
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

    st.caption(
        f"{len(exibir)} linha(s) visíveis · {len(base)} no cadastro · "
        "Toque na célula para editar"
    )

    edited = st.data_editor(
        exibir[cols_editor],
        num_rows="dynamic",
        use_container_width=True,
        column_config=cfg,
        height=altura,
        key=f"{chave}_editor",
    )

    if c2.button("💾 Salvar", type="primary", key=f"{chave}_save"):
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
            st.success("Salvo no apostolado.xlsx · backup em backups/")
            st.rerun()
            return resultado
        except Exception as e:
            st.error(f"Erro ao salvar: {e}")

    return None
