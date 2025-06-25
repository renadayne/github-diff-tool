import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import tempfile
import threading
from git import Repo
import requests
import json

class GitDiffTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Git Diff Tool - Công cụ so sánh Git")
        self.root.geometry("600x500")
        
        # Biến lưu trữ
        self.repo = None
        self.temp_dir = None
        self.branches = []
        self.commits = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Cấu hình grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 1. GitHub Repository URL
        ttk.Label(main_frame, text="GitHub Repository URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.repo_url_var = tk.StringVar()
        self.repo_entry = ttk.Entry(main_frame, textvariable=self.repo_url_var, width=50)
        self.repo_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 2. Authentication (nếu cần)
        ttk.Label(main_frame, text="Personal Access Token (nếu repo private):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.token_var = tk.StringVar()
        self.token_entry = ttk.Entry(main_frame, textvariable=self.token_var, show="*", width=50)
        self.token_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 3. Nút Clone
        self.clone_btn = ttk.Button(main_frame, text="Clone Repository", command=self.clone_repository)
        self.clone_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # 4. Chế độ so sánh
        ttk.Label(main_frame, text="Chế độ so sánh:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.compare_mode = tk.StringVar(value="branch")
        mode_frame = ttk.Frame(main_frame)
        mode_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        ttk.Radiobutton(mode_frame, text="So sánh 2 branch", variable=self.compare_mode, 
                       value="branch", command=self.on_mode_change).pack(side=tk.LEFT)
        ttk.Radiobutton(mode_frame, text="So sánh 2 commit gần nhất", variable=self.compare_mode, 
                       value="commit", command=self.on_mode_change).pack(side=tk.LEFT, padx=(10, 0))
        
        # 5. Lựa chọn branch/commit
        # Branch 1
        ttk.Label(main_frame, text="Branch/Commit 1:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.branch1_var = tk.StringVar()
        self.branch1_combo = ttk.Combobox(main_frame, textvariable=self.branch1_var, state="readonly", width=47)
        self.branch1_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Branch 2
        ttk.Label(main_frame, text="Branch/Commit 2:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.branch2_var = tk.StringVar()
        self.branch2_combo = ttk.Combobox(main_frame, textvariable=self.branch2_var, state="readonly", width=47)
        self.branch2_combo.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 6. Thư mục đích
        ttk.Label(main_frame, text="Thư mục đích:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.target_dir_var = tk.StringVar()
        target_frame = ttk.Frame(main_frame)
        target_frame.grid(row=6, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        self.target_entry = ttk.Entry(target_frame, textvariable=self.target_dir_var, width=35)
        self.target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_btn = ttk.Button(target_frame, text="Browse", command=self.browse_target_dir)
        self.browse_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 7. Nút Compare
        self.compare_btn = ttk.Button(main_frame, text="So sánh và Tạo Diff", command=self.compare_and_create_diff)
        self.compare_btn.grid(row=7, column=0, columnspan=2, pady=20)
        
        # 8. Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 9. Status label
        self.status_var = tk.StringVar(value="Sẵn sàng")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=5)
        
        # Vô hiệu hóa các control ban đầu
        self.set_controls_state(False)
    
    def set_controls_state(self, enabled):
        """Bật/tắt các control dựa trên trạng thái"""
        state = "normal" if enabled else "disabled"
        self.branch1_combo.config(state=state)
        self.branch2_combo.config(state=state)
        self.browse_btn.config(state=state)
        self.compare_btn.config(state=state)
    
    def on_mode_change(self):
        """Xử lý khi thay đổi chế độ so sánh"""
        if self.repo:
            self.update_branch_commit_lists()
    
    def clone_repository(self):
        """Clone repository từ GitHub"""
        url = self.repo_url_var.get().strip()
        if not url:
            messagebox.showerror("Lỗi", "Vui lòng nhập URL repository")
            return
        
        # Tạo thư mục tạm
        self.temp_dir = tempfile.mkdtemp(prefix="gitdiff_")
        
        # Chạy clone trong thread riêng
        thread = threading.Thread(target=self._clone_repository_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _clone_repository_thread(self, url):
        """Thread để clone repository"""
        try:
            self.root.after(0, lambda: self.status_var.set("Đang clone repository..."))
            self.root.after(0, self.progress.start)
            
            # Xử lý URL và token
            if self.token_var.get().strip():
                # Thêm token vào URL
                token = self.token_var.get().strip()
                if "github.com" in url:
                    url = url.replace("https://github.com", f"https://{token}@github.com")
            
            # Clone repository
            self.repo = Repo.clone_from(url, self.temp_dir)
            
            # Cập nhật UI
            self.root.after(0, self._on_clone_success)
            
        except Exception as e:
            self.root.after(0, lambda: self._on_clone_error(str(e)))
    
    def _on_clone_success(self):
        """Xử lý khi clone thành công"""
        self.progress.stop()
        self.status_var.set("Clone thành công! Đang tải danh sách branch/commit...")
        
        # Cập nhật danh sách branch và commit
        self.update_branch_commit_lists()
        
        # Bật các control
        self.set_controls_state(True)
        
        messagebox.showinfo("Thành công", "Repository đã được clone thành công!")
    
    def _on_clone_error(self, error_msg):
        """Xử lý khi clone thất bại"""
        self.progress.stop()
        self.status_var.set("Clone thất bại")
        messagebox.showerror("Lỗi Clone", f"Không thể clone repository:\n{error_msg}")
        
        # Dọn dẹp thư mục tạm
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def update_branch_commit_lists(self):
        """Cập nhật danh sách branch và commit"""
        if not self.repo:
            return
        
        try:
            # Lấy danh sách branch
            self.branches = [ref.name for ref in self.repo.references if ref.name.startswith('origin/')]
            self.branches = [branch.replace('origin/', '') for branch in self.branches]
            
            # Lấy danh sách commit (10 commit gần nhất)
            self.commits = []
            for commit in self.repo.iter_commits('HEAD', max_count=10):
                msg = commit.message.split('\n')[0]
                self.commits.append(f"{commit.hexsha[:8]} - {msg}")
            
            # Cập nhật combobox
            if self.compare_mode.get() == "branch":
                self.branch1_combo['values'] = self.branches
                self.branch2_combo['values'] = self.branches
                if self.branches:
                    self.branch1_var.set(self.branches[0])
                    self.branch2_var.set(self.branches[1] if len(self.branches) > 1 else self.branches[0])
            else:
                self.branch1_combo['values'] = self.commits
                self.branch2_combo['values'] = self.commits
                if self.commits:
                    self.branch1_var.set(self.commits[0])
                    self.branch2_var.set(self.commits[1] if len(self.commits) > 1 else self.commits[0])
            
            self.status_var.set("Sẵn sàng so sánh")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách branch/commit:\n{str(e)}")
    
    def browse_target_dir(self):
        """Chọn thư mục đích"""
        directory = filedialog.askdirectory(title="Chọn thư mục đích")
        if directory:
            self.target_dir_var.set(directory)
    
    def compare_and_create_diff(self):
        """So sánh và tạo diff"""
        # Kiểm tra dữ liệu đầu vào
        if not self.repo:
            messagebox.showerror("Lỗi", "Chưa clone repository")
            return
        
        if not self.branch1_var.get() or not self.branch2_var.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn 2 branch/commit để so sánh")
            return
        
        if not self.target_dir_var.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục đích")
            return
        
        # Chạy trong thread riêng
        thread = threading.Thread(target=self._compare_thread)
        thread.daemon = True
        thread.start()
    
    def _compare_thread(self):
        """Thread để thực hiện so sánh"""
        try:
            self.root.after(0, lambda: self.status_var.set("Đang so sánh..."))
            self.root.after(0, self.progress.start)
            
            target_dir = self.target_dir_var.get()
            mode = self.compare_mode.get()
            
            # Tạo thư mục before và after
            before_dir = os.path.join(target_dir, "before")
            after_dir = os.path.join(target_dir, "after")
            
            # Xóa thư mục cũ nếu có
            if os.path.exists(before_dir):
                shutil.rmtree(before_dir)
            if os.path.exists(after_dir):
                shutil.rmtree(after_dir)
            
            # Tạo thư mục mới
            os.makedirs(before_dir)
            os.makedirs(after_dir)
            
            # Lấy thông tin branch/commit
            if mode == "branch":
                branch1 = self.branch1_var.get()
                branch2 = self.branch2_var.get()
                
                # Checkout branch 1 và copy vào before
                self.repo.git.checkout(branch1)
                self._copy_repo_to_dir(before_dir)
                
                # Checkout branch 2 và copy vào after
                self.repo.git.checkout(branch2)
                self._copy_repo_to_dir(after_dir)
                
            else:  # commit mode
                commit1 = self.branch1_var.get().split(" - ")[0]
                commit2 = self.branch2_var.get().split(" - ")[0]
                
                # Checkout commit 1 và copy vào before
                self.repo.git.checkout(commit1)
                self._copy_repo_to_dir(before_dir)
                
                # Checkout commit 2 và copy vào after
                self.repo.git.checkout(commit2)
                self._copy_repo_to_dir(after_dir)
            
            # Hoàn thành
            self.root.after(0, lambda: self._on_compare_success(before_dir, after_dir))
            
        except Exception as e:
            self.root.after(0, lambda: self._on_compare_error(str(e)))
    
    def _copy_repo_to_dir(self, target_dir):
        """Copy toàn bộ repo (trừ .git) vào thư mục đích"""
        for item in os.listdir(self.temp_dir):
            source = os.path.join(self.temp_dir, item)
            destination = os.path.join(target_dir, item)
            
            if item != '.git':
                if os.path.isdir(source):
                    shutil.copytree(source, destination)
                else:
                    shutil.copy2(source, destination)
    
    def _on_compare_success(self, before_dir, after_dir):
        """Xử lý khi so sánh thành công"""
        self.progress.stop()
        self.status_var.set("So sánh hoàn thành!")
        
        messagebox.showinfo("Thành công", 
                          f"Đã tạo diff thành công!\n\n"
                          f"Thư mục 'before': {before_dir}\n"
                          f"Thư mục 'after': {after_dir}\n\n"
                          f"Bạn có thể so sánh 2 thư mục này để xem sự khác biệt.")
    
    def _on_compare_error(self, error_msg):
        """Xử lý khi so sánh thất bại"""
        self.progress.stop()
        self.status_var.set("So sánh thất bại")
        messagebox.showerror("Lỗi So sánh", f"Không thể thực hiện so sánh:\n{error_msg}")
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except:
                pass

def main():
    root = tk.Tk()
    app = GitDiffTool(root)
    
    # Xử lý khi đóng ứng dụng
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main() 