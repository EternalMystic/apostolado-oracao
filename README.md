# Apostolado da Oração – Paróquia São Jorge

Sistema de gestão para o Apostolado da Oração (Nova Odessa – SP).

## Onde publicar? **Streamlit** (não Vercel)

Escolhemos **Streamlit Cloud** porque é o mais **fácil para 50+** (um link, letras grandes, sem instalar app) e o sistema **já está pronto**. Vercel exigiria reescrever tudo do zero.

[![Deploy no Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)

**Deploy em 3 minutos:**

1. Abra https://share.streamlit.io e entre com GitHub  
2. **New app** → repositório `EternalMystic/apostolado-oracao`  
3. **Main file:** `app/app.py`  
4. **Secrets** (obrigatório):

```toml
APP_PASSWORD = "sua-senha-segura"
```

5. Deploy → compartilhe o link `https://....streamlit.app` no WhatsApp do grupo

Detalhes: [DEPLOY.md](DEPLOY.md)

## Uso local

- `INSTALAR.bat` — primeira vez  
- `INICIAR.bat` — abrir no PC da paróquia  

## Tecnologias

Streamlit · Excel · Python · R (relatórios) · Rust (rota opcional)
