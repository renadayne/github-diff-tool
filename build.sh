#!/bin/bash

echo "========================================"
echo "   Git Diff Tool - Build Script"
echo "========================================"
echo

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Python3 chưa được cài đặt"
    exit 1
fi

# Cài đặt thư viện cần thiết
echo "📦 Cài đặt thư viện cần thiết..."
python3 -m pip install -r requirements.txt
python3 -m pip install pyinstaller

if [ $? -ne 0 ]; then
    echo "❌ Lỗi: Không thể cài đặt thư viện"
    exit 1
fi

echo
echo "🔨 Bắt đầu build executable..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Lỗi khi build"
    exit 1
fi

echo
echo "✅ Build hoàn thành!"
echo "📁 Kiểm tra thư mục dist/ để lấy file executable" 