"""Valida tipos do data_editor em todas as tabelas CRUD."""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

import utils.data_manager as dm  # noqa: E402
import utils.tabelas_apostolado as ta  # noqa: E402
from utils.colunas_ui import montar_column_config  # noqa: E402
from utils.data_manager import preparar_data_editor  # noqa: E402
from utils.dados_membros import ITENS_ENTREGA  # noqa: E402
from utils.opcoes import (  # noqa: E402
    ATIVO_SN,
    CARGOS_DIRETORIA,
    CATEGORIA_INTENCAO,
    CONSAGRADA,
    DIVULGADA,
    ENTREGUE,
    FITA_CONSAGRACAO,
    PRIORIDADE_INTENCAO,
    PRIORIDADES,
    REALIZADA,
    RESOLVIDA,
    SEXOS,
    SITUACOES,
    STATUS_INTENCAO,
    STATUS_REUNIAO_IA,
    STATUS_SUGESTAO,
    TIPOS_AGENDA,
    TIPOS_COMUNICACAO,
    TIPOS_REUNIAO,
    TIPOS_SUGESTAO,
    TIPOS_VISITA,
    TIPO_MEMBRO,
)


def _chk_select(df, col, cfg) -> None:
    opts = set(str(o) for o in getattr(cfg, "options", []) or [])
    for v in df[col].tolist():
        s = str(v).strip()
        if s and s not in opts:
            raise AssertionError(f"{col}={s!r} fora de {sorted(opts)}")


def _case(name, df, cols, cfg, *, colunas_data=None, id_col="id") -> None:
    prep, cfg2 = preparar_data_editor(
        df,
        cols,
        colunas_data=colunas_data or [],
        id_col=id_col,
        column_config=cfg,
    )
    for c, cc in cfg2.items():
        if c not in prep.columns:
            continue
        if type(cc).__name__ == "SelectboxColumn":
            _chk_select(prep, c, cc)
        if type(cc).__name__ == "DateColumn":
            if not prep[c].isna().all() and prep[c].dtype.kind not in "M":
                raise AssertionError(f"{name}.{c} deveria ser datetime, veio {prep[c].dtype}")
    print(f"OK {name} ({len(prep)} linhas)")


def main() -> None:
    _case(
        "membros",
        dm.ler_membros_df(),
        dm.COL_MEMBROS,
        montar_column_config(
            dm.COL_MEMBROS,
            {
                "sexo": st.column_config.SelectboxColumn(options=SEXOS),
                "situacao": st.column_config.SelectboxColumn(options=SITUACOES),
                "consagrada": st.column_config.SelectboxColumn(options=CONSAGRADA),
                "tipo_membro": st.column_config.SelectboxColumn(options=TIPO_MEMBRO),
                "comunidade": st.column_config.SelectboxColumn(options=dm.listar_comunidades()),
                "fita_consagracao": st.column_config.SelectboxColumn(options=FITA_CONSAGRACAO),
                "nasc": st.column_config.DateColumn("Nascimento"),
                "ingresso": st.column_config.DateColumn("Ingresso"),
                "data_inscricao": st.column_config.DateColumn("Inscrição"),
            },
        ),
        colunas_data=["nasc", "ingresso", "data_inscricao"],
    )
    _case(
        "centros",
        dm.ler_centros(),
        ta.COL_CENTROS,
        montar_column_config(
            ta.COL_CENTROS,
            {
                "comunidade": st.column_config.SelectboxColumn(options=dm.listar_comunidades()),
                "ativo": st.column_config.SelectboxColumn(options=ATIVO_SN),
            },
        ),
    )
    _case(
        "consagracoes",
        dm.ler_consagracoes(),
        dm.COL_CONSAGRACOES,
        montar_column_config(
            dm.COL_CONSAGRACOES,
            {"data_consagracao": st.column_config.DateColumn("Data")},
        ),
        colunas_data=["data_consagracao"],
    )
    _case(
        "entregas",
        dm.ler_entregas(),
        dm.COL_ENTREGAS,
        montar_column_config(
            dm.COL_ENTREGAS,
            {
                "item": st.column_config.SelectboxColumn(options=ITENS_ENTREGA),
                "entregue": st.column_config.SelectboxColumn(options=ENTREGUE),
                "data_entrega": st.column_config.DateColumn("Data"),
            },
        ),
        colunas_data=["data_entrega"],
    )
    _case(
        "diretoria",
        dm.ler_diretoria(),
        ta.COL_DIRETORIA,
        montar_column_config(
            ta.COL_DIRETORIA,
            {
                "cargo": st.column_config.SelectboxColumn(options=CARGOS_DIRETORIA),
                "ativo": st.column_config.SelectboxColumn(options=ATIVO_SN),
                "mandato_inicio": st.column_config.DateColumn("Início"),
            },
        ),
        colunas_data=["mandato_inicio"],
    )
    _case(
        "intencoes_papa",
        dm.ler_intencoes_papa(),
        ta.COL_INTENCOES_PAPA,
        montar_column_config(
            ta.COL_INTENCOES_PAPA,
            {"divulgada": st.column_config.SelectboxColumn(options=DIVULGADA)},
        ),
    )
    _case(
        "inconsistencias",
        dm.ler_inconsistencias_df(),
        dm.COL_INCONSISTENCIAS,
        montar_column_config(
            dm.COL_INCONSISTENCIAS,
            {
                "prioridade": st.column_config.SelectboxColumn(options=PRIORIDADES),
                "resolvida": st.column_config.SelectboxColumn(options=RESOLVIDA),
            },
        ),
        id_col=None,
    )
    print("OK — editor compatível em todas as tabelas testadas.")


if __name__ == "__main__":
    main()
