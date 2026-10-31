# Kế hoạch Đại tu & Nâng cấp Git Diff Tool (Master Execution Plan)

## 1. Hiện trạng & Các vấn đề tồn đọng

### A. Vấn đề chức năng (Core & Logic)
- **Thiếu cơ chế tự động tìm Git executable**: Trên Windows, nếu Git không nằm trong `PATH` mặc định (ví dụ cài ở `D:\Software\Git\Git\cmd\git.exe`), thư viện `gitpython` sẽ lập tức crash khi khởi động hoặc chạy lệnh.
- **Bắt buộc clone lại repo**: Tool hiện tại chỉ cho phép nhập URL GitHub và clone mới. Không hỗ trợ chọn Repository có sẵn trên máy (Local Repo), gây tốn thời gian, băng thông và không thuận tiện cho developer.
- **Diff logic không tối ưu (Copy toàn bộ thư mục)**: Hàm export hiện tại copy **toàn bộ mã nguồn** của branch/commit vào `before/` và `after/` (kể cả hàng chục nghìn file không thay đổi), thay vì chỉ trích xuất các file có sự thay đổi (modified/added/deleted).
- **Lỗi xử lý Git References**:
  - `origin/HEAD` bị sót lại trong danh sách branch gây lỗi khi checkout.
  - Checkout branch từ remote có thể gây xung đột hoặc detach HEAD nếu không xử lý track branch.
  - Commit chỉ hardcode lấy 10 commit gần nhất trên HEAD mà không tìm kiếm hoặc lọc theo branch.
- **File cấu hình `config.json` bị bỏ quên**: File có sẵn trong repo nhưng không bao giờ được load hoặc lưu trữ trong `git_diff_tool.py`.

### B. Vấn đề Giao diện (UI/UX)
- Giao diện Tkinter mặc định kiểu cổ điển (Windows 95/2000 style xám xịt), khoảng cách ô chật chội, layout đơn điệu dồn vào một lưới không có phân cấp.
- **Thiếu tính năng cốt lõi của một Diff Tool**: Ứng dụng không có giao diện xem trước sự khác biệt (Diff Preview)! Người dùng ấn nút thì chỉ hiện ra một hộp thoại thông báo đã copy vào ổ đĩa. Không có danh sách file thay đổi, không có thống kê `+` / `-`, không có viewer tô màu syntax diff.
- Thiếu các thao tác nhanh: Nút mở nhanh folder `before`, folder `after`, hoặc mở diff trực tiếp trong VS Code / Cursor / WinMerge.

### C. Vấn đề Tài liệu (AI Slop trong README)
- Tràn ngập emoji rác (`🎯`, `📋`, `🚀`, `💻`, `📁`, `🔧`, `🛠`, `⚠️`, `🐛`, `🤝`, `📄`) ở mọi tiêu đề và bullet point.
- Câu từ sáo rỗng, mô tả chung chung như tài liệu do bot tự động sinh ra, thiếu tính chuyên nghiệp của một công cụ dev tool chất lượng cao.

---

## 2. Kiến trúc Module Mới (Tối ưu Token & Phân tán Context)

Thay vì dồn toàn bộ 500-1000 dòng code vào một file `git_diff_tool.py` duy nhất (khiến mỗi lần agent đọc/sửa tốn nhiều token), dự án sẽ được chia nhỏ thành các module độc lập:

