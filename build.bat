@echo off
echo ========================================
echo    Git Diff Tool - Build Script
echo ========================================
echo.

REM Kiem tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [Loi] Python chua duoc cai dat hoac khong co trong PATH
    pause
    exit /b 1
)

REM Cai dat thu vien can thiet
echo [1/2] Kiem tra va cai dat thu vien can thiet...
pip install -r requirements.txt

if errorlevel 1 (
    echo [Loi] Khong the cai dat thu vien
    pause
    exit /b 1
)

echo.
echo [2/2] Bat dau build executable qua setup.py...
python setup.py

if errorlevel 1 (
    echo.
    echo [Loi] Qua trinh build that bai
    pause
    exit /b 1
)

echo.
echo [Thanh cong] Build hoan thanh. Kiem tra thu muc dist/ de lay file executable.
pause