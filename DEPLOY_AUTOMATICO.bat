@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  ============================================
echo   DEPLOY - Apostolado da Oraacao (Streamlit)
echo  ============================================
echo.
echo  Passo 1: Enviando codigo para o GitHub...
git add -A
git commit -m "Deploy visual roxo 50+" 2>nul
git push origin main
if errorlevel 1 (
    echo  Aviso: git push falhou - verifique internet e GitHub.
) else (
    echo  OK - GitHub atualizado.
)
echo.
echo  Passo 2: Abrindo o site de deploy no navegador...
echo.
echo  NA TELA QUE ABRIR, preencha:
echo    Repository: EternalMystic/apostolado-oracao
echo    Branch: main
echo    Main file: app/app.py
echo    App URL: apostolado-sao-jorge
echo.
echo  Em Advanced settings - Secrets, cole o conteudo de:
echo    STREAMLIT_SECRETS_COPIAR.txt
echo.
start https://share.streamlit.io/
start notepad "%~dp0STREAMLIT_SECRETS_COPIAR.txt"
echo.
pause
