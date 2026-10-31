"""
main_window.py: Cửa sổ giao diện chính của Git Diff Tool theo thiết kế Clean Light.
"""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional

from core.config_manager import get_config_manager
from core.diff_exporter import DiffExporter, ExportResult
from core.git_service import GitService, get_git_service
from ui.diff_viewer import DiffViewerFrame
from ui.theme import CleanLightTheme


class MainWindow:
    """Cửa sổ ứng dụng chính"""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.config_mgr = get_config_manager()
        self.git_service = get_git_service()
        self.diff_exporter = DiffExporter(self.git_service)

        # Cấu hình cửa sổ
        self.root.title("Git Diff Tool - Công cụ so sánh Git")
        win_size = self.config_mgr.get("app_settings", "window_size", "1020x760")
        self.root.geometry(win_size)
        self.root.minsize(860, 640)

        # Áp dụng theme Clean Light
        CleanLightTheme.apply(self.root)

        # Biến trạng thái UI
        self.local_path_var = tk.StringVar(value=os.path.abspath("."))
        self.repo_url_var = tk.StringVar()
        self.token_var = tk.StringVar()

        self.compare_mode = tk.StringVar(value="branch")  # "branch" hoặc "commit"
        self.rev1_var = tk.StringVar()
        self.rev2_var = tk.StringVar()

        default_out = self.config_mgr.get("app_settings", "default_target_dir", "")
        if not default_out:
            default_out = os.path.join(os.path.expanduser("~"), "Desktop", "git_diff_result")
        self.target_dir_var = tk.StringVar(value=default_out)

        self.export_mode_var = tk.StringVar(
            value=self.config_mgr.get("app_settings", "export_mode", "changed_only")
        )
        self.gen_patch_var = tk.BooleanVar(
            value=self.config_mgr.get("app_settings", "generate_patch", True)
        )
        self.gen_summary_var = tk.BooleanVar(
            value=self.config_mgr.get("app_settings", "generate_summary", True)
        )

        self.status_var = tk.StringVar(value="Sẵn sàng")
        self.repo_status_var = tk.StringVar(value="⚪ Chưa nạp repository")

        self.branches = []
        self.commits = []

        self._build_ui()
        self._try_load_initial_repo()

    def _build_ui(self):
        """Khởi dựng layout toàn bộ cửa sổ"""
        # Container chính cuộn hoặc padding
        main_container = ttk.Frame(self.root, padding=12)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 1. Header Card
        self._build_header(main_container)

        # 2. Section: Chọn nguồn Repository
        self._build_source_section(main_container)

        # 3. Section: Cấu hình so sánh (Branches / Commits) & Xuất dữ liệu
        self._build_control_section(main_container)

        # 4. Section: Diff Viewer (Xem thay đổi trực quan)
        self._build_viewer_section(main_container)

        # 5. Footer: Progress & Status
        self._build_footer(main_container)

    def _build_header(self, parent):
        header_card = ttk.Frame(parent, style="Card.TFrame", padding=(12, 8))
        header_card.pack(fill=tk.X, pady=(0, 8))

        # Tiêu đề bên trái
        left_box = ttk.Frame(header_card, style="Card.TFrame")
        left_box.pack(side=tk.LEFT, fill=tk.Y)

        title_lbl = ttk.Label(
            left_box,
            text="Git Diff Tool",
            style="Title.TLabel",
        )
        title_lbl.pack(anchor=tk.W)

        sub_lbl = ttk.Label(
            left_box,
            text="Phân tích thay đổi nhánh, commit và xuất file before/after chuyên nghiệp",
            style="Muted.TLabel",
        )
        sub_lbl.pack(anchor=tk.W)

        # Badge trạng thái bên phải
        self.badge_lbl = ttk.Label(
            header_card,
            textvariable=self.repo_status_var,
            style="Card.TLabel",
            font=(CleanLightTheme.FONT_FAMILY, 9, "bold"),
            foreground=CleanLightTheme.PRIMARY,
        )
        self.badge_lbl.pack(side=tk.RIGHT, padx=4)

    def _build_source_section(self, parent):
        source_card = ttk.Frame(parent, style="Card.TFrame", padding=(12, 10))
        source_card.pack(fill=tk.X, pady=(0, 8))

        lbl_sec = ttk.Label(source_card, text="1. Nguồn Repository", style="Section.TLabel")
        lbl_sec.pack(anchor=tk.W, pady=(0, 6))

        notebook = ttk.Notebook(source_card)
        notebook.pack(fill=tk.X)

        # Tab 1: Local Repo
        tab_local = ttk.Frame(notebook, style="Card.TFrame", padding=10)
        notebook.add(tab_local, text="Thư mục máy (Local Repo)")

        ttk.Label(tab_local, text="Đường dẫn Git trên máy:", style="Card.TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=4
        )
        local_entry = ttk.Entry(tab_local, textvariable=self.local_path_var, width=55)
        local_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=6, pady=4)
        tab_local.columnconfigure(1, weight=1)

        btn_browse_local = ttk.Button(
            tab_local, text="Chọn thư mục...", command=self._browse_local_repo
        )
        btn_browse_local.grid(row=0, column=2, padx=4, pady=4)

        btn_open_local = ttk.Button(
            tab_local, text="Mở Repository", command=self._open_local_repo
        )
        btn_open_local.grid(row=0, column=3, padx=4, pady=4)

        # Tab 2: GitHub Clone
        tab_remote = ttk.Frame(notebook, style="Card.TFrame", padding=10)
        notebook.add(tab_remote, text="Clone từ GitHub (Remote)")

        ttk.Label(tab_remote, text="URL GitHub:", style="Card.TLabel").grid(
            row=0, column=0, sticky=tk.W, pady=3
        )
        remote_entry = ttk.Entry(tab_remote, textvariable=self.repo_url_var, width=50)
        remote_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=6, pady=3)
        tab_remote.columnconfigure(1, weight=1)

        ttk.Label(tab_remote, text="Access Token (Repo Private):", style="Card.TLabel").grid(
            row=1, column=0, sticky=tk.W, pady=3
        )
        token_entry = ttk.Entry(tab_remote, textvariable=self.token_var, show="*", width=50)
        token_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=6, pady=3)

        self.btn_clone = ttk.Button(
            tab_remote, text="Clone Repository", command=self._clone_remote_repo
        )
        self.btn_clone.grid(row=0, column=2, rowspan=2, padx=6, pady=3, sticky=(tk.N, tk.S))

    def _build_control_section(self, parent):
        ctrl_card = ttk.Frame(parent, style="Card.TFrame", padding=(12, 10))
        ctrl_card.pack(fill=tk.X, pady=(0, 8))

        lbl_sec = ttk.Label(
            ctrl_card, text="2. Tùy chọn So sánh & Thư mục Xuất", style="Section.TLabel"
        )
        lbl_sec.pack(anchor=tk.W, pady=(0, 6))

        # Dòng 1: Chế độ so sánh
        mode_box = ttk.Frame(ctrl_card, style="Card.TFrame")
        mode_box.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(mode_box, text="Chế độ:", style="Card.TLabel", font=(CleanLightTheme.FONT_FAMILY, 9, "bold")).pack(
            side=tk.LEFT, padx=(0, 10)
        )
        ttk.Radiobutton(
            mode_box,
            text="So sánh giữa 2 Nhánh (Branches)",
            variable=self.compare_mode,
            value="branch",
            command=self._on_mode_change,
        ).pack(side=tk.LEFT, padx=6)
        ttk.Radiobutton(
            mode_box,
            text="So sánh giữa 2 Commit",
            variable=self.compare_mode,
            value="commit",
            command=self._on_mode_change,
        ).pack(side=tk.LEFT, padx=6)

        # Dòng 2: Bộ chọn Base vs Target
        sel_box = ttk.Frame(ctrl_card, style="Card.TFrame")
        sel_box.pack(fill=tk.X, pady=(0, 8))
        sel_box.columnconfigure(1, weight=1)
        sel_box.columnconfigure(3, weight=1)

        ttk.Label(sel_box, text="Bản Trước (Before):", style="Card.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=4
        )
        self.combo_rev1 = ttk.Combobox(
            sel_box, textvariable=self.rev1_var, state="readonly"
        )
        self.combo_rev1.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=6)

        btn_swap = ttk.Button(sel_box, text="⇄ Đổi", width=6, command=self._swap_revisions)
        btn_swap.grid(row=0, column=2, padx=4)

        ttk.Label(sel_box, text="Bản Sau (After):", style="Card.TLabel").grid(
            row=0, column=3, sticky=tk.W, padx=4
        )
        self.combo_rev2 = ttk.Combobox(
            sel_box, textvariable=self.rev2_var, state="readonly"
        )
        self.combo_rev2.grid(row=0, column=4, sticky=(tk.W, tk.E), padx=6)

        self.btn_preview = ttk.Button(
            sel_box, text="Xem trước Diff", command=self._preview_diff
        )
        self.btn_preview.grid(row=0, column=5, padx=(6, 0))

        # Dòng 3: Thư mục đích & Tùy chọn xuất
        out_box = ttk.Frame(ctrl_card, style="Card.TFrame")
        out_box.pack(fill=tk.X, pady=(0, 6))
        out_box.columnconfigure(1, weight=1)

        ttk.Label(out_box, text="Thư mục xuất:", style="Card.TLabel").grid(
            row=0, column=0, sticky=tk.W, padx=4
        )
        entry_out = ttk.Entry(out_box, textvariable=self.target_dir_var)
        entry_out.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=6)

        btn_browse_out = ttk.Button(
            out_box, text="Chọn...", command=self._browse_target_dir
        )
        btn_browse_out.grid(row=0, column=2, padx=4)

        # Dòng 4: Export Mode & Checkboxes & Nút thực hiện
        act_box = ttk.Frame(ctrl_card, style="Card.TFrame")
        act_box.pack(fill=tk.X, pady=(4, 0))

        ttk.Radiobutton(
            act_box,
            text="Chỉ xuất file thay đổi (Khuyên dùng)",
            variable=self.export_mode_var,
            value="changed_only",
        ).pack(side=tk.LEFT, padx=4)

        ttk.Radiobutton(
            act_box,
            text="Xuất toàn bộ snapshot",
            variable=self.export_mode_var,
            value="full_snapshot",
        ).pack(side=tk.LEFT, padx=10)

        ttk.Checkbutton(
            act_box, text="Tạo patch (.patch)", variable=self.gen_patch_var
        ).pack(side=tk.LEFT, padx=6)

        ttk.Checkbutton(
            act_box, text="Báo cáo tóm tắt (.md/.json)", variable=self.gen_summary_var
        ).pack(side=tk.LEFT, padx=6)

        self.btn_export = ttk.Button(
            act_box,
            text="So sánh & Xuất Thư mục",
            style="Primary.TButton",
            command=self._start_export,
        )
        self.btn_export.pack(side=tk.RIGHT, padx=4)

    def _build_viewer_section(self, parent):
        # Viewer nhúng
        self.diff_viewer = DiffViewerFrame(parent, self.git_service)
        self.diff_viewer.pack(fill=tk.BOTH, expand=True, pady=(0, 6))

    def _build_footer(self, parent):
        footer = ttk.Frame(parent, style="TFrame")
        footer.pack(fill=tk.X)

        self.progress = ttk.Progressbar(footer, mode="indeterminate", style="Horizontal.TProgressbar")
        self.progress.pack(fill=tk.X, pady=(0, 4))

        status_lbl = ttk.Label(
            footer,
            textvariable=self.status_var,
            style="Status.TLabel",
        )
        status_lbl.pack(side=tk.LEFT)

    def _try_load_initial_repo(self):
        """Khởi động: tự động nạp repository hiện tại nếu có"""
        current_dir = os.path.abspath(".")
        if os.path.exists(os.path.join(current_dir, ".git")):
            try:
                self._load_local_repo_path(current_dir)
            except Exception:
                pass

    def _browse_local_repo(self):
        directory = filedialog.askdirectory(title="Chọn thư mục Git Repository")
        if directory:
            self.local_path_var.set(directory)
            self._load_local_repo_path(directory)

    def _open_local_repo(self):
        path = self.local_path_var.get().strip()
        if not path or not os.path.isdir(path):
            messagebox.showerror("Lỗi", "Đường dẫn thư mục không hợp lệ")
            return
        self._load_local_repo_path(path)

    def _load_local_repo_path(self, path: str):
        try:
            self.git_service.open_local_repository(path)
            repo_name = os.path.basename(os.path.abspath(path))
            self.repo_status_var.set(f"🟢 Local: {repo_name}")
            self.status_var.set(f"Đã mở repository: {repo_name}")
            self._refresh_branches_and_commits()
        except Exception as err:
            messagebox.showerror("Lỗi", f"Không thể mở repository:\n{err}")

    def _clone_remote_repo(self):
        url = self.repo_url_var.get().strip()
        token = self.token_var.get().strip()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL GitHub")
            return

        self.btn_clone.config(state="disabled")
        self.progress.start(10)
        self.status_var.set("Đang clone repository...")

        def worker():
            try:
                timeout = self.config_mgr.get("git_settings", "clone_timeout", 300)
                self.git_service.clone_remote_repository(
                    url=url,
                    token=token,
                    timeout=timeout,
                    progress_callback=lambda msg: self.root.after(0, lambda: self.status_var.set(msg)),
                )
                repo_name = url.rstrip("/").split("/")[-1].replace(".git", "")
                self.root.after(0, lambda: self._on_clone_success(repo_name))
            except Exception as err:
                self.root.after(0, lambda: self._on_clone_error(str(err)))

        threading.Thread(target=worker, daemon=True).start()

    def _on_clone_success(self, repo_name: str):
        self.progress.stop()
        self.btn_clone.config(state="normal")
        self.repo_status_var.set(f"🌐 Remote: {repo_name}")
        self.status_var.set(f"Clone thành công: {repo_name}")
        self._refresh_branches_and_commits()
        messagebox.showinfo("Thành công", f"Đã clone thành công repository {repo_name}!")

    def _on_clone_error(self, err_msg: str):
        self.progress.stop()
        self.btn_clone.config(state="normal")
        self.status_var.set("Clone thất bại")
        messagebox.showerror("Lỗi Clone", f"Không thể clone repository:\n{err_msg}")

    def _refresh_branches_and_commits(self):
        """Tải lại danh sách nhánh và commit"""
        if not self.git_service.repo:
            return

        self.branches = self.git_service.get_branches()
        max_c = self.config_mgr.get("app_settings", "max_commits", 50)
        self.commits = self.git_service.get_recent_commits(max_count=max_c)

        self._populate_combos()

    def _populate_combos(self):
        mode = self.compare_mode.get()
        if mode == "branch":
            values = self.branches
            self.combo_rev1["values"] = values
            self.combo_rev2["values"] = values

            if values:
                self.rev1_var.set(values[0])
                self.rev2_var.set(values[1] if len(values) > 1 else values[0])
        else:
            commit_displays = [c.display_text() for c in self.commits]
            self.combo_rev1["values"] = commit_displays
            self.combo_rev2["values"] = commit_displays

            if self.commits:
                # Mặc định commit 1 là commit áp chót, commit 2 là commit mới nhất
                if len(self.commits) > 1:
                    self.rev1_var.set(commit_displays[1])
                    self.rev2_var.set(commit_displays[0])
                else:
                    self.rev1_var.set(commit_displays[0])
                    self.rev2_var.set(commit_displays[0])

    def _on_mode_change(self):
        self._populate_combos()

    def _swap_revisions(self):
        v1 = self.rev1_var.get()
        v2 = self.rev2_var.get()
        self.rev1_var.set(v2)
        self.rev2_var.set(v1)

    def _get_selected_revisions(self) -> tuple[str, str]:
        """Trích xuất mã revision (branch name hoặc commit hash) sạch"""
        mode = self.compare_mode.get()
        raw1 = self.rev1_var.get().strip()
        raw2 = self.rev2_var.get().strip()

        if mode == "branch":
            return raw1, raw2
        else:
            h1 = raw1.split(" - ")[0].strip() if " - " in raw1 else raw1
            h2 = raw2.split(" - ")[0].strip() if " - " in raw2 else raw2
            return h1, h2

    def _preview_diff(self):
        """Chỉ xem trước diff trong giao diện mà không cần xuất ra ổ đĩa"""
        if not self.git_service.repo:
            messagebox.showwarning("Thông báo", "Vui lòng mở hoặc clone một repository trước.")
            return

        r1, r2 = self._get_selected_revisions()
        if not r1 or not r2:
            messagebox.showwarning("Thông báo", "Vui lòng chọn 2 phiên bản để so sánh.")
            return

        self.status_var.set("Đang phân tích thay đổi...")
        self.progress.start(10)

        def worker():
            try:
                diff_items = self.git_service.get_diff_file_list(r1, r2)
                self.root.after(
                    0,
                    lambda: (
                        self.progress.stop(),
                        self.diff_viewer.update_diff_data(
                            r1, r2, self.target_dir_var.get(), diff_items
                        ),
                        self.status_var.set(
                            f"Đã phân tích xong: {len(diff_items)} file thay đổi giữa {r1} và {r2}"
                        ),
                    ),
                )
            except Exception as err:
                self.root.after(
                    0,
                    lambda: (
                        self.progress.stop(),
                        self.status_var.set("Lỗi phân tích diff"),
                        messagebox.showerror("Lỗi", f"Không thể lấy diff:\n{err}"),
                    ),
                )

        threading.Thread(target=worker, daemon=True).start()

    def _browse_target_dir(self):
        d = filedialog.askdirectory(title="Chọn thư mục lưu kết quả diff")
        if d:
            self.target_dir_var.set(d)

    def _start_export(self):
        """Bắt đầu xuất các file diff vào before/ và after/"""
        if not self.git_service.repo:
            messagebox.showwarning("Thông báo", "Vui lòng mở hoặc clone một repository trước.")
            return

        r1, r2 = self._get_selected_revisions()
        if not r1 or not r2:
            messagebox.showwarning("Thông báo", "Vui lòng chọn 2 phiên bản để so sánh.")
            return

        target_dir = self.target_dir_var.get().strip()
        if not target_dir:
            messagebox.showwarning("Thông báo", "Vui lòng chọn thư mục lưu kết quả.")
            return

        mode = self.export_mode_var.get()
        gen_patch = self.gen_patch_var.get()
        gen_summary = self.gen_summary_var.get()

        self.btn_export.config(state="disabled")
        self.status_var.set("Đang tiến hành xuất file diff...")
        self.progress.start(10)

        def worker():
            res: ExportResult = self.diff_exporter.export(
                rev1=r1,
                rev2=r2,
                target_dir=target_dir,
                mode=mode,
                generate_patch=gen_patch,
                generate_summary=gen_summary,
                progress_callback=lambda cur, tot, fn: self.root.after(
                    0, lambda: self.status_var.set(f"Đang xuất [{cur}/{tot}]: {fn}")
                ),
            )
            self.root.after(0, lambda: self._on_export_finished(res, r1, r2))

        threading.Thread(target=worker, daemon=True).start()

    def _on_export_finished(self, res: ExportResult, r1: str, r2: str):
        self.progress.stop()
        self.btn_export.config(state="normal")

        if res.success:
            self.status_var.set(
                f"Xuất hoàn tất! {res.total_files_changed} file vào {res.target_dir}"
            )
            # Cập nhật luôn diff viewer
            self.diff_viewer.update_diff_data(r1, r2, res.target_dir)

            msg = (
                f"Đã xuất diff thành công!\n\n"
                f"- Số file thay đổi: {res.total_files_changed}\n"
                f"- Thư mục Trước (before): {res.before_dir}\n"
                f"- Thư mục Sau (after): {res.after_dir}\n"
            )
            if res.patch_file:
                msg += f"- File Patch: {res.patch_file}\n"
            if res.summary_file:
                msg += f"- Báo cáo: {res.summary_file}\n"

            messagebox.showinfo("Xuất Thành công", msg)
        else:
            self.status_var.set("Xuất diff thất bại")
            messagebox.showerror("Lỗi", f"Không thể xuất diff:\n{res.error_message}")

    def cleanup(self):
        """Dọn dẹp thư mục tạm khi đóng ứng dụng"""
        auto_cleanup = self.config_mgr.get("ui_settings", "auto_cleanup", True)
        if auto_cleanup:
            self.git_service.cleanup_temp_if_needed()
