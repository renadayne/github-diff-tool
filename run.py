#!/usr/bin/env python3
"""
run.py: Script khởi chạy Git Diff Tool có hỗ trợ tự động kiểm tra môi trường.
"""

import os
import sys

# Đảm bảo thư mục gốc dự án luôn nằm trong sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from core.git_finder import setup_git_environment
    setup_git_environment()
except Exception as err:
    print(f"Cảnh báo Git: {err}")

try:
    from git_diff_tool import main
    print("Khởi động Git Diff Tool...")
    main()
except ImportError as err:
    print(f"Lỗi thiếu thư viện: {err}")
    print("Vui lòng cài đặt các thư viện cần thiết:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as err:
    print(f"Lỗi khởi động ứng dụng: {err}")
    sys.exit(1)