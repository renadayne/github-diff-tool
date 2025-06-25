#!/usr/bin/env python3
"""
Script để chạy Git Diff Tool
"""

import sys
import os

# Thêm thư mục hiện tại vào Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from git_diff_tool import main
    print("🚀 Khởi động Git Diff Tool...")
    main()
except ImportError as e:
    print(f"❌ Lỗi import: {e}")
    print("📦 Vui lòng cài đặt các thư viện cần thiết:")
    print("   pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Lỗi khởi động: {e}")
    sys.exit(1) 