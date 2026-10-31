#!/bin/bash

echo "========================================"
echo "   Git Diff Tool - Build Script"
echo "========================================"
echo

# Kiem tra Python
if ! command -v python3 &> /dev/null; then
    echo "[Loi] Python3 chua duoc cai dat tren he thong."
    exit 1
fi

# Cai dat dependencies
echo "[1/2] Cai dat thu vien can thiet..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "[Loi] Khong the cai dat thu vien."
    exit 1
fi

echo
echo "[2/2] Bat dau build executable..."
python3 setup.py

if [ $? -ne 0 ]; then
    echo
    echo "[Loi] Qua trinh build that bai."
    exit 1
fi

echo
echo "[Thanh cong] Build hoan thanh. Kiem tra thu muc dist/ de lay file executable."