"""Testa CRUD de todas as abas no Excel (cópia temporária)."""
from __future__ import annotations

import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "app"))

import utils.data_manager as dm  # noqa: E402
from utils.crud_ui import mesclar_por_id, mesclar_por_rid, garantir_rid  # noqa: E402

MARCADOR = "__TESTE_CRUD__"


def _setup_temp_db() -> Path:
    src = dm.EXCEL_PATH
    if not src.exists():
        from inicializar_excel import criar_workbook_inicial

        criar_workbook_inicial()
    tmp = Path(tempfile.mkdtemp())
    dest = tmp / "apostolado.xlsx"
    shutil.copy2(src, dest)
    dm.EXCEL_PATH = dest
    dm.DATA_DIR = tmp
    dm.BACKUPS_DIR = tmp / "backups"
    dm.BACKUPS_DIR.mkdir(exist_ok=True)
    return dest


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_membros() -> None:
    df = dm.ler_membros_df()
    n0 = len(df)
    novo_id = int(df["id"].max()) + 1 if not df.empty else 99
    extra = pd.DataFrame(
        [
            {
                "id": novo_id,
                "num_orig": "T",
                "nome": MARCADOR,
                "sexo": "F",
                "nasc": None,
                "ingresso": None,
                "endereco": "",
                "bairro": "",
                "telefone": "",
                "funcao": "",
                "situacao": "Ativo",
                "consagrada": "Não",
                "observacoes": "teste",
                "pagina": "",
            }
        ]
    )
    dm.salvar_membros_df(pd.concat([df, extra], ignore_index=True))
    df2 = dm.ler_membros_df()
    _assert(len(df2) == n0 + 1, "membros create")
    _assert((df2["nome"] == MARCADOR).any(), "membros read")
    df2.loc[df2["nome"] == MARCADOR, "observacoes"] = "ok"
    dm.salvar_membros_df(df2)
    _assert(
        dm.ler_membros_df().loc[dm.ler_membros_df()["nome"] == MARCADOR, "observacoes"].iloc[0]
        == "ok",
        "membros update",
    )
    df3 = dm.ler_membros_df()
    df3 = df3[df3["nome"] != MARCADOR]
    dm.salvar_membros_df(df3)
    _assert(not (dm.ler_membros_df()["nome"] == MARCADOR).any(), "membros delete")


def test_tabela_id(ler, salvar, cols, id_val: int) -> None:
    df = ler()
    n0 = len(df)
    row = {c: "" for c in cols}
    row["id"] = id_val
    if "data" in cols:
        row["data"] = date.today()
    if "intencao" in cols:
        row["intencao"] = MARCADOR
    if "titulo" in cols:
        row["titulo"] = MARCADOR
    if "membro_nome" in cols:
        row["membro_nome"] = MARCADOR
    if "item" in cols:
        row["item"] = "Nenhum – visita de acompanhamento pastoral"
    if "entregue" in cols:
        row["entregue"] = "N"
    if "realizada" in cols:
        row["realizada"] = "N"
    salvar(pd.concat([df, pd.DataFrame([row])], ignore_index=True))
    df2 = ler()
    _assert(len(df2) == n0 + 1, f"{id_val} create")
    df2 = df2[df2["id"] != id_val] if "id" in df2.columns else df2.iloc[:-1]
    salvar(df2)
    _assert(len(ler()) == n0, f"{id_val} delete")


def test_inconsistencias() -> None:
    df = dm.ler_inconsistencias_df()
    n0 = len(df)
    nova = pd.DataFrame(
        [
            {
                "categoria": "Teste",
                "prioridade": "🔵 Informativa",
                "descricao": MARCADOR,
                "acao_sugerida": "x",
                "resolvida": "Não",
            }
        ]
    )
    dm.salvar_inconsistencias_df(pd.concat([df, nova], ignore_index=True))
    _assert((dm.ler_inconsistencias_df()["descricao"] == MARCADOR).any(), "inc create")
    rest = dm.ler_inconsistencias_df()
    rest = rest[rest["descricao"] != MARCADOR]
    dm.salvar_inconsistencias_df(rest)
    _assert(len(dm.ler_inconsistencias_df()) == n0, "inc delete")


def test_config() -> None:
    df = dm.ler_config_df()
    extra = pd.DataFrame([{"chave": "teste_crud_key", "valor": MARCADOR}])
    dm.salvar_config_df(pd.concat([df, extra], ignore_index=True))
    _assert(MARCADOR in dm.ler_config_df()["valor"].values, "config create")
    df2 = dm.ler_config_df()
    df2 = df2[df2["chave"] != "teste_crud_key"]
    dm.salvar_config_df(df2)
    _assert("teste_crud_key" not in dm.ler_config_df()["chave"].values, "config delete")


def test_memorial() -> None:
    df = dm.ler_memorial()
    n0 = len(df)
    nova = pd.DataFrame([{"nome": MARCADOR, "nasc": None, "falecimento": None, "observacao": "t"}])
    dm.salvar_memorial(pd.concat([df, nova], ignore_index=True))
    _assert((dm.ler_memorial()["nome"] == MARCADOR).any(), "memorial create")
    dm.salvar_memorial(df)
    _assert(len(dm.ler_memorial()) == n0, "memorial delete")


def test_entregas_editor_tipos() -> None:
    df = pd.DataFrame(
        [
            {
                "id": 1,
                "membro_id": 2,
                "membro_nome": "X",
                "item": "Camisa do Apostolado",
                "data_entrega": "",
                "entregue": "N",
                "observacoes": "bairro",
            }
        ]
    )
    prep = dm.preparar_entregas_editor(df)
    _assert(str(prep["data_entrega"].dtype).startswith("datetime"), "data_entrega datetime")
    _assert(prep["id"].dtype == int, "id int")


def test_merge_filtrado() -> None:
    df = pd.DataFrame([{"id": 1, "x": "a"}, {"id": 2, "x": "b"}])
    sub = df[df["id"] == 1].copy()
    sub.loc[sub.index[0], "x"] = "A"
    m = mesclar_por_id(df, sub, filtrado=True)
    _assert(m.loc[m["id"] == 1, "x"].iloc[0] == "A", "merge id")
    _assert(len(m) == 2, "merge id len")


def main() -> None:
    path = _setup_temp_db()
    print(f"Testando cópia: {path}")
    test_entregas_editor_tipos()
    test_merge_filtrado()
    test_membros()
    test_inconsistencias()
    test_config()
    test_memorial()
    test_tabela_id(dm.ler_entregas, dm.salvar_entregas, dm.COL_ENTREGAS, 99901)
    test_tabela_id(dm.ler_visitas, dm.salvar_visitas, dm.COL_VISITAS, 99902)
    test_tabela_id(dm.ler_consagracoes, dm.salvar_consagracoes, dm.COL_CONSAGRACOES, 99903)
    test_tabela_id(dm.ler_intencoes, dm.salvar_intencoes, dm.COL_INTENCOES, 99904)
    test_tabela_id(dm.ler_agenda, dm.salvar_agenda, dm.COL_AGENDA, 99905)
    print("OK — todos os CRUDs gravam e leem o Excel corretamente.")


if __name__ == "__main__":
    main()
