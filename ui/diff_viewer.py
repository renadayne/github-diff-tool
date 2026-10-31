"""
diff_viewer.py: Khung xem và phân tích Diff trực quan ngay trong ứng dụng với cú pháp tô màu.
"""

import os
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
from typing import List, Optional

from core.git_service import DiffFileItem, GitService
from ui.theme import CleanLightTheme


class DiffViewerFrame(ttk.Frame):
    """Component hiển thị danh sách file thay đổi và trình xem Diff có màu"""

    def __init__(self, parent, git_service: GitService, **kwargs):
        super().__init__(parent, **kwargs)
        self.git_service = git_service
        self.rev1: str = ""
        self.rev2: str = ""
        self.target_dir: str = ""
        self.diff_items: List[DiffFileItem] = []

        self._setup_ui()

    def _setup_ui(self):
        # 1. Thanh công cụ phía trên
        toolbar = ttk.Frame(self, style="Card.TFrame", padding=(8, 6))
        toolbar.pack(fill=tk.X, pady=(0, 6))

        self.summary_label = ttk.Label(
            toolbar,
            text="Danh sách thay đổi: Chưa có dữ liệu",
            style="Card.TLabel",
            font=(CleanLightTheme.FONT_FAMILY, 9, "bold"),
        )
        self.summary_label.pack(side=tk.LEFT, padx=4)

        # Nút tiện ích bên phải
        self.btn_copy_diff = ttk.Button(
            toolbar,
            text="Sao chép Diff",
            command=self._copy_diff_to_clipboard,
            state="disabled",
        )
        self.btn_copy_diff.pack(side=tk.RIGHT, padx=4)

        self.btn_open_vscode = ttk.Button(
            toolbar,
            text="Mở trong VS Code",
            command=self._open_in_vscode,
            state="disabled",
        )
        self.btn_open_vscode.pack(side=tk.RIGHT, padx=4)

        self.btn_open_after = ttk.Button(
            toolbar,
            text="Mở folder After",
            command=lambda: self._open_folder("after"),
            state="disabled",
        )
        self.btn_open_after.pack(side=tk.RIGHT, padx=4)

        self.btn_open_before = ttk.Button(
            toolbar,
            text="Mở folder Before",
            command=lambda: self._open_folder("before"),
            state="disabled",
        )
        self.btn_open_before.pack(side=tk.RIGHT, padx=4)

        # 2. PanedWindow chia 2 cột: Trái (File Tree) - Phải (Diff text)
        paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Cột trái: Treeview
        tree_frame = ttk.Frame(paned, style="Card.TFrame")
        paned.add(tree_frame, weight=1)

        tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("status", "path", "stats"),
            show="headings",
            selectmode="browse",
            yscrollcommand=tree_scroll_y.set,
        )
        tree_scroll_y.config(command=self.tree.yview)

        self.tree.heading("status", text="Trạng thái")
        self.tree.heading("path", text="Đường dẫn file")
        self.tree.heading("stats", text="+ / -")

        self.tree.column("status", width=80, anchor=tk.CENTER)
        self.tree.column("path", width=220, anchor=tk.W)
        self.tree.column("stats", width=80, anchor=tk.E)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_file_selected)

        # Cột phải: Diff text có tô màu
        diff_frame = ttk.Frame(paned, style="Card.TFrame")
        paned.add(diff_frame, weight=2)

        diff_scroll_y = ttk.Scrollbar(diff_frame, orient=tk.VERTICAL)
        diff_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        diff_scroll_x = ttk.Scrollbar(diff_frame, orient=tk.HORIZONTAL)
        diff_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.diff_text = tk.Text(
            diff_frame,
            wrap=tk.NONE,
            font=(CleanLightTheme.FONT_MONO, 9),
            bg=CleanLightTheme.BG_CARD,
            fg=CleanLightTheme.TEXT_MAIN,
            relief="flat",
            borderwidth=1,
            padx=8,
            pady=8,
            yscrollcommand=diff_scroll_y.set,
            xscrollcommand=diff_scroll_x.set,
        )
        self.diff_text.pack(fill=tk.BOTH, expand=True)
        diff_scroll_y.config(command=self.diff_text.yview)
        diff_scroll_x.config(command=self.diff_text.xview)

        # Thiết lập tag tô màu cho git diff
        self.diff_text.tag_config(
            "diff_add",
            foreground=CleanLightTheme.DIFF_ADD_FG,
            background=CleanLightTheme.DIFF_ADD_BG,
        )
        self.diff_text.tag_config(
            "diff_del",
            foreground=CleanLightTheme.DIFF_DEL_FG,
            background=CleanLightTheme.DIFF_DEL_BG,
        )
        self.diff_text.tag_config(
            "diff_hunk",
            foreground=CleanLightTheme.DIFF_HUNK_FG,
            background=CleanLightTheme.DIFF_HUNK_BG,
            font=(CleanLightTheme.FONT_MONO, 9, "bold"),
        )
        self.diff_text.tag_config(
            "diff_header",
            foreground=CleanLightTheme.TEXT_MAIN,
            background=CleanLightTheme.BG_CARD_SUBTLE,
            font=(CleanLightTheme.FONT_MONO, 9, "bold"),
        )

        self._set_placeholder_text("Chọn một file trong danh sách bên trái để xem diff chi tiết.")

    def update_diff_data(
        self,
        rev1: str,
        rev2: str,
        target_dir: str = "",
        diff_items: Optional[List[DiffFileItem]] = None,
    ):
        """Cập nhật dữ liệu so sánh mới vào giao diện"""
        self.rev1 = rev1
        self.rev2 = rev2
        self.target_dir = target_dir

        if diff_items is None:
            self.diff_items = self.git_service.get_diff_file_list(rev1, rev2)
        else:
            self.diff_items = diff_items

        # Xóa dữ liệu cũ trong treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_files = len(self.diff_items)
        total_ins = sum(i.insertions for i in self.diff_items)
        total_dels = sum(i.deletions for i in self.diff_items)

        self.summary_label.config(
            text=f"Thay đổi: {total_files} file | +{total_ins} dòng | -{total_dels} dòng"
        )

        for item in self.diff_items:
            display_path = item.path if not item.old_path else f"{item.old_path} -> {item.path}"
            stat_str = f"+{item.insertions} / -{item.deletions}"
            self.tree.insert(
                "",
                tk.END,
                iid=item.path,
                values=(item.status_label, display_path, stat_str),
            )

        has_items = total_files > 0
        self.btn_copy_diff.config(state="normal" if has_items else "disabled")
        self.btn_open_vscode.config(state="normal" if has_items else "disabled")

        has_target = bool(target_dir and os.path.exists(target_dir))
        self.btn_open_before.config(state="normal" if has_target else "disabled")
        self.btn_open_after.config(state="normal" if has_target else "disabled")

        if has_items:
            # Tự động chọn file đầu tiên
            first_id = self.diff_items[0].path
            self.tree.selection_set(first_id)
            self._render_file_diff(first_id)
        else:
            self._set_placeholder_text("Không có sự khác biệt nào giữa 2 phiên bản này.")

    def _on_file_selected(self, event):
        """Khi người dùng click chọn 1 file trong danh sách"""
        selected = self.tree.selection()
        if not selected:
            return
        file_path = selected[0]
        self._render_file_diff(file_path)

    def _render_file_diff(self, file_path: str):
        """Tải và hiển thị diff có màu cho file được chọn"""
        diff_content = self.git_service.get_unified_diff(self.rev1, self.rev2, file_path)

        self.diff_text.config(state=tk.NORMAL)
        self.diff_text.delete("1.0", tk.END)

        if not diff_content.strip():
            self.diff_text.insert(tk.END, "Không có nội dung diff cho file này (có thể là file binary).")
            self.diff_text.config(state=tk.DISABLED)
            return

        for line in diff_content.splitlines(keepends=True):
            if line.startswith("+++") or line.startswith("---") or line.startswith("diff "):
                self.diff_text.insert(tk.END, line, "diff_header")
            elif line.startswith("@@"):
                self.diff_text.insert(tk.END, line, "diff_hunk")
            elif line.startswith("+"):
                self.diff_text.insert(tk.END, line, "diff_add")
            elif line.startswith("-"):
                self.diff_text.insert(tk.END, line, "diff_del")
            else:
                self.diff_text.insert(tk.END, line)

        self.diff_text.config(state=tk.DISABLED)

    def _set_placeholder_text(self, text: str):
        self.diff_text.config(state=tk.NORMAL)
        self.diff_text.delete("1.0", tk.END)
        self.diff_text.insert(tk.END, text)
        self.diff_text.config(state=tk.DISABLED)

    def _copy_diff_to_clipboard(self):
        """Sao chép toàn bộ diff vào clipboard"""
        selected = self.tree.selection()
        file_filter = selected[0] if selected else None
        diff_str = self.git_service.get_unified_diff(self.rev1, self.rev2, file_filter)
        if diff_str:
            self.clipboard_clear()
            self.clipboard_append(diff_str)
            messagebox.showinfo("Thành công", "Đã sao chép nội dung diff vào Clipboard!")

    def _open_in_vscode(self):
        """Mở diff trong VS Code nếu có"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn một file trong bảng.")
            return

        file_path = selected[0]
        before_file = os.path.join(self.target_dir, "before", file_path) if self.target_dir else ""
        after_file = os.path.join(self.target_dir, "after", file_path) if self.target_dir else ""

        if before_file and after_file and os.path.exists(before_file) and os.path.exists(after_file):
            try:
                subprocess.Popen(["code", "--diff", before_file, after_file], shell=True)
                return
            except Exception:
                pass

        # Nếu chưa xuất thư mục, mở repo path
        if self.git_service.repo_path:
            try:
                subprocess.Popen(["code", self.git_service.repo_path], shell=True)
            except Exception as err:
                messagebox.showerror("Lỗi", f"Không thể mở VS Code: {err}")

    def _open_folder(self, which: str):
        """Mở thư mục before hoặc after trong Explorer"""
        if not self.target_dir:
            return
        folder_path = os.path.join(self.target_dir, which)
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            messagebox.showwarning("Thông báo", f"Thư mục {which} chưa được tạo hoặc không tồn tại.")