```
github-diff-tool/
├── core/
│   ├── __init__.py
│   ├── git_finder.py      # Tự động quét và phát hiện git.exe trên Windows/Linux/macOS
│   ├── git_service.py     # Thao tác Git: Local repo, clone remote, lấy branches/commits, git diff
│   ├── diff_exporter.py   # Export các file thay đổi vào before/after, tạo diff.patch & summary
│   └── config_manager.py  # Đọc, ghi và validate cấu hình từ config.json
├── ui/
│   ├── __init__.py
│   ├── theme.py           # Design system: Bảng màu hiện đại (Dark Slate / Clean Light), ttk.Style
│   ├── components.py      # Các widget dùng lại: Thẻ card, badge pill, thanh tìm kiếm, file tree
│   ├── diff_viewer.py     # Cửa sổ / khung preview diff màu sắc (+ xanh, - đỏ), thống kê thay đổi
│   └── main_window.py     # Layout ứng dụng chính, kết nối các luồng xử lý đa luồng
├── git_diff_tool.py       # Entry point tối giản gọi UI và Core
├── run.py                 # Runner thông minh kiểm tra môi trường và khởi chạy
├── config.json            # Cấu hình chuẩn hóa
├── requirements.txt       # Dependencies tinh gọn
└── README.md              # Tài liệu kỹ thuật chuyên nghiệp, loại bỏ sạch AI slop
```

---

## 3. Lộ trình Triển khai & Chia nhỏ Task (Execution Steps)

Mỗi task là một context độc lập, có phạm vi hẹp. **Sau mỗi task con hoàn thành và kiểm thử, tiến hành git commit và git push lên GitHub**.

### Giai đoạn 1: Thiết lập Nền tảng & Cấu trúc Module
- [x] **Task 1.1: Cập nhật môi trường & .gitignore**
  - Cập nhật `.gitignore` để bỏ qua `.venv/`, thư mục test diff tạm, file rác.
  - Tạo `core/git_finder.py` tự động nhận diện `git.exe` ở các thư mục cài đặt đặc thù (như `D:\Software\Git\Git\cmd\git.exe`, Program Files, AppData, Registry) và gán `GIT_PYTHON_GIT_EXECUTABLE`.
  - *Kiểm thử & Git commit + Push GitHub.*
- [x] **Task 1.2: Module hóa Quản lý Cấu hình (`core/config_manager.py`)**
  - Tạo lớp `ConfigManager` quản lý load/save `config.json` với fallback mặc định an toàn.
  - Bổ sung cấu hình: export mode (chỉ file đổi vs toàn bộ repo), theme (dark/light), ignore patterns, external diff viewer (VS Code).
  - *Kiểm thử & Git commit + Push GitHub.*

### Giai đoạn 2: Xây dựng Core Git Engine & Diff Exporter
- [x] **Task 2.1: Hoàn thiện `core/git_service.py`**
  - Hỗ trợ 2 chế độ mở repo:
    1. **Local Repository**: Mở ngay thư mục Git trên máy tính không cần clone.
    2. **Remote Clone**: Clone từ GitHub (hỗ trợ PAT token an toàn, timeout, tắt terminal prompt để tránh treo).
  - Trích xuất danh sách branches sạch (loại bỏ `origin/HEAD`, chuẩn hóa tên branch local & remote).
  - Trích xuất danh sách commits linh hoạt (hash, tác giả, thời gian, commit message, hỗ trợ phân trang/tìm kiếm).
  - Phân tích diff giữa 2 revision bằng Git Engine: trả về danh sách file thay đổi kèm trạng thái (A: Thêm mới, M: Sửa đổi, D: Xóa, R: Đổi tên) và số dòng +/-.
  - *Kiểm thử độc lập với script & Git commit + Push GitHub.*
- [x] **Task 2.2: Hoàn thiện `core/diff_exporter.py`**
  - Hàm xuất file diff:
    - Chế độ 1 (**Khuyên dùng - Changed Files Only**): Chỉ trích xuất các file thay đổi vào `before/` và `after/` theo đúng cấu trúc thư mục con tương đối.
    - Chế độ 2 (**Full Tree Snapshot**): Trích xuất toàn bộ dự án nếu người dùng có nhu cầu.
    - Tạo file `changes.patch` chuẩn unified diff và file `diff_summary.json` / `diff_summary.md`.
  - *Kiểm thử & Git commit + Push GitHub.*

