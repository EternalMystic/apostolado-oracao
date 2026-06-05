"""Leitura/escrita do Excel com backup automático antes de cada gravação."""
from __future__ import annotations

import shutil
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

try:
    from . import tabelas_apostolado as _ta
except ImportError:
    try:
        from utils import tabelas_apostolado as _ta
    except ImportError:
        import tabelas_apostolado as _ta

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT / "data"
BACKUPS_DIR = ROOT / "backups"
EXCEL_PATH = DATA_DIR / "apostolado.xlsx"

# Mensagem única após recuperar arquivo corrompido (ex.: nuvem Streamlit)
ULTIMA_RECUPERACAO: str | None = None
_recuperando_excel = False

SHEET_MEMBROS = "Membros"
SHEET_INCONSISTENCIAS = "Inconsistencias"
SHEET_ENTREGAS = "Entregas"
SHEET_VISITAS = "Visitas"
SHEET_CONSAGRACOES = "Consagracoes"
SHEET_INTENCOES = "Intencoes"
SHEET_AGENDA = "Agenda"
SHEET_CONFIG = "Config"
SHEET_MEMORIAL = "Memorial"

COL_MEMBROS = [
    "id", "num_orig", "nome", "sexo", "nasc", "ingresso",
    "rua", "numero", "bairro", "cep", "cidade",
    "telefone", "funcao", "situacao", "consagrada", "observacoes", "pagina",
    "tipo_membro", "comunidade", "data_inscricao", "fita_consagracao",
]
COL_ENDERECO = ["cep", "rua", "numero", "bairro", "cidade"]
COL_INCONSISTENCIAS = [
    "categoria", "prioridade", "descricao", "acao_sugerida", "resolvida",
]
COL_ENTREGAS = [
    "id", "membro_id", "membro_nome",
    *COL_ENDERECO,
    "item", "data_entrega", "entregue", "observacoes",
]
COL_VISITAS = [
    "id", "membro_id", "membro_nome", "data_visita",
    *COL_ENDERECO,
    "item", "realizada", "tipo_visita", "nota_pastoral", "observacoes",
]
COL_CONSAGRACOES = [
    "id", "membro_id", "membro_nome", "data_consagracao", "local", "observacoes",
]
COL_INTENCOES = [
    "id", "data", "categoria", "intencao", "solicitante", "status", "prioridade", "observacoes",
]
COL_AGENDA = [
    "id", "data", "hora", "titulo", "tipo", "local", "responsavel", "observacoes",
]
COL_CONFIG = ["chave", "valor"]
COL_MEMORIAL = ["nome", "nasc", "falecimento", "observacao"]


def _migrar_membros_endereco(df: pd.DataFrame) -> pd.DataFrame:
    try:
        from .endereco import separar_endereco_legacy
    except ImportError:
        from endereco import separar_endereco_legacy

    out = df.copy()
    if "endereco" in out.columns and "rua" not in out.columns:
        out["rua"] = out["endereco"]
        mudou = True
    else:
        mudou = False
    for c in COL_MEMBROS:
        if c not in out.columns:
            out[c] = ""
            mudou = True
    for i in out.index:
        if not str(out.at[i, "rua"]).strip() and "endereco" in df.columns:
            leg = str(df.at[i, "endereco"] if i in df.index else "")
            if leg:
                out.at[i, "rua"] = leg
        if not str(out.at[i, "numero"]).strip() or not str(out.at[i, "cidade"]).strip():
            sep = separar_endereco_legacy(
                str(out.at[i, "rua"]),
                str(out.at[i, "bairro"]),
                str(out.at[i, "cidade"]) if str(out.at[i, "cidade"]).strip() else "",
            )
            if not str(out.at[i, "numero"]).strip() and sep["numero"]:
                out.at[i, "numero"] = sep["numero"]
                out.at[i, "rua"] = sep["rua"]
                mudou = True
            if not str(out.at[i, "cidade"]).strip():
                out.at[i, "cidade"] = sep["cidade"]
                mudou = True
    if "endereco" in out.columns:
        out = out.drop(columns=["endereco"])
        mudou = True
    return out.reindex(columns=COL_MEMBROS), mudou


def _mapa_membros_por_id() -> dict[int, dict[str, str]]:
    try:
        from .endereco import linha_entrega_visita_de_membro
    except ImportError:
        from endereco import linha_entrega_visita_de_membro

    df = ler_membros_df()
    mp: dict[int, dict[str, str]] = {}
    for _, r in df.iterrows():
        mid = int(pd.to_numeric(r.get("id"), errors="coerce") or 0)
        if mid:
            mp[mid] = linha_entrega_visita_de_membro(r.to_dict())
    return mp


