"""Referência do sistema completo."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Instruções", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
require_login()
inject_css()
st.title("📝 Referência")

st.markdown(
    """
### Módulos do sistema (como nos apostolados e paróquias)

| Área | Página | Função |
|------|--------|--------|
| Cadastro | Membros | Associados, zeladores, comunidade, fita |
| Busca | Consulta Rápida | Achar membro no celular |
| Espiritualidade | Espiritualidade | Oferecimento + intenções do Papa |
| Orações | Orações | Rosário tomista, ladainhas, rezas |
| Pastoral | Rota / Visitas / Entregas | Visitas domiciliares e materiais |
| Oração | Mural de oração | Pedidos da comunidade |
| Organização | Diretoria / Centros / Atas | Estrutura do AO na paróquia |
| Agenda | Agenda | Reuniões, missas, formações |
| Comunicação | Comunicações | Registro + WhatsApp |
| Consagrações | Consagrações | Registro ao Sagrado Coração |
| Qualidade | Inconsistências | Corrigir cadastro |
| Memória | Memorial | Falecidos |
| Sugestões | Sugestões | Ideias e comentários sobre o app |
| Reunião + IA | Reunião IA | Áudio da reunião semanal → resumo (OpenAI/Claude) |
| Dados | Configurações / Relatórios | Backup e exportação |

**Salvar:** em cada tabela use **💾 Salvar**.

**Celular:** menu ☰ → **Adicionar à tela inicial**.

Coordenador(a) do Apostolado para senha.
"""
)
