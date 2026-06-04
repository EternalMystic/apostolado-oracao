# Deploy gratuito – acesso de qualquer lugar

O Apostolado pode rodar **de graça** na nuvem com HTTPS (celular, tablet, PC, qualquer país).

## Opção recomendada: Streamlit Community Cloud

1. Crie conta em https://share.streamlit.io (login com GitHub).
2. Este repositório deve estar no GitHub (público ou privado).
3. Clique **New app** e preencha:
   - **Repository:** seu-usuario/apostolado-oracao
   - **Branch:** main
   - **Main file path:** `app/app.py`
4. Em **Advanced settings**:
   - **Python version:** 3.11
5. Em **Secrets** (Settings do app), cole:

```toml
APP_PASSWORD = "senha-que-o-coordenador-escolher"
```

6. Deploy. URL final: `https://SEU-APP.streamlit.app`

Compartilhe esse link no WhatsApp do Apostolado.

### Dados na nuvem

- Alterações ficam no servidor enquanto o app estiver ativo.
- **Semanalmente:** Configurações → Baixar apostolado.xlsx (backup).
- Para restaurar: Configurações → Enviar arquivo .xlsx.

## Alternativa: Hugging Face Spaces (também grátis)

1. Conta em https://huggingface.co
2. New Space → SDK **Streamlit**
3. Envie os arquivos desta pasta `apostolado_oracao/`
4. `README.md` do Space:

```yaml
---
title: Apostolado da Oração
emoji: ✝️
colorFrom: purple
colorTo: purple
sdk: streamlit
app_file: app/app.py
pinned: false
---
```

5. Secrets: `APP_PASSWORD` na aba Settings do Space.

## Uso local (paróquia)

`INICIAR.bat` — só funciona no computador da igreja.

## Segurança

- Sempre defina `APP_PASSWORD` na nuvem.
- Não publique a senha na internet; envie só aos coordenadores.
