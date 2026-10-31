"""
git_diff_tool.py: Điểm khởi chạy chính của ứng dụng Git Diff Tool.
Tích hợp giao diện Clean Light, Git Engine nâng cao và Diff Exporter thông minh.
"""

import sys
import tkinter as tk

from core.git_finder import setup_git_environment
from ui.main_window import MainWindow


def main():
    """Khởi động ứng dụng Git Diff Tool"""
    # 1. Tự động kiểm tra và cấu hình môi trường Git
    try:
        setup_git_environment()
    except Exception as err:
        print(f"Cảnh báo môi trường Git: {err}", file=sys.stderr)

    # 2. Khởi tạo giao diện Tkinter
    root = tk.Tk()
    app = MainWindow(root)

    def on_closing():
        try:
            app.cleanup()
        finally:
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()