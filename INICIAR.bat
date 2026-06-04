@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist "data\apostolado.xlsx" (
    echo Criando dados iniciais...
    cd app\utils
    python inicializar_excel.py
    cd ..\..
)
echo Iniciando Apostolado da Oração...
cd app
start "" http://localhost:8501
python -m streamlit run app.py --server.headless true
pause
