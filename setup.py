#!/usr/bin/env python3
"""
Setup script để đóng gói Git Diff Tool thành executable độc lập sử dụng PyInstaller.
"""

import os
import shutil
import subprocess
import sys


def install_pyinstaller():
    """Cài đặt PyInstaller nếu chưa có"""
    try:
        import PyInstaller  # type: ignore # noqa: F401
        print("[OK] PyInstaller đã được cài đặt sẵn.")
    except ImportError:
        print("[Info] Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller đã được cài đặt thành công.")


def build_executable():
    """Build executable với PyInstaller"""
    print("[Info] Đang build executable...")

    # Tạo thư mục dist nếu chưa có
    os.makedirs("dist", exist_ok=True)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=GitDiffTool",
        "--add-data=config.json;.",
        "--hidden-import=git",
        "--hidden-import=requests",
        "--hidden-import=core",
        "--hidden-import=core.git_finder",
        "--hidden-import=core.git_service",
        "--hidden-import=core.diff_exporter",
        "--hidden-import=core.config_manager",
        "--hidden-import=ui",
        "--hidden-import=ui.theme",
        "--hidden-import=ui.diff_viewer",
        "--hidden-import=ui.main_window",
        "git_diff_tool.py",
    ]

    if os.path.exists("icon.ico"):
        cmd.insert(cmd.index("git_diff_tool.py"), "--icon=icon.ico")

    try:
        subprocess.check_call(cmd)
        print("[OK] Build thành công.")

        # Copy các file tài liệu và runner sang dist
        files_to_copy = ["README.md", "USAGE_GUIDE.md", "PACKAGING_GUIDE.md", "config.json", "run.bat", "run.sh"]
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, "dist/")
                print(f"[Copy] {file} -> dist/")

        print("\nĐóng gói hoàn tất!")
        print("Executable được tạo tại: dist/GitDiffTool.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Lỗi] Thao tác build thất bại: {e}")
        return False


def create_installer():
    """Tạo installer script cho Windows"""
    print("[Info] Tạo installer script dist/install.bat...")

    installer_content = """@echo off
echo ========================================
echo    Git Diff Tool - Installer
echo ========================================
echo.

set INSTALL_DIR=%USERPROFILE%\\GitDiffTool
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo Dang copy cac file can thiet...
copy "GitDiffTool.exe" "%INSTALL_DIR%\\" >nul
copy "README.md" "%INSTALL_DIR%\\" >nul
copy "USAGE_GUIDE.md" "%INSTALL_DIR%\\" >nul
copy "config.json" "%INSTALL_DIR%\\" >nul

echo Tao shortcut tren Desktop...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Git Diff Tool.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\GitDiffTool.exe'; $Shortcut.Save()"

echo.
echo [Thanh cong] Cai dat hoan tat.
echo Thu muc cai dat: %INSTALL_DIR%
echo Shortcut da duoc tao tren Desktop.
echo.
pause
"""
    with open("dist/install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    print("[OK] Đã tạo file: dist/install.bat")


def main():
    print("=" * 50)
    print("   Bắt đầu đóng gói Git Diff Tool")
    print("=" * 50)

    install_pyinstaller()
    if build_executable():
        create_installer()
        print("\n" + "=" * 50)
        print("Hướng dẫn:")
        print("1. Chạy dist/install.bat để cài đặt vào máy")
        print("2. Hoặc chạy trực tiếp file dist/GitDiffTool.exe")
        print("=" * 50)
    else:
        print("\n[Lỗi] Đóng gói thất bại.")
        sys.exit(1)


if __name__ == "__main__":
    main()