#!/bin/bash

echo "========================================"
echo "   Git Diff Tool - Công cụ so sánh Git"
echo "========================================"
echo

# Kiểm tra Python có được cài đặt không
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Python3 chưa được cài đặt"
    echo "📥 Vui lòng cài đặt Python3:"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "   macOS: brew install python3"
    exit 1
fi

# Kiểm tra file requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ Lỗi: Không tìm thấy file requirements.txt"
    exit 1
fi

# Cài đặt thư viện nếu chưa có
echo "📦 Kiểm tra và cài đặt thư viện cần thiết..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Lỗi: Không thể cài đặt thư viện"
    exit 1
fi

echo
echo "🚀 Khởi động Git Diff Tool..."
echo

# Chạy ứng dụng
python3 run.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Lỗi khi chạy ứng dụng"
    exit 1
fi

echo
echo "✅ Ứng dụng đã đóng" 