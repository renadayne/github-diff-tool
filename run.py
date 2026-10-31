#!/usr/bin/env python3
"""
run.py: Script khởi chạy Git Diff Tool có hỗ trợ tự động kiểm tra môi trường,
tự động chuyển sang venv cục bộ nếu môi trường toàn cục thiếu thư viện.
"""

import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def _try_reexec_with_venv():
    """Tự động chuyển sang .venv nếu có sẵn"""
    venv_python = os.path.join(BASE_DIR, ".venv", "Scripts", "python.exe")
    if sys.platform != "win32":
        venv_python = os.path.join(BASE_DIR, ".venv", "bin", "python")

    current_python = os.path.abspath(sys.executable)
    if os.path.isfile(venv_python) and current_python.lower() != os.path.abspath(venv_python).lower():
        # Tránh lặp vô hạn
        if os.environ.get("_GITDIFF_VENV_ATTEMPTED") != "1":
            env = os.environ.copy()
            env["_GITDIFF_VENV_ATTEMPTED"] = "1"
            res = subprocess.call([venv_python, os.path.abspath(__file__)] + sys.argv[1:], env=env)
            sys.exit(res)


# 1. Cấu hình môi trường Git
try:
    from core.git_finder import setup_git_environment
    setup_git_environment()
except Exception as err:
    print(f"Cảnh báo Git: {err}")

# 2. Khởi chạy ứng dụng
try:
    from git_diff_tool import main
    print("Khởi động Git Diff Tool...")
    main()
except ImportError as err:
    # Nếu thiếu thư viện ở môi trường hiện tại, thử tìm trong .venv
    _try_reexec_with_venv()

    print(f"\n[Lỗi thiếu thư viện]: {err}")
    print("\nDo môi trường Python của bạn được quản lý bởi uv (PEP 668), bạn có thể cài đặt bằng:")
    print("   1) Cài đặt trực tiếp:")
    print("      python -m pip install -r requirements.txt --break-system-packages")
    print("   2) Hoặc cài qua uv:")
    print("      uv pip install -r requirements.txt")
    print("   3) Hoặc chạy qua môi trường ảo .venv đã được tạo sẵn:")
    print("      .\\.venv\\Scripts\\python.exe run.py\n")
    sys.exit(1)
except Exception as err:
    print(f"[Lỗi khởi động ứng dụng]: {err}")
    sys.exit(1)