"""
git_service.py: Dịch vụ tương tác với Git Repository (cả Local và Remote qua GitHub).
Cung cấp khả năng trích xuất nhánh, commit, phân tích diff không làm xáo trộn working tree.
"""

import os
import shutil
import tempfile
import urllib.parse
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from core.git_finder import setup_git_environment

# Đảm bảo Git executable được cấu hình trước khi import GitPython
setup_git_environment()
import git  # type: ignore # noqa: E402
from git import Repo  # noqa: E402


@dataclass
class CommitInfo:
    """Thông tin tóm tắt về commit"""
    hexsha: str
    short_hash: str
    author: str
    date_str: str
    summary: str

    def display_text(self) -> str:
        return f"{self.short_hash} - {self.summary} ({self.author}, {self.date_str})"


@dataclass
class DiffFileItem:
    """Thông tin về một file bị thay đổi giữa 2 revision"""
    status: str  # 'A', 'M', 'D', 'R', 'C'
    path: str
    old_path: Optional[str] = None
    insertions: int = 0
    deletions: int = 0

    @property
    def status_label(self) -> str:
        mapping = {
            "A": "Added",
            "M": "Modified",
            "D": "Deleted",
            "R": "Renamed",
            "C": "Copied",
        }
        return mapping.get(self.status, "Modified")


class GitService:
    """Dịch vụ bao bọc GitPython và các tác vụ Git an toàn"""

    def __init__(self):
        self.repo: Optional[Repo] = None
        self.repo_path: Optional[str] = None
        self.is_temporary: bool = False
        self.temp_dir: Optional[str] = None

    def open_local_repository(self, path: str) -> bool:
        """Mở repository có sẵn trên máy cục bộ"""
        path = os.path.abspath(path)
        if not os.path.isdir(path):
            raise ValueError(f"Đường dẫn không tồn tại: {path}")

        try:
            self.cleanup_temp_if_needed()
            self.repo = Repo(path)
            self.repo_path = path
            self.is_temporary = False
            return True
        except Exception as err:
            raise RuntimeError(f"Không thể mở Git repository tại '{path}': {err}")

    def clone_remote_repository(
        self,
        url: str,
        token: str = "",
        timeout: int = 300,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Clone repository từ GitHub/Git server về thư mục tạm.
        Hỗ trợ Personal Access Token cho repo private mà không treo terminal.
        """
        url = url.strip()
        if not url:
            raise ValueError("URL repository không được để trống")

        # Chuẩn bị URL có token an toàn
        clone_url = url
        if token.strip():
            tok = urllib.parse.quote(token.strip(), safe="")
            if "github.com" in url:
                if url.startswith("https://"):
                    clone_url = f"https://{tok}@github.com/" + url[len("https://github.com/") :]
                elif url.startswith("http://"):
                    clone_url = f"http://{tok}@github.com/" + url[len("http://github.com/") :]

        # Tạo thư mục tạm mới
        self.cleanup_temp_if_needed()
        self.temp_dir = tempfile.mkdtemp(prefix="gitdiff_")

        # Ngăn Git hiển thị prompt nhập mật khẩu nếu xác thực thất bại
        env = os.environ.copy()
        env["GIT_TERMINAL_PROMPT"] = "0"

        if progress_callback:
            progress_callback("Đang tiến hành clone repository...")

        try:
            self.repo = Repo.clone_from(
                clone_url,
                self.temp_dir,
                env=env,
                kill_after_timeout=timeout,
            )
            self.repo_path = self.temp_dir
            self.is_temporary = True
            return self.temp_dir
        except Exception as err:
            self.cleanup_temp_if_needed()
            raise RuntimeError(f"Lỗi khi clone repository: {err}")

    def get_branches(self) -> List[str]:
        """Lấy danh sách các nhánh hợp lệ (local và remote)"""
        if not self.repo:
            return []

        branch_set = set()

        # Nhánh local
        for head in self.repo.heads:
            branch_set.add(head.name)

        # Nhánh remote
        try:
            for ref in self.repo.references:
                name = ref.name
                if name.startswith("origin/") and not name.endswith("/HEAD"):
                    clean_name = name[len("origin/") :]
                    branch_set.add(clean_name)
        except Exception:
            pass

        branches = sorted(list(branch_set))
        # Đưa main/master lên đầu nếu có
        for primary in ("main", "master"):
            if primary in branches:
                branches.remove(primary)
                branches.insert(0, primary)
        return branches

    def get_recent_commits(self, max_count: int = 50, branch_or_ref: str = "HEAD") -> List[CommitInfo]:
        """Lấy danh sách commit gần nhất từ branch hoặc ref chỉ định"""
        if not self.repo:
            return []

        commits = []
        try:
            # Nếu ref là tên branch remote
            ref_to_query = branch_or_ref
            if ref_to_query not in self.repo.heads:
                remote_ref = f"origin/{ref_to_query}"
                if remote_ref in self.repo.references:
                    ref_to_query = remote_ref

            for c in self.repo.iter_commits(ref_to_query, max_count=max_count):
                dt = datetime.fromtimestamp(c.committed_date).strftime("%Y-%m-%d %H:%M")
                summary = c.message.strip().split("\n")[0]
                commits.append(
                    CommitInfo(
                        hexsha=c.hexsha,
                        short_hash=c.hexsha[:8],
                        author=c.author.name or "Unknown",
                        date_str=dt,
                        summary=summary,
                    )
                )
        except Exception as err:
            print(f"Lỗi khi đọc commits từ {branch_or_ref}: {err}")
        return commits

    def resolve_ref(self, ref_name: str) -> str:
        """Chuẩn hóa ref name (commit hash, branch local hoặc remote)"""
        if not self.repo:
            return ref_name

        ref_name = ref_name.strip()
        # Nếu đã là hash commit đầy đủ hoặc rút gọn
        if len(ref_name) >= 7 and all(c in "0123456789abcdefABCDEF" for c in ref_name):
            return ref_name

        # Nếu là local branch
        if ref_name in self.repo.heads:
            return ref_name

        # Nếu là remote branch
        remote_ref = f"origin/{ref_name}"
        if remote_ref in [r.name for r in self.repo.references]:
            return remote_ref

        return ref_name

    def get_diff_file_list(self, rev1: str, rev2: str) -> List[DiffFileItem]:
        """
        Lấy danh sách các file thay đổi giữa rev1 (base) và rev2 (target).
        Bao gồm trạng thái A/M/D/R và số dòng thêm/xóa.
        """
        if not self.repo:
            return []

        r1 = self.resolve_ref(rev1)
        r2 = self.resolve_ref(rev2)

        # Lấy diff name-status
        raw_status = self.repo.git.diff("--name-status", r1, r2)
        diff_items: List[DiffFileItem] = []

        if not raw_status.strip():
            return []

        # Lấy numstat để tính dòng thêm/xóa
        numstat_map: Dict[str, tuple[int, int]] = {}
        try:
            raw_numstat = self.repo.git.diff("--numstat", r1, r2)
            for line in raw_numstat.strip().splitlines():
                parts = line.split("\t")
                if len(parts) >= 3:
                    ins = int(parts[0]) if parts[0].isdigit() else 0
                    dels = int(parts[1]) if parts[1].isdigit() else 0
                    filepath = parts[2].strip()
                    numstat_map[filepath] = (ins, dels)
        except Exception:
            pass

        for line in raw_status.strip().splitlines():
            parts = line.split("\t")
            if not parts:
                continue

            status_code = parts[0].strip()
            status_char = status_code[0]

            if status_char == "R" and len(parts) >= 3:
                # Renamed: R100 \t old_path \t new_path
                old_p = parts[1].strip()
                new_p = parts[2].strip()
                ins, dels = numstat_map.get(new_p, (0, 0))
                diff_items.append(
                    DiffFileItem(
                        status="R",
                        path=new_p,
                        old_path=old_p,
                        insertions=ins,
                        deletions=dels,
                    )
                )
            elif len(parts) >= 2:
                file_p = parts[1].strip()
                ins, dels = numstat_map.get(file_p, (0, 0))
                diff_items.append(
                    DiffFileItem(
                        status=status_char,
                        path=file_p,
                        insertions=ins,
                        deletions=dels,
                    )
                )

        return diff_items

    def get_unified_diff(self, rev1: str, rev2: str, file_path: Optional[str] = None) -> str:
        """Lấy nội dung Unified Diff giữa 2 revision, có thể lọc theo 1 file"""
        if not self.repo:
            return ""

        r1 = self.resolve_ref(rev1)
        r2 = self.resolve_ref(rev2)

        try:
            if file_path:
                return self.repo.git.diff("-u", r1, r2, "--", file_path)
            return self.repo.git.diff("-u", r1, r2)
        except Exception as err:
            return f"Không thể lấy diff: {err}"

    def get_file_content_at_rev(self, rev: str, file_path: str) -> Optional[bytes]:
        """
        Trích xuất trực tiếp nội dung file tại revision mà KHÔNG cần checkout working tree.
        Trả về bytes hoặc None nếu file không tồn tại ở revision này (ví dụ file mới được add).
        """
        if not self.repo:
            return None

        resolved = self.resolve_ref(rev)
        clean_path = file_path.replace("\\", "/").lstrip("/")

        try:
            # Cách 1: Sử dụng GitPython commit tree blob
            commit = self.repo.commit(resolved)
            blob = commit.tree / clean_path
            return blob.data_stream.read()
        except KeyError:
            # File không tồn tại ở revision này
            return None
        except Exception:
            pass

        try:
            # Cách 2: Fallback qua git show dạng chuỗi mã hóa
            raw = self.repo.git.show(f"{resolved}:{clean_path}")
            return raw.encode("utf-8", errors="surrogateescape")
        except Exception:
            return None

    def cleanup_temp_if_needed(self):
        """Xóa thư mục tạm nếu đã clone trước đó"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                # Đóng repo object để giải phóng file locks trên Windows
                if self.repo:
                    self.repo.close()
                    self.repo = None
                shutil.rmtree(self.temp_dir, ignore_errors=True)
            except Exception:
                pass
            self.temp_dir = None


# Instance dùng chung
_global_git_service: Optional[GitService] = None


def get_git_service() -> GitService:
    global _global_git_service
    if _global_git_service is None:
        _global_git_service = GitService()
    return _global_git_service
