@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === Apostolado da Oração - Instalação ===
python --version >nul 2>&1
if errorlevel 1 (
    echo Python não encontrado. Instale Python 3.10+ de python.org
    pause
    exit /b 1
)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo.
echo Criando planilha inicial...
cd app\utils
python inicializar_excel.py
cd ..\..
echo.
echo Instalação concluída. Execute INICIAR.bat
pause
