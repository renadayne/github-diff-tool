@echo off
echo ========================================
echo    Git Diff Tool - Build Script
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Lỗi: Python chưa được cài đặt
    pause
    exit /b 1
)

REM Cài đặt thư viện cần thiết
echo 📦 Cài đặt thư viện cần thiết...
pip install -r requirements.txt
pip install pyinstaller

if errorlevel 1 (
    echo ❌ Lỗi: Không thể cài đặt thư viện
    pause
    exit /b 1
)

echo.
echo 🔨 Bắt đầu build executable...
python setup.py

if errorlevel 1 (
    echo.
    echo ❌ Lỗi khi build
    pause
    exit /b 1
)

echo.
echo ✅ Build hoàn thành!
echo 📁 Kiểm tra thư mục dist/ để lấy file executable
pause 