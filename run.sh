#!/bin/bash

echo "========================================"
echo "   Git Diff Tool"
echo "========================================"
echo

# Kiem tra Python
if ! command -v python3 &> /dev/null; then
    echo "[Loi] Python3 chua duoc cai dat tren he thong."
    exit 1
fi

# Kiem tra requirements
if [ ! -f "requirements.txt" ]; then
    echo "[Loi] Khong tim thay file requirements.txt."
    exit 1
fi

echo "Khoi dong Git Diff Tool..."
python3 run.py

if [ $? -ne 0 ]; then
    echo
    echo "[Loi] Ung dung dung lai voi loi."
    exit 1
fi