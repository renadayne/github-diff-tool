"""
diff_exporter.py: Xuất các file thay đổi hoặc toàn bộ snapshot vào thư mục before/ và after/.
Hỗ trợ tạo kèm file patch và báo cáo tóm tắt diff_summary.md / diff_summary.json.
"""

import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Optional

from core.git_service import DiffFileItem, GitService


@dataclass
class ExportResult:
    """Kết quả sau khi xuất diff"""
    success: bool
    target_dir: str
    before_dir: str
    after_dir: str
    patch_file: Optional[str] = None
    summary_file: Optional[str] = None
    total_files_changed: int = 0
    total_insertions: int = 0
    total_deletions: int = 0
    error_message: Optional[str] = None


class DiffExporter:
    """Thực hiện trích xuất và xuất diff theo cấu trúc thư mục"""

    def __init__(self, git_service: GitService):
        self.git_service = git_service

    def export(
        self,
        rev1: str,
        rev2: str,
        target_dir: str,
        mode: str = "changed_only",  # "changed_only" hoặc "full_snapshot"
        generate_patch: bool = True,
        generate_summary: bool = True,
        progress_callback: Optional[Callable[[int, int, str], None]] = None,
    ) -> ExportResult:
        """
        Xuất diff giữa 2 revision vào thư mục đích.
        Tự động tạo before/ và after/ và dọn dẹp nội dung cũ nếu có.
        """
        target_dir = os.path.abspath(target_dir)
        before_dir = os.path.join(target_dir, "before")
        after_dir = os.path.join(target_dir, "after")

        try:
            # Tạo mới các thư mục đích
            os.makedirs(before_dir, exist_ok=True)
            os.makedirs(after_dir, exist_ok=True)

            diff_items = self.git_service.get_diff_file_list(rev1, rev2)
            total_items = len(diff_items)

            total_ins = sum(item.insertions for item in diff_items)
            total_dels = sum(item.deletions for item in diff_items)

            if mode == "changed_only":
                self._export_changed_only(
                    rev1, rev2, diff_items, before_dir, after_dir, progress_callback
                )
            else:
                self._export_full_snapshot(
                    rev1, rev2, before_dir, after_dir, progress_callback
                )

            # Tạo file patch
            patch_path: Optional[str] = None
            if generate_patch:
                patch_content = self.git_service.get_unified_diff(rev1, rev2)
                patch_path = os.path.join(target_dir, "changes.patch")
                with open(patch_path, "w", encoding="utf-8", errors="replace") as f:
                    f.write(patch_content)

            # Tạo báo cáo tóm tắt
            summary_path: Optional[str] = None
            if generate_summary:
                summary_path = self._write_summary_reports(
                    rev1, rev2, diff_items, target_dir, total_ins, total_dels
                )

            return ExportResult(
                success=True,
                target_dir=target_dir,
                before_dir=before_dir,
                after_dir=after_dir,
                patch_file=patch_path,
                summary_file=summary_path,
                total_files_changed=total_items,
                total_insertions=total_ins,
                total_deletions=total_dels,
            )

        except Exception as err:
            return ExportResult(
                success=False,
                target_dir=target_dir,
                before_dir=before_dir,
                after_dir=after_dir,
                error_message=str(err),
            )

    def _export_changed_only(
        self,
        rev1: str,
        rev2: str,
        diff_items: List[DiffFileItem],
        before_dir: str,
        after_dir: str,
        progress_callback: Optional[Callable[[int, int, str], None]],
    ):
        """Chỉ xuất những file có sự thay đổi (giữ nguyên cây thư mục con tương đối)"""
        total = len(diff_items)
        for idx, item in enumerate(diff_items, start=1):
            if progress_callback:
                progress_callback(idx, total, item.path)

            # Xử lý cho thư mục before (nếu file tồn tại ở rev1: Modified, Deleted, Renamed)
            if item.status in ("M", "D", "R", "C"):
                src_path = item.old_path if item.old_path else item.path
                content_v1 = self.git_service.get_file_content_at_rev(rev1, src_path)
                if content_v1 is not None:
                    dest_before = os.path.join(before_dir, src_path)
                    os.makedirs(os.path.dirname(dest_before), exist_ok=True)
                    with open(dest_before, "wb") as f:
                        f.write(content_v1)

            # Xử lý cho thư mục after (nếu file tồn tại ở rev2: Modified, Added, Renamed)
            if item.status in ("M", "A", "R", "C"):
                content_v2 = self.git_service.get_file_content_at_rev(rev2, item.path)
                if content_v2 is not None:
                    dest_after = os.path.join(after_dir, item.path)
                    os.makedirs(os.path.dirname(dest_after), exist_ok=True)
                    with open(dest_after, "wb") as f:
                        f.write(content_v2)

    def _export_full_snapshot(
        self,
        rev1: str,
        rev2: str,
        before_dir: str,
        after_dir: str,
        progress_callback: Optional[Callable[[int, int, str], None]],
    ):
        """Xuất snapshot toàn bộ kho mã nguồn bằng git archive (không ảnh hưởng working tree)"""
        repo = self.git_service.repo
        if not repo:
            raise RuntimeError("Chưa có repository nào được mở")

        import tarfile
        import io

        # Xuất trước cho before_dir
        if progress_callback:
            progress_callback(1, 2, "Đang trích xuất snapshot Trước (before)...")
        r1 = self.git_service.resolve_ref(rev1)
        tar_bytes_1 = repo.git.archive(r1, format="tar", as_process=True).stdout.read()
        with tarfile.open(fileobj=io.BytesIO(tar_bytes_1)) as tar:
            tar.extractall(path=before_dir)

        # Xuất tiếp cho after_dir
        if progress_callback:
            progress_callback(2, 2, "Đang trích xuất snapshot Sau (after)...")
        r2 = self.git_service.resolve_ref(rev2)
        tar_bytes_2 = repo.git.archive(r2, format="tar", as_process=True).stdout.read()
        with tarfile.open(fileobj=io.BytesIO(tar_bytes_2)) as tar:
            tar.extractall(path=after_dir)

    def _write_summary_reports(
        self,
        rev1: str,
        rev2: str,
        diff_items: List[DiffFileItem],
        target_dir: str,
        total_ins: int,
        total_dels: int,
    ) -> str:
        """Ghi báo cáo markdown và JSON tóm tắt các thay đổi"""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Ghi JSON
        json_data = {
            "timestamp": now_str,
            "base_revision": rev1,
            "target_revision": rev2,
            "total_files_changed": len(diff_items),
            "total_insertions": total_ins,
            "total_deletions": total_dels,
            "files": [
                {
                    "path": item.path,
                    "old_path": item.old_path,
                    "status": item.status_label,
                    "status_code": item.status,
                    "insertions": item.insertions,
                    "deletions": item.deletions,
                }
                for item in diff_items
            ],
        }
        json_path = os.path.join(target_dir, "diff_summary.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)

        # Ghi Markdown
        md_lines = [
            "# Git Diff Summary Report",
            "",
            f"- **Base Revision (Before):** `{rev1}`",
            f"- **Target Revision (After):** `{rev2}`",
            f"- **Generated At:** {now_str}",
            f"- **Files Changed:** {len(diff_items)}",
            f"- **Insertions:** +{total_ins}",
            f"- **Deletions:** -{total_dels}",
            "",
            "## Changed Files",
            "",
            "| Status | File Path | Additions | Deletions |",
            "| :--- | :--- | :---: | :---: |",
        ]

        for item in diff_items:
            path_display = item.path if not item.old_path else f"{item.old_path} -> {item.path}"
            md_lines.append(
                f"| `{item.status_label}` | `{path_display}` | +{item.insertions} | -{item.deletions} |"
            )

        md_path = os.path.join(target_dir, "diff_summary.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines) + "\n")

        return md_path
