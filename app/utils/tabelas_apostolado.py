"""Tabelas e conteúdos do Apostolado da Oração (MEJ / práticas paroquiais)."""
from __future__ import annotations

from datetime import date

# Oferecimento diário (Rede Mundial de Oração do Papa)
OFERECIMENTO_DIARIO = """
**Oferecimento ao Sagrado Coração de Jesus** (rezar diariamente)

*Ó Jesus, manso e humilde de coração, ouvi-me. Dentro dos meus males escondidos,*
*dentro das minhas inquietações, dentro dos meus limites, dentro da minha fragilidade,*
*na minha aflição e no meu cansaço: ouvi-me.*

*Ó Jesus, manso e humilde de coração, ouvi-me. Dentro das minhas necessidades,*
*dentro dos meus esforços, dentro das minhas lutas, dentro dos meus desejos de bem,*
*na minha solidão e na minha angústia: ouvi-me.*

*Ó Jesus, manso e humilde de coração, ouvi-me. Dentro dos meus projetos,*
*dentro dos meus trabalhos, dentro dos meus sonhos, dentro dos meus anseios,*
*na minha tristeza e na minha dor: ouvi-me.*

*Ó Jesus, manso e humilde de coração, ouvi-me. E, se me for possível, alivia o meu sofrimento;*
*se não, dá-me resignação. Concede-me uma fé viva, uma esperança firme e um amor ardente a Ti.*
*Faze com que eu repita sempre: Jesus, eu confio em Vós!*
"""

COL_DIRETORIA = [
    "id", "cargo", "nome", "telefone", "email", "mandato_inicio", "ativo", "observacoes",
]
COL_ZELADORES = [
    "id", "membro_id", "membro_nome", "comunidade", "data_posse", "ativo", "observacoes",
]
COL_INTENCOES_PAPA = [
    "id", "mes", "ano", "titulo", "texto", "divulgada", "observacoes",
]
COL_CENTROS = [
    "id", "nome", "comunidade", "local", "responsavel", "telefone", "ativo", "observacoes",
]
COL_COMUNICACOES = [
    "id", "data", "tipo", "titulo", "mensagem", "publico", "registrado_por", "observacoes",
]
COL_REUNIOES = [
    "id", "data", "tipo", "titulo", "presentes", "deliberacoes", "ata_num", "observacoes",
]

SHEET_DIRETORIA = "Diretoria"
SHEET_ZELADORES = "Zeladores"
SHEET_INTENCOES_PAPA = "Intencoes_Papa"
SHEET_CENTROS = "Centros"
SHEET_COMUNICACOES = "Comunicacoes"
SHEET_REUNIOES = "Reunioes"

COL_MEMBROS_EXT = ["tipo_membro", "comunidade", "data_inscricao", "fita_consagracao"]
COL_INTENCOES_EXT = ["categoria", "prioridade"]
COL_VISITAS_EXT = ["tipo_visita", "nota_pastoral"]

_hoje = date.today()

DIRETORIA_SEED = [
    (1, "Presidente", "Luiz Antônio", "", "", _hoje.replace(year=_hoje.year - 1), "Sim", "Coordenador"),
    (2, "Coordenadora", "Luíza Regina", "", "", _hoje.replace(year=_hoje.year - 1), "Sim", "Coordenadora pastoral"),
    (3, "Secretário(a)", "", "", "", None, "Não", "A preencher"),
    (4, "Tesoureiro(a)", "", "", "", None, "Não", "A preencher"),
    (5, "Diretor Espiritual", "Pe. (paróquia)", "", "", None, "Sim", "Pároco ou indicado"),
]

INTENCOES_PAPA_SEED = [
    (
        1,
        _hoje.month,
        _hoje.year,
        f"Intenções de {_hoje.strftime('%B/%Y')}",
        "Pela paz no mundo, pelos doentes, pelas famílias da paróquia e pelo Papa.",
        "N",
        "Atualizar com o bilhete mensal / Mensageiro do Coração de Jesus",
    ),
]

CENTROS_SEED = [
    (1, "Centro Paróquia São Jorge", "Matriz", "Paróquia São Jorge", "Luiz Antônio", "", "Sim", "Centro principal"),
    (2, "Centro Santa Luzia", "Santa Luzia", "Comunidade Santa Luzia", "", "", "Sim", ""),
    (3, "Centro Santa Dulce", "Santa Dulce dos Pobres", "Comunidade Santa Dulce", "", "", "Sim", ""),
    (4, "Centro N. Sra. de Fátima", "N. Sra. de Fátima", "Comunidade N. Sra. de Fátima", "", "", "Sim", ""),
]