### Giai đoạn 3: Thiết kế Lại Toàn diện Giao diện (UI/UX)
- [ ] **Task 3.1: Hệ thống Giao diện & Design System (`ui/theme.py`)**
  - Tạo theme hiện đại trên nền `ttk.Style` với bảng màu slate cao cấp (`#0f172a`, `#1e293b`, `#3b82f6`, `#10b981`, `#ef4444`).
  - Typography tối ưu cho Windows (Segoe UI), bo góc nhẹ, padding thoáng đãng, phân tách thẻ card rõ ràng.
  - Hỗ trợ chuyển đổi Dark Mode / Light Mode.
  - *Kiểm thử visual & Git commit + Push GitHub.*
- [ ] **Task 3.2: Giao diện Chính (`ui/main_window.py`)**
  - Thiết kế layout 2 tab nguồn: "Local Git Repo" và "Clone GitHub".
  - Bộ chọn phiên bản (Source vs Target: Branch hoặc Commit) có dropdown tìm kiếm nhanh.
  - Tùy chọn xuất file: Chọn thư mục lưu, chọn chế độ (chỉ file đổi hay toàn bộ repo), nút mở nhanh thư mục.
  - Thanh tiến trình thực tế, nhãn trạng thái và xử lý background thread mượt mà.
  - *Kiểm thử & Git commit + Push GitHub.*
- [ ] **Task 3.3: Khung Xem & So sánh Diff Ngay Trong Ứng dụng (`ui/diff_viewer.py`)**
  - Tích hợp khung Split View:
    - Bên trái: Bảng danh sách các file thay đổi (có icon/tag: Added, Modified, Deleted) cùng số dòng thay đổi.
    - Bên phải: Trình xem Unified Diff với màu sắc trực quan (dòng thêm nền xanh, dòng xóa nền đỏ, số dòng rõ ràng).
  - Nút tiện ích: "Mở trong VS Code" (`code -d before/file after/file`), "Mở Explorer", "Copy Patch".
  - *Kiểm thử & Git commit + Push GitHub.*
- [ ] **Task 3.4: Nối Entry Points & Đóng gói Runner**
  - Cập nhật `git_diff_tool.py` và `run.py` trỏ đến cấu trúc mới.
  - Tự động kiểm tra môi trường, hướng dẫn cài đặt nếu thiếu thư viện.
  - *Kiểm thử khởi chạy toàn diện & Git commit + Push GitHub.*

### Giai đoạn 4: Viết Lại Tài Liệu (Khử Sạch AI Slop)
- [ ] **Task 4.1: Viết lại `README.md` theo phong cách Open-source chuyên nghiệp**
  - Xóa sạch emoji thừa thãi, rườm rà.
  - Cấu trúc chuẩn: Giới thiệu ngắn gọn, Tính năng chính, Hướng dẫn cài đặt, Hướng dẫn sử dụng nhanh qua GUI, Bảng cấu hình `config.json`, Phím tắt/CLI, Giấy phép.
  - Ngôn từ kỹ thuật súc tích, mạch lạc.
- [ ] **Task 4.2: Chuẩn hóa `USAGE_GUIDE.md` và `PACKAGING_GUIDE.md`**
  - Cập nhật hướng dẫn khớp với UI mới.
  - Hướng dẫn build file exe bằng PyInstaller với cấu trúc module mới.
  - *Kiểm thử & Git commit + Push GitHub.*

---

## 4. Quy ước Git & Push GitHub cho từng Task

- **Cấu hình Git**: Sử dụng đường dẫn Git executable đã nhận diện (`D:\Software\Git\Git\cmd\git.exe`).
- **Format Commit Message**: Tuân thủ [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat(core): implement automatic git executable detection on windows`
  - `feat(core): implement git service for local and remote repositories`
  - `feat(core): implement selective changed-files diff exporter`
  - `feat(ui): add modern slate theme and responsive ttk styles`
  - `feat(ui): implement in-app diff viewer and changed files tree`
  - `docs: rewrite readme to remove ai slop and document new architecture`
- **Lệnh thực thi**:
  ```powershell
  & "D:\Software\Git\Git\cmd\git.exe" add <files>
  & "D:\Software\Git\Git\cmd\git.exe" commit -m "<message>"
  & "D:\Software\Git\Git\cmd\git.exe" push origin main
  ```