def _migrar_planilha_endereco(
    df: pd.DataFrame, cols: list[str], mapa: dict[int, dict[str, str]]
) -> tuple[pd.DataFrame, bool]:
    out = df.copy()
    mudou = False
    for c in cols:
        if c not in out.columns:
            out[c] = ""
            mudou = True
    for i in out.index:
        mid_raw = pd.to_numeric(out.at[i, "membro_id"], errors="coerce")
        mid = int(mid_raw) if pd.notna(mid_raw) else 0
        mem = mapa.get(mid, {})
        for k in COL_ENDERECO:
            if mem.get(k) and not str(out.at[i, k]).strip():
                out.at[i, k] = mem[k]
                mudou = True
        obs = str(out.at[i, "observacoes"]).strip()
        bairro_mem = mem.get("bairro", "")
        if obs and bairro_mem and obs == bairro_mem and not str(out.at[i, "bairro"]).strip():
            out.at[i, "bairro"] = obs
            out.at[i, "observacoes"] = ""
            mudou = True
        elif obs and not any(str(out.at[i, k]).strip() for k in COL_ENDERECO):
            if bairro_mem and obs == bairro_mem:
                out.at[i, "bairro"] = obs
                out.at[i, "observacoes"] = ""
                mudou = True
    if "bairro" in out.columns and "rua" in cols and "rua" not in COL_ENDERECO:
        pass
    # Visitas antigas: só coluna "bairro" no meio da planilha
    if "bairro" in df.columns and "rua" not in df.columns:
        for i in out.index:
            b = str(df.at[i, "bairro"]).strip()
            if b and not str(out.at[i, "bairro"]).strip():
                out.at[i, "bairro"] = b
                mudou = True
    return out.reindex(columns=cols), mudou


def _criar_workbook_inicial() -> None:
    try:
        from .inicializar_excel import criar_workbook_inicial
    except ImportError:
        try:
            from utils.inicializar_excel import criar_workbook_inicial
        except ImportError:
            import sys

            utils_dir = Path(__file__).resolve().parent
            if str(utils_dir) not in sys.path:
                sys.path.insert(0, str(utils_dir))
            from inicializar_excel import criar_workbook_inicial  # noqa: E402

    criar_workbook_inicial()


def _path_e_xlsx_valido(path: Path) -> bool:
    if not path.is_file() or path.stat().st_size < 128:
        return False
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            if not any(n.startswith("xl/") for n in names):
                return False
        pd.read_excel(path, sheet_name=0, engine="openpyxl", nrows=1)
        return True
    except Exception:
        return False


def _ultimo_backup_valido() -> Path | None:
    if not BACKUPS_DIR.is_dir():
        return None
    candidatos = sorted(BACKUPS_DIR.glob("apostolado_*.xlsx"), reverse=True)
    for path in candidatos:
        if "corrupto" in path.name.lower():
            continue
        if _path_e_xlsx_valido(path):
            return path
    return None


def _recuperar_excel_corrompido(erro: Exception | None = None) -> dict[str, pd.DataFrame]:
    """Restaura backup ou recria workbook quando o .xlsx está ilegível."""
    global ULTIMA_RECUPERACAO

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if EXCEL_PATH.exists():
        dest = BACKUPS_DIR / f"corrupto_{stamp}.xlsx"
        try:
            shutil.move(str(EXCEL_PATH), str(dest))
        except Exception:
            shutil.copy2(EXCEL_PATH, dest)
            EXCEL_PATH.unlink(missing_ok=True)

    backup = _ultimo_backup_valido()
    if backup:
        shutil.copy2(backup, EXCEL_PATH)
        ULTIMA_RECUPERACAO = (
            f"O arquivo Excel estava danificado e foi restaurado do backup "
            f"({backup.name}). Confira os dados e baixe uma cópia em Configurações."
        )
    else:
        _criar_workbook_inicial()
        ULTIMA_RECUPERACAO = (
            "O arquivo Excel estava danificado. Foi criado um arquivo novo. "
            "Se tiver cópia no computador, envie em Configurações → Enviar Excel."
        )

    if erro:
        ULTIMA_RECUPERACAO += f" (detalhe técnico: {type(erro).__name__})"

    return pd.read_excel(EXCEL_PATH, sheet_name=None, engine="openpyxl")


def _ler_todas_abas() -> dict[str, pd.DataFrame]:
    global _recuperando_excel
    try:
        return pd.read_excel(EXCEL_PATH, sheet_name=None, engine="openpyxl")
    except Exception as e:
        if _recuperando_excel:
            raise
        _recuperando_excel = True
        try:
            return _recuperar_excel_corrompido(e)
        finally:
            _recuperando_excel = False


def _escrever_todas_abas(todas: dict[str, pd.DataFrame]) -> None:
    """Grava em arquivo temporário e substitui — evita .xlsx corrompido pela metade."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    tmp = EXCEL_PATH.with_name(f"{EXCEL_PATH.stem}._tmp.xlsx")
    try:
        with pd.ExcelWriter(tmp, engine="openpyxl") as writer:
            for nome, sdf in todas.items():
                sdf.to_excel(writer, sheet_name=str(nome)[:31], index=False)
        tmp.replace(EXCEL_PATH)
    except Exception:
        if tmp.exists():
            tmp.unlink(missing_ok=True)
        raise


def mostrar_aviso_recuperacao_excel() -> None:
    """Exibe aviso uma vez por sessão se o Excel foi recuperado automaticamente."""
    global ULTIMA_RECUPERACAO
    if not ULTIMA_RECUPERACAO:
        return
    try:
        import streamlit as st
    except ImportError:
        return
    if st.session_state.get("_aviso_recuperacao_excel") == ULTIMA_RECUPERACAO:
        return
    st.warning(ULTIMA_RECUPERACAO)
    st.session_state["_aviso_recuperacao_excel"] = ULTIMA_RECUPERACAO


def _migrar_excel() -> None:
    """Adiciona abas e colunas novas sem apagar dados existentes."""
    todas = _ler_todas_abas()
    mudou = False

    novas_abas = {
        _ta.SHEET_DIRETORIA: (
            _ta.COL_DIRETORIA,
            pd.DataFrame(
                [dict(zip(_ta.COL_DIRETORIA, t)) for t in _ta.DIRETORIA_SEED],
                columns=_ta.COL_DIRETORIA,
            ),
        ),
        _ta.SHEET_ZELADORES: (_ta.COL_ZELADORES, pd.DataFrame(columns=_ta.COL_ZELADORES)),
        _ta.SHEET_INTENCOES_PAPA: (
            _ta.COL_INTENCOES_PAPA,
            pd.DataFrame(
                [dict(zip(_ta.COL_INTENCOES_PAPA, t)) for t in _ta.INTENCOES_PAPA_SEED],
                columns=_ta.COL_INTENCOES_PAPA,
            ),
        ),
        _ta.SHEET_CENTROS: (
            _ta.COL_CENTROS,
            pd.DataFrame(
                [dict(zip(_ta.COL_CENTROS, t)) for t in _ta.CENTROS_SEED],
                columns=_ta.COL_CENTROS,
            ),
        ),
        _ta.SHEET_COMUNICACOES: (
            _ta.COL_COMUNICACOES,
            pd.DataFrame(columns=_ta.COL_COMUNICACOES),
        ),
        _ta.SHEET_REUNIOES: (_ta.COL_REUNIOES, pd.DataFrame(columns=_ta.COL_REUNIOES)),
        _ta.SHEET_SUGESTOES: (_ta.COL_SUGESTOES, pd.DataFrame(columns=_ta.COL_SUGESTOES)),
        _ta.SHEET_REUNIOES_IA: (_ta.COL_REUNIOES_IA, pd.DataFrame(columns=_ta.COL_REUNIOES_IA)),
    }
    for nome, (cols, vazio) in novas_abas.items():
        if nome not in todas:
            todas[nome] = vazio
            mudou = True

    if SHEET_MEMBROS in todas:
        df, m2 = _migrar_membros_endereco(todas[SHEET_MEMBROS])
        todas[SHEET_MEMBROS] = df
        mudou = mudou or m2

    mapa = {}
    if SHEET_MEMBROS in todas:
        try:
            from .endereco import linha_entrega_visita_de_membro
        except ImportError:
            from endereco import linha_entrega_visita_de_membro
        for _, r in todas[SHEET_MEMBROS].iterrows():
            mid = int(pd.to_numeric(r.get("id"), errors="coerce") or 0)
            if mid:
                mapa[mid] = linha_entrega_visita_de_membro(r.to_dict())

    if SHEET_ENTREGAS in todas:
        df, m2 = _migrar_planilha_endereco(todas[SHEET_ENTREGAS], COL_ENTREGAS, mapa)
        todas[SHEET_ENTREGAS] = df
        mudou = mudou or m2

    if SHEET_INTENCOES in todas:
        df = todas[SHEET_INTENCOES].copy()
        if "categoria" not in df.columns:
            df["categoria"] = "Pedido"
            mudou = True
        if "prioridade" not in df.columns:
            df["prioridade"] = "Normal"
            mudou = True
        for c in COL_INTENCOES:
            if c not in df.columns:
                df[c] = ""
                mudou = True
        todas[SHEET_INTENCOES] = df.reindex(columns=COL_INTENCOES)

    if SHEET_VISITAS in todas:
        df, m2 = _migrar_planilha_endereco(todas[SHEET_VISITAS], COL_VISITAS, mapa)
        todas[SHEET_VISITAS] = df
        mudou = mudou or m2

    if mudou:
        _backup_antes_de_escrever()
        _escrever_todas_abas(todas)


def _ensure_excel() -> None:
    if not EXCEL_PATH.exists():
        _criar_workbook_inicial()
        return
    if not _path_e_xlsx_valido(EXCEL_PATH):
        global _recuperando_excel
        if not _recuperando_excel:
            _recuperando_excel = True
            try:
                _recuperar_excel_corrompido(ValueError("arquivo Excel inválido"))
            finally:
                _recuperando_excel = False
    _migrar_excel()


def _backup_antes_de_escrever() -> Path | None:
    if not EXCEL_PATH.exists():
        return None
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = BACKUPS_DIR / f"apostolado_{stamp}.xlsx"
    shutil.copy2(EXCEL_PATH, dest)
    return dest


def _as_date(v: Any) -> date | None:
    if v is None or v == "" or pd.isna(v):
        return None
    if isinstance(v, date) and not isinstance(v, datetime):
        return v
    if isinstance(v, datetime):
        return v.date()
    try:
        ts = pd.to_datetime(v, errors="coerce")
        if pd.isna(ts):
            return None
        return ts.date()
    except Exception:
        return None


def _ler_aba(sheet: str) -> pd.DataFrame:
    _ensure_excel()
    return pd.read_excel(EXCEL_PATH, sheet_name=sheet, engine="openpyxl")


def _salvar_aba(sheet: str, df: pd.DataFrame, cols: list[str]) -> None:
    _ensure_excel()
    _backup_antes_de_escrever()
    out = df.reindex(columns=cols).copy()
    todas = _ler_todas_abas()
    todas[sheet] = out
    _escrever_todas_abas(todas)


def _membro_dict(row: pd.Series) -> dict[str, Any]:
    try:
        from .endereco import endereco_completo_de_registro
    except ImportError:
        from endereco import endereco_completo_de_registro

    d = {c: row.get(c, "") for c in COL_MEMBROS}
    d["id"] = int(row.get("id", 0) or 0)
    d["nasc"] = _as_date(row.get("nasc"))
    d["ingresso"] = _as_date(row.get("ingresso"))
    d["data_inscricao"] = _as_date(row.get("data_inscricao"))
    d["endereco_completo"] = endereco_completo_de_registro(d)
    return d


def ler_membros_df() -> pd.DataFrame:
    return _ler_generico(SHEET_MEMBROS, COL_MEMBROS)


def salvar_membros_df(df: pd.DataFrame) -> None:
    _salvar_generico(
        SHEET_MEMBROS,
        df,
        COL_MEMBROS,
        id_col="id",
        colunas_data=["nasc", "ingresso", "data_inscricao"],
    )


def _normalizar_datas_df(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for c in cols:
        if c not in out.columns:
            continue
        out[c] = pd.to_datetime(out[c], errors="coerce")
    return out


COLUNAS_INTEIRAS = frozenset(
    {
        "id",
        "membro_id",
        "_rid",
        "num_orig",
        "pagina",
        "duracao_min",
        "mes",
        "ano",
        "ata_num",
    }
)


def _celula_str(v: Any) -> str:
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    s = str(v).strip()
    return "" if s.lower() in ("nan", "none", "nat") else s


def _eh_tipo_coluna(cfg: Any, nome: str) -> bool:
    return type(cfg).__name__ == nome


def preparar_data_editor(
    df: pd.DataFrame,
    cols: list[str],
    *,
    colunas_data: list[str] | None = None,
    id_col: str | None = "id",
    column_config: dict[str, Any] | None = None,
) -> tuple[pd.DataFrame, dict[str, Any]]:
    """Tipos e opções compatíveis com st.data_editor (evita erro em quase todas as telas)."""
    import streamlit as st

    cfg_out = dict(column_config or {})
    if df.empty:
        return pd.DataFrame(columns=cols), cfg_out

    out = df.reindex(columns=cols).copy()
    colunas_data = list(colunas_data or [])

    for c, col_cfg in cfg_out.items():
        if c in cols and _eh_tipo_coluna(col_cfg, "DateColumn") and c not in colunas_data:
            colunas_data.append(c)

    ints = set(COLUNAS_INTEIRAS) & set(cols)
    if id_col and id_col in cols:
        ints.add(id_col)

    for c in cols:
        col_cfg = cfg_out.get(c)
        if col_cfg and _eh_tipo_coluna(col_cfg, "NumberColumn"):
            nums = pd.to_numeric(out[c], errors="coerce").fillna(0)
            out[c] = nums.astype(int)
            ints.add(c)
            continue
        if c in ints:
            nums = pd.to_numeric(out[c], errors="coerce").fillna(0)
            out[c] = nums.astype(int)

    for c in colunas_data:
        if c in out.columns:
            out[c] = pd.to_datetime(out[c], errors="coerce")

    for c in cols:
        col_cfg = cfg_out.get(c)
        if col_cfg and _eh_tipo_coluna(col_cfg, "SelectboxColumn"):
            opts = [str(o) for o in (getattr(col_cfg, "options", None) or [])]
            for v in out[c].tolist():
                s = _celula_str(v)
                if s and s not in opts:
                    opts.append(s)
            if not opts:
                opts = [""]

            def _norm_select(val: Any) -> str:
                s = _celula_str(val)
                if s in opts:
                    return s
                for o in opts:
                    if o.lower() == s.lower():
                        return o
                return opts[0]

            out[c] = out[c].apply(_norm_select)
            label = getattr(col_cfg, "label", None) or c.replace("_", " ").title()
            cfg_out[c] = st.column_config.SelectboxColumn(label, options=opts)
            continue

        if c in ints or c in colunas_data:
            continue

        out[c] = out[c].apply(_celula_str)

    return out, cfg_out


def ler_membros() -> list[dict[str, Any]]:
    df = ler_membros_df()
    if df.empty:
        return []
    return [_membro_dict(r) for _, r in df.iterrows()]


def salvar_membros(membros: list[dict[str, Any]] | list[tuple]) -> None:
    rows = []
    for m in membros:
        if isinstance(m, dict):
            rows.append({c: m.get(c, "") for c in COL_MEMBROS})
        elif len(m) >= len(COL_MEMBROS):
            rows.append(dict(zip(COL_MEMBROS, m[: len(COL_MEMBROS)])))
        else:
            try:
                from .endereco import separar_endereco_legacy
            except ImportError:
                from endereco import separar_endereco_legacy
            addr = separar_endereco_legacy(str(m[6]), str(m[7]))
            rows.append(
                {
                    "id": m[0],
                    "num_orig": m[1],
                    "nome": m[2],
                    "sexo": m[3],
                    "nasc": m[4],
                    "ingresso": m[5],
                    "rua": addr["rua"],
                    "numero": addr["numero"],
                    "bairro": addr["bairro"],
                    "cep": addr["cep"],
                    "cidade": addr["cidade"],
                    "telefone": m[8],
                    "funcao": m[9],
                    "situacao": m[10],
                    "consagrada": m[11],
                    "observacoes": m[12],
                    "pagina": m[13],
                    "tipo_membro": "Associado",
                    "comunidade": "",
                    "data_inscricao": m[5],
                    "fita_consagracao": "Não",
                }
            )
    salvar_membros_df(pd.DataFrame(rows, columns=COL_MEMBROS))


def ler_inconsistencias() -> list[tuple]:
    df = _ler_aba(SHEET_INCONSISTENCIAS)
    if df.empty:
        return []
    return [tuple(r[c] for c in COL_INCONSISTENCIAS) for _, r in df.iterrows()]


def salvar_inconsistencias(items: list[tuple]) -> None:
    df = pd.DataFrame(
        [dict(zip(COL_INCONSISTENCIAS, t)) for t in items], columns=COL_INCONSISTENCIAS
    )
    salvar_inconsistencias_df(df)


def ler_inconsistencias_df() -> pd.DataFrame:
    return _ler_generico(SHEET_INCONSISTENCIAS, COL_INCONSISTENCIAS)


def salvar_inconsistencias_df(df: pd.DataFrame) -> None:
    _salvar_generico(SHEET_INCONSISTENCIAS, df, COL_INCONSISTENCIAS)


def _ler_generico(sheet: str, cols: list[str]) -> pd.DataFrame:
    df = _ler_aba(sheet)
    if df.empty:
        return pd.DataFrame(columns=cols)
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return df[cols]


def _remover_linhas_vazias(
    df: pd.DataFrame, cols: list[str], id_col: str | None = None
) -> pd.DataFrame:
    if df.empty:
        return df

    def tem_conteudo(row: pd.Series) -> bool:
        for c in cols:
            if c == id_col:
                continue
            v = row.get(c)
            if v is None or (isinstance(v, float) and pd.isna(v)):
                continue
            if str(v).strip():
                return True
        return False

    mask = df.apply(tem_conteudo, axis=1)
    return df[mask].reset_index(drop=True)


def preparar_dataframe(
    df: pd.DataFrame,
    cols: list[str],
    *,
    id_col: str | None = None,
    colunas_data: list[str] | None = None,
) -> pd.DataFrame:
    """Normaliza tipos e remove linhas vazias antes de gravar no Excel."""
    out = df.reindex(columns=cols).copy()
    out = _remover_linhas_vazias(out, cols, id_col=id_col)
    if colunas_data:
        out = _normalizar_datas_df(out, colunas_data)
    if id_col and id_col in out.columns:
        nums = pd.to_numeric(out[id_col], errors="coerce")
        out[id_col] = nums.astype("Int64")
    return out


def _salvar_generico(
    sheet: str,
    df: pd.DataFrame,
    cols: list[str],
    *,
    id_col: str | None = None,
    colunas_data: list[str] | None = None,
) -> None:
    df = preparar_dataframe(df, cols, id_col=id_col, colunas_data=colunas_data)
    _salvar_aba(sheet, df, cols)


def preparar_entregas_editor(df: pd.DataFrame) -> pd.DataFrame:
    """Tipos compatíveis com st.data_editor (DateColumn, SelectboxColumn)."""
    try:
        from .dados_membros import ITENS_ENTREGA
    except ImportError:
        try:
            from utils.dados_membros import ITENS_ENTREGA
        except ImportError:
            from dados_membros import ITENS_ENTREGA

    if df.empty:
        return pd.DataFrame(columns=COL_ENTREGAS)
    out = df.reindex(columns=COL_ENTREGAS).copy()
    out["id"] = pd.to_numeric(out["id"], errors="coerce").fillna(0).astype(int)
    out["membro_id"] = pd.to_numeric(out["membro_id"], errors="coerce").fillna(0).astype(int)
    out["membro_nome"] = out["membro_nome"].fillna("").astype(str)
    for c in COL_ENDERECO:
        out[c] = out[c].fillna("").astype(str)
    out["data_entrega"] = pd.to_datetime(out["data_entrega"], errors="coerce")
    out["item"] = out["item"].fillna("").astype(str).str.strip()
    invalid_item = ~out["item"].isin(ITENS_ENTREGA) | (out["item"] == "")
    out.loc[invalid_item, "item"] = ITENS_ENTREGA[0]
    ent = out["entregue"].fillna("N").astype(str).str.strip().str.upper()
    out["entregue"] = ent.where(ent.isin(["S", "N"]), "N")
    out["observacoes"] = out["observacoes"].fillna("").astype(str)
    return out


def ler_entregas() -> pd.DataFrame:
    return preparar_entregas_editor(_ler_generico(SHEET_ENTREGAS, COL_ENTREGAS))


def salvar_entregas(df: pd.DataFrame) -> None:
    _salvar_generico(
        SHEET_ENTREGAS,
        df,
        COL_ENTREGAS,
        id_col="id",
        colunas_data=["data_entrega"],
    )


def ler_visitas() -> pd.DataFrame:
    return _ler_generico(SHEET_VISITAS, COL_VISITAS)


def salvar_visitas(df: pd.DataFrame) -> None:
    _salvar_generico(
        SHEET_VISITAS,
        df,
        COL_VISITAS,
        id_col="id",
        colunas_data=["data_visita"],
    )


def _ler_aba_generica(sheet: str, cols: list[str]) -> pd.DataFrame:
    return _ler_generico(sheet, cols)


def _salvar_aba_generica(
    sheet: str, df: pd.DataFrame, cols: list[str], **kwargs
) -> None:
    _salvar_generico(sheet, df, cols, **kwargs)


def ler_diretoria() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_DIRETORIA, _ta.COL_DIRETORIA)


def salvar_diretoria(df: pd.DataFrame) -> None:
    _salvar_aba_generica(
        _ta.SHEET_DIRETORIA,
        df,
        _ta.COL_DIRETORIA,
        id_col="id",
        colunas_data=["mandato_inicio"],
    )


def ler_zeladores() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_ZELADORES, _ta.COL_ZELADORES)


def salvar_zeladores(df: pd.DataFrame) -> None:
    _salvar_aba_generica(
        _ta.SHEET_ZELADORES,
        df,
        _ta.COL_ZELADORES,
        id_col="id",
        colunas_data=["data_posse"],
    )


def ler_intencoes_papa() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_INTENCOES_PAPA, _ta.COL_INTENCOES_PAPA)


def salvar_intencoes_papa(df: pd.DataFrame) -> None:
    _salvar_aba_generica(_ta.SHEET_INTENCOES_PAPA, df, _ta.COL_INTENCOES_PAPA, id_col="id")


def ler_centros() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_CENTROS, _ta.COL_CENTROS)


def salvar_centros(df: pd.DataFrame) -> None:
    _salvar_aba_generica(_ta.SHEET_CENTROS, df, _ta.COL_CENTROS, id_col="id")


def ler_comunicacoes() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_COMUNICACOES, _ta.COL_COMUNICACOES)


def salvar_comunicacoes(df: pd.DataFrame) -> None:
    _salvar_aba_generica(
        _ta.SHEET_COMUNICACOES,
        df,
        _ta.COL_COMUNICACOES,
        id_col="id",
        colunas_data=["data"],
    )


def ler_reunioes() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_REUNIOES, _ta.COL_REUNIOES)


def salvar_reunioes(df: pd.DataFrame) -> None:
    _salvar_aba_generica(
        _ta.SHEET_REUNIOES,
        df,
        _ta.COL_REUNIOES,
        id_col="id",
        colunas_data=["data"],
    )


def ler_sugestoes() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_SUGESTOES, _ta.COL_SUGESTOES)


def salvar_sugestoes(df: pd.DataFrame) -> None:
    _salvar_aba_generica(
        _ta.SHEET_SUGESTOES,
        df,
        _ta.COL_SUGESTOES,
        id_col="id",
        colunas_data=["data"],
    )


def ler_reunioes_ia() -> pd.DataFrame:
    return _ler_aba_generica(_ta.SHEET_REUNIOES_IA, _ta.COL_REUNIOES_IA)


def salvar_reunioes_ia(df: pd.DataFrame) -> None:
    _salvar_aba_generica(
        _ta.SHEET_REUNIOES_IA,
        df,
        _ta.COL_REUNIOES_IA,
        id_col="id",
        colunas_data=["data"],
    )


def contar_zeladores_ativos() -> int:
    z = ler_zeladores()
    if z.empty:
        return 0
    return len(z[z["ativo"].astype(str).str.lower().isin(("sim", "s"))])


def listar_comunidades() -> list[str]:
    vistos: set[str] = set()
    ordem: list[str] = []

    def add_many(vals: list[str]) -> None:
        for c in vals:
            t = str(c).strip()
            if t and t not in vistos:
                vistos.add(t)
                ordem.append(t)

    cfg = ler_config()
    raw = cfg.get("comunidades", "")
    add_many([x.strip() for x in raw.replace("·", "|").split("|") if x.strip()])
    add_many(["Matriz", "Paróquia São Jorge"])

    try:
        dfm = ler_membros_df()
        if not dfm.empty and "comunidade" in dfm.columns:
            add_many(dfm["comunidade"].dropna().astype(str).tolist())
    except Exception:
        pass

    try:
        dfc = ler_centros()
        if not dfc.empty and "comunidade" in dfc.columns:
            add_many(dfc["comunidade"].dropna().astype(str).tolist())
    except Exception:
        pass

    return ordem or ["Matriz"]


def ler_consagracoes() -> pd.DataFrame:
    return _ler_generico(SHEET_CONSAGRACOES, COL_CONSAGRACOES)


def salvar_consagracoes(df: pd.DataFrame) -> None:
    _salvar_generico(
        SHEET_CONSAGRACOES,
        df,
        COL_CONSAGRACOES,
        id_col="id",
        colunas_data=["data_consagracao"],
    )


def ler_intencoes() -> pd.DataFrame:
    return _ler_generico(SHEET_INTENCOES, COL_INTENCOES)


def salvar_intencoes(df: pd.DataFrame) -> None:
    _salvar_generico(
        SHEET_INTENCOES,
        df,
        COL_INTENCOES,
        id_col="id",
        colunas_data=["data"],
    )


def ler_agenda() -> pd.DataFrame:
    return _ler_generico(SHEET_AGENDA, COL_AGENDA)


def salvar_agenda(df: pd.DataFrame) -> None:
    _salvar_generico(
        SHEET_AGENDA,
        df,
        COL_AGENDA,
        id_col="id",
        colunas_data=["data"],
    )


def _import_config_padrao():
    try:
        from .dados_membros import CONFIG_PADRAO
    except ImportError:
        try:
            from utils.dados_membros import CONFIG_PADRAO
        except ImportError:
            from dados_membros import CONFIG_PADRAO
    return CONFIG_PADRAO


def ler_config() -> dict[str, str]:
    df = _ler_aba(SHEET_CONFIG)
    if df.empty:
        return dict(_import_config_padrao())
    return {str(r["chave"]): str(r["valor"]) for _, r in df.iterrows()}


def salvar_config(cfg: dict[str, str]) -> None:
    df = pd.DataFrame(
        [{"chave": k, "valor": v} for k, v in cfg.items()], columns=COL_CONFIG
    )
    _salvar_aba(SHEET_CONFIG, df, COL_CONFIG)


def ler_config_df() -> pd.DataFrame:
    df = _ler_generico(SHEET_CONFIG, COL_CONFIG)
    if df.empty:
        cfg = _import_config_padrao()
        return pd.DataFrame(
            [{"chave": k, "valor": str(v)} for k, v in cfg.items()],
            columns=COL_CONFIG,
        )
    return df


def salvar_config_df(df: pd.DataFrame) -> None:
    _salvar_generico(SHEET_CONFIG, df, COL_CONFIG)


def ler_memorial() -> pd.DataFrame:
    return _ler_generico(SHEET_MEMORIAL, COL_MEMORIAL)


def salvar_memorial(df: pd.DataFrame) -> None:
    _salvar_generico(
        SHEET_MEMORIAL,
        df,
        COL_MEMORIAL,
        colunas_data=["nasc", "falecimento"],
    )


def _idade_anos(nasc: date | None) -> int | None:
    if not nasc:
        return None
    hoje = date.today()
    anos = hoje.year - nasc.year
    if (hoje.month, hoje.day) < (nasc.month, nasc.day):
        anos -= 1
    return anos


def aniversariantes_proximos(dias: int = 30) -> list[dict[str, Any]]:
    hoje = date.today()
    limite = hoje + timedelta(days=dias)
    resultado = []
    for m in ler_membros():
        nasc = _as_date(m.get("nasc"))
        sit = m.get("situacao", "")
        if not nasc or sit == "Falecida":
            continue
        try:
            prox = date(hoje.year, nasc.month, nasc.day)
        except ValueError:
            continue
        if prox < hoje:
            prox = date(hoje.year + 1, nasc.month, nasc.day)
        if hoje <= prox <= limite:
            resultado.append(
                {
                    "id": m["id"],
                    "num_orig": m.get("num_orig", ""),
                    "nome": m.get("nome", ""),
                    "nasc": nasc,
                    "telefone": m.get("telefone", ""),
                    "situacao": sit,
                    "proximo": prox,
                    "dias": (prox - hoje).days,
                    "idade": _idade_anos(nasc),
                }
            )
    resultado.sort(key=lambda x: x["proximo"])
    return resultado


def inconsistencias_criticas_abertas() -> list[tuple]:
    abertas = []
    for inc in ler_inconsistencias():
        prio = str(inc[1])
        resolvida = str(inc[4]).strip().lower()
        if "crítica" in prio.lower() or "🔴" in prio:
            if resolvida not in ("sim", "s"):
                abertas.append(inc)
    return abertas


def total_por_situacao() -> dict[str, int]:
    totais: dict[str, int] = {}
    for m in ler_membros():
        sit = m.get("situacao") or "Sem situação"
        totais[sit] = totais.get(sit, 0) + 1
    return totais


def membros_sem_telefone() -> list[dict[str, Any]]:
    return [m for m in ler_membros() if not str(m.get("telefone", "")).strip()]


def membros_sem_endereco() -> list[dict[str, Any]]:
    return [m for m in ler_membros() if not str(m.get("rua", "")).strip()]
