@echo off
chcp 65001 >nul
cd /d "%~dp0"
set TASK=ApostoladoBackupDiario
set SCRIPT=%~dp0backup_diario.py
schtasks /Create /TN "%TASK%" /TR "python \"%SCRIPT%\"" /SC DAILY /ST 23:00 /F
if errorlevel 1 (
    echo Falha ao criar tarefa. Execute como Administrador.
) else (
    echo Tarefa agendada: %TASK% às 23:00 diariamente.
)
pause
