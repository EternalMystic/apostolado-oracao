"""Instruções de uso do sistema."""
import sys
from pathlib import Path

import streamlit as st

from utils.auth import require_login
from utils.ui import inject_css

sys.path.insert(0, str(Path(__file__).parent.parent))

st.set_page_config(page_title="Instruções", page_icon="📝", layout="wide")
require_login()
inject_css()
st.title("📝 Instruções de Uso")

st.markdown(
    """
### Como usar este sistema
**Paróquia São Jorge · Apostolado da Oração · Nova Odessa – SP**

1. **Consultar um membro** – Use *Consulta Rápida* ou *Membros* (Ctrl+F no navegador).
2. **Adicionar membro** – Aba *Membros*, última linha, preencha e salve.
3. **Planejar visita** – *Rota de Visitas* por bairro; marque **S** após cada entrega.
4. **Aniversários** – *Aniversários* mostra os próximos 7–90 dias; ligue no dia.
5. **Inconsistências** – *Inconsistências*; marque **Sim** quando resolver.
6. **Backup** – Automático antes de salvar; use `BACKUP_AGORA.bat` para cópia manual.
7. **Iniciar** – Duplo clique em `INICIAR.bat` (abre no navegador).

### Arquivos importantes
| Arquivo | Função |
|---------|--------|
| `data/apostolado.xlsx` | Banco de dados principal |
| `backups/` | Cópias automáticas datadas |
| `exports/` | CSV exportados |
| `relatorios/` | PDFs do R |

### Atalhos úteis
- **WhatsApp**: botão na Consulta Rápida (se telefone válido).
- **Relatório mensal PDF**: `r_scripts/relatorio_mensal.R`.
- **Otimizar rota**: `rust_utils/route_optimizer` (opcional).

> *"A ordem no trabalho ordinário é forma excelente de amar a Deus."*  
> — São Josemaría Escrivá

**Dúvidas?** Procure o coordenador ou a coordenadora do Apostolado.
"""
)
