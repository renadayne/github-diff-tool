@echo off
echo ========================================
echo    Git Diff Tool - Công cụ so sánh Git
echo ========================================
echo.

REM Kiểm tra Python có được cài đặt không
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Lỗi: Python chưa được cài đặt hoặc không có trong PATH
    echo 📥 Vui lòng tải và cài đặt Python từ: https://python.org
    pause
    exit /b 1
)

REM Kiểm tra file requirements.txt
if not exist "requirements.txt" (
    echo ❌ Lỗi: Không tìm thấy file requirements.txt
    pause
    exit /b 1
)

REM Cài đặt thư viện nếu chưa có
echo 📦 Kiểm tra và cài đặt thư viện cần thiết...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Lỗi: Không thể cài đặt thư viện
    pause
    exit /b 1
)

echo.
echo 🚀 Khởi động Git Diff Tool...
echo.

REM Chạy ứng dụng
python run.py

if errorlevel 1 (
    echo.
    echo ❌ Lỗi khi chạy ứng dụng
    pause
    exit /b 1
)

echo.
echo ✅ Ứng dụng đã đóng
pause 