@echo off
echo ========================================
echo    Git Diff Tool
echo ========================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Loi] Python chua duoc cai dat hoac khong co trong PATH
    echo Vui long cai dat Python tai: https://python.org
    pause
    exit /b 1
)

REM Kiem tra requirements
if not exist "requirements.txt" (
    echo [Loi] Khong tim thay file requirements.txt
    pause
    exit /b 1
)

REM Chay ung dung
echo Khoi dong Git Diff Tool...
python run.py

if errorlevel 1 (
    echo.
    echo [Loi] Ung dung da dung lai voi loi.
    pause
    exit /b 1
)