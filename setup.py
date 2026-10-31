#!/usr/bin/env python3
"""
Setup script để đóng gói Git Diff Tool thành executable
"""

import os
import sys
import subprocess
import shutil

def install_pyinstaller():
    """Cài đặt PyInstaller nếu chưa có"""
    try:
        import PyInstaller
        print("✅ PyInstaller đã được cài đặt")
    except ImportError:
        print("📦 Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller đã được cài đặt thành công")

def build_executable():
    """Build executable với PyInstaller"""
    print("🔨 Đang build executable...")
    
    # Tạo thư mục dist nếu chưa có
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Lệnh PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Tạo 1 file executable duy nhất
        "--windowed",                   # Không hiển thị console window
        "--name=GitDiffTool",           # Tên file executable
        "--icon=icon.ico",              # Icon (nếu có)
        "--add-data=config.json;.",     # Thêm file config
        "--hidden-import=git",          # Import git module
        "--hidden-import=requests",     # Import requests module
        "--hidden-import=core",
        "--hidden-import=core.git_finder",
        "--hidden-import=core.git_service",
        "--hidden-import=core.diff_exporter",
        "--hidden-import=core.config_manager",
        "--hidden-import=ui",
        "--hidden-import=ui.theme",
        "--hidden-import=ui.diff_viewer",
        "--hidden-import=ui.main_window",
        "git_diff_tool.py"              # File chính
    ]
    
    # Bỏ icon nếu không có file icon
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Build thành công!")
        
        # Copy các file cần thiết vào thư mục dist
        files_to_copy = ["README.md", "USAGE_GUIDE.md", "run.bat", "run.sh"]
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, "dist/")
                print(f"📄 Đã copy {file}")
        
        print("\n🎉 Đóng gói hoàn thành!")
        print("📁 Executable được tạo tại: dist/GitDiffTool.exe")
        print("📦 Toàn bộ file được đặt tại: dist/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi build: {e}")
        return False
    
    return True

def create_installer():
    """Tạo installer script"""
    print("📦 Tạo installer script...")
    
    installer_content = """@echo off
echo ========================================
echo    Git Diff Tool - Installer
echo ========================================
echo.

REM Tạo thư mục cài đặt
set INSTALL_DIR=%USERPROFILE%\\GitDiffTool
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy files
echo Đang copy files...
copy "GitDiffTool.exe" "%INSTALL_DIR%\\"
copy "README.md" "%INSTALL_DIR%\\"
copy "USAGE_GUIDE.md" "%INSTALL_DIR%\\"
copy "run.bat" "%INSTALL_DIR%\\"
copy "run.sh" "%INSTALL_DIR%\\"

REM Tạo shortcut
echo Tạo shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Git Diff Tool.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\GitDiffTool.exe'; $Shortcut.Save()"

echo.
echo ✅ Cài đặt hoàn thành!
echo 📁 Thư mục cài đặt: %INSTALL_DIR%
echo 🖥️ Shortcut đã được tạo trên Desktop
echo.
pause
"""
    
    with open("dist/install.bat", "w", encoding="utf-8") as f:
        f.write(installer_content)
    
    print("✅ Installer script đã được tạo: dist/install.bat")

def main():
    """Hàm chính"""
    print("🚀 Bắt đầu đóng gói Git Diff Tool...")
    print("=" * 50)
    
    # Cài đặt PyInstaller
    install_pyinstaller()
    
    # Build executable
    if build_executable():
        # Tạo installer
        create_installer()
        
        print("\n" + "=" * 50)
        print("🎯 Hướng dẫn sử dụng:")
        print("1. Chạy dist/install.bat để cài đặt")
        print("2. Hoặc chạy trực tiếp dist/GitDiffTool.exe")
        print("3. File README.md và USAGE_GUIDE.md chứa hướng dẫn chi tiết")
    else:
        print("❌ Đóng gói thất bại!")

if __name__ == "__main__":
    main() 