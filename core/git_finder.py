"""
git_finder.py: Tự động tìm kiếm và thiết lập đường dẫn Git executable trên Windows, Linux và macOS.
"""

import os
import shutil
import subprocess
import sys


def find_git_executable() -> str | None:
    """
    Tìm kiếm đường dẫn git executable khả dụng.
    Trả về đường dẫn tuyệt đối hoặc None nếu không tìm thấy.
    """
    # 1. Kiểm tra PATH tiêu chuẩn
    git_in_path = shutil.which("git")
    if git_in_path and _verify_git(git_in_path):
        return os.path.abspath(git_in_path)

    # 2. Kiểm tra biến môi trường người dùng nếu có
    custom_env = os.environ.get("GIT_PYTHON_GIT_EXECUTABLE")
    if custom_env and os.path.isfile(custom_env) and _verify_git(custom_env):
        return os.path.abspath(custom_env)

    # 3. Quét các đường dẫn cài đặt phổ biến trên Windows
    if sys.platform == "win32":
        candidates = [
            r"D:\Software\Git\Git\cmd\git.exe",
            r"D:\Software\Git\Git\bin\git.exe",
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files\Git\bin\git.exe",
            r"C:\Program Files (x86)\Git\cmd\git.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe"),
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\bin\git.exe"),
            os.path.expanduser(r"~\scoop\shims\git.exe"),
            r"C:\ProgramData\chocolatey\bin\git.exe",
        ]

        # Kiểm tra qua Registry Windows
        reg_path = _find_git_from_registry()
        if reg_path:
            candidates.insert(0, reg_path)

        for path in candidates:
            if path and os.path.isfile(path) and _verify_git(path):
                return os.path.abspath(path)

    # 4. Unix phổ biến
    unix_candidates = [
        "/usr/bin/git",
        "/usr/local/bin/git",
        "/opt/homebrew/bin/git",
    ]
    for path in unix_candidates:
        if os.path.isfile(path) and _verify_git(path):
            return path

    return None


def _find_git_from_registry() -> str | None:
    """Đọc đường dẫn cài đặt Git từ Registry Windows"""
    try:
        import winreg  # type: ignore

        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                key = winreg.OpenKey(hive, r"SOFTWARE\GitForWindows")
                install_dir, _ = winreg.QueryValueEx(key, "InstallPath")
                winreg.CloseKey(key)
                if install_dir:
                    cmd_path = os.path.join(install_dir, "cmd", "git.exe")
                    if os.path.isfile(cmd_path):
                        return cmd_path
            except OSError:
                continue
    except Exception:
        pass
    return None


def _verify_git(executable_path: str) -> bool:
    """Kiểm tra file có thực thi được 'git --version' không"""
    try:
        res = subprocess.run(
            [executable_path, "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
        return res.returncode == 0 and "git version" in res.stdout.lower()
    except Exception:
        return False


def setup_git_environment() -> str:
    """
    Khởi tạo môi trường Git cho ứng dụng.
    Tự động đặt GIT_PYTHON_GIT_EXECUTABLE và bổ sung vào PATH.
    Trả về đường dẫn Git hoặc ném RuntimeError nếu không tìm thấy.
    """
    git_path = find_git_executable()
    if not git_path:
        raise RuntimeError(
            "Không tìm thấy Git trên hệ thống. Vui lòng cài đặt Git và đảm bảo 'git' có thể chạy được."
        )

    os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = git_path

    # Thêm thư mục chứa git.exe vào PATH nếu chưa có
    git_dir = os.path.dirname(git_path)
    current_path = os.environ.get("PATH", "")
    if git_dir not in current_path:
        os.environ["PATH"] = git_dir + os.path.pathsep + current_path

    return git_path


if __name__ == "__main__":
    try:
        path = setup_git_environment()
        print(f"Git phát hiện thành công: {path}")
    except Exception as err:
        print(f"Lỗi: {err}", file=sys.stderr)
