"""Títulos em português para cabeçalhos das tabelas (Streamlit data_editor)."""
from __future__ import annotations

from typing import Any

import streamlit as st

TITULOS: dict[str, str] = {
    "id": "ID",
    "num_orig": "Nº livro",
    "nome": "Nome",
    "sexo": "Sexo",
    "nasc": "Nascimento",
    "ingresso": "Ingresso AO",
    "endereco": "Rua / logradouro",
    "rua": "Rua / logradouro",
    "numero": "Número",
    "bairro": "Bairro",
    "cep": "CEP",
    "cidade": "Cidade",
    "telefone": "Telefone",
    "funcao": "Função pastoral",
    "situacao": "Situação",
    "consagrada": "Consagrada",
    "observacoes": "Observações",
    "observacao": "Observação",
    "pagina": "Página livro",
    "tipo_membro": "Tipo de membro",
    "comunidade": "Comunidade",
    "data_inscricao": "Inscrição AO",
    "fita_consagracao": "Fita vermelha",
    "membro_id": "ID membro",
    "membro_nome": "Nome do membro",
    "item": "Material / motivo",
    "data_entrega": "Data da entrega",
    "entregue": "Entregue?",
    "data_visita": "Data da visita",
    "realizada": "Realizada?",
    "tipo_visita": "Tipo de visita",
    "nota_pastoral": "Nota pastoral",
    "data_consagracao": "Data consagração",
    "local": "Local",
    "data": "Data",
    "categoria": "Categoria",
    "intencao": "Intenção de oração",
    "solicitante": "Solicitante",
    "status": "Status",
    "prioridade": "Prioridade",
    "hora": "Hora",
    "titulo": "Título",
    "tipo": "Tipo",
    "responsavel": "Responsável",
    "chave": "Chave",
    "valor": "Valor",
    "falecimento": "Falecimento",
    "categoria_inc": "Categoria",
    "descricao": "Descrição",
    "acao_sugerida": "Ação sugerida",
    "resolvida": "Resolvida",
    "cargo": "Cargo",
    "email": "E-mail",
    "mandato_inicio": "Início do mandato",
    "ativo": "Ativo?",
    "data_posse": "Data de posse",
    "mes": "Mês",
    "ano": "Ano",
    "texto": "Texto",
    "divulgada": "Divulgada?",
    "mensagem": "Mensagem",
    "publico": "Público-alvo",
    "registrado_por": "Registrado por",
    "presentes": "Presentes",
    "deliberacoes": "Deliberações",
    "ata_num": "Nº da ata",
    "autor": "Autor",
    "resposta": "Resposta",
    "arquivo_audio": "Arquivo de áudio",
    "transcricao_arquivo": "Arquivo transcrição",
    "duracao_min": "Duração (min)",
    "resumo": "Resumo IA",
    "explicacao": "Explicação IA",
    "pontos_chave": "Pontos-chave",
}


def titulo(coluna: str) -> str:
    return TITULOS.get(coluna, coluna.replace("_", " ").title())


def coluna_texto(coluna: str, **kwargs: Any) -> Any:
    return st.column_config.TextColumn(titulo(coluna), **kwargs)


_COLUNAS_NUMERO = frozenset(
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


def montar_column_config(
    colunas: list[str],
    extra: dict[str, Any] | None = None,
    *,
    ocultar: set[str] | None = None,
) -> dict[str, Any]:
    """Garante título em português para cada coluna; `extra` sobrescreve."""
    cfg: dict[str, Any] = {}
    ocultar = ocultar or set()
    for c in colunas:
        if c in ocultar:
            continue
        if extra and c in extra:
            cfg[c] = extra[c]
        elif c in _COLUNAS_NUMERO:
            cfg[c] = st.column_config.NumberColumn(titulo(c), format="%d", min_value=0)
        else:
            cfg[c] = coluna_texto(c)
    if extra:
        for c, v in extra.items():
            if c not in cfg:
                cfg[c] = v
    return cfg
