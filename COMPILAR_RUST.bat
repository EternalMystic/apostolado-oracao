@echo off
chcp 65001 >nul
cd /d "%~dp0rust_utils\route_optimizer"
where cargo >nul 2>&1
if errorlevel 1 (
    echo Rust/Cargo não encontrado. Instale de https://rustup.rs
    pause
    exit /b 1
)
cargo build --release
echo.
echo Binário: target\release\route_optimizer.exe
pause
