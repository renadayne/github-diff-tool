# Git Diff Tool

Git Diff Tool là công cụ GUI trực quan được thiết kế để phân tích, so sánh sự khác biệt giữa các nhánh (branches) hoặc commit trong Git repository và tự động trích xuất các file thay đổi vào hai thư mục `before/` và `after/`.

Ứng dụng hỗ trợ cả thư mục Git cục bộ (Local Repo) lẫn kho lưu trữ từ xa trên GitHub (hỗ trợ Personal Access Token cho kho lưu trữ riêng tư).

---

## Tính năng chính

- **Mở kho lưu trữ linh hoạt**:
  - Hỗ trợ mở trực tiếp thư mục Git có sẵn trên máy mà không cần clone lại.
  - Hỗ trợ clone từ GitHub với chế độ bảo vệ token và cơ chế chống treo tiến trình.
- **Trích xuất Diff thông minh (Changed Files Only)**:
  - Chỉ trích xuất các file có thay đổi (Added, Modified, Deleted, Renamed) vào thư mục `before/` và `after/`, giữ nguyên cấu trúc thư mục phân cấp tương đối.
  - Hỗ trợ tùy chọn trích xuất toàn bộ snapshot kho mã nguồn khi cần.
  - Tự động tạo file `changes.patch` chuẩn unified diff và báo cáo tóm tắt (`diff_summary.md`, `diff_summary.json`).
- **Trình xem Diff tích hợp (In-app Diff Viewer)**:
  - Bảng danh sách file thay đổi kèm thống kê số dòng thêm/xóa (`+` / `-`).
  - Khung xem nội dung unified diff trực tiếp với màu sắc trực quan (dòng thêm nền xanh, dòng xóa nền đỏ).
  - Tích hợp phím tắt mở file trực tiếp trong Visual Studio Code (`code --diff`) hoặc mở thư mục trong File Explorer.
- **Tự động nhận diện Git trên Windows**:
  - Tự động quét và phát hiện các đường dẫn cài đặt Git phổ biến (`Program Files`, `D:\Software\Git`, `AppData`, Registry), giải quyết lỗi thiếu Git trong `PATH` hệ thống.
- **Giao diện Clean Light hiện đại**:
  - Thiết kế tối giản, phân cấp rõ ràng theo khối thẻ (cards), phông chữ Segoe UI sắc nét, không phụ thuộc vào các thư viện giao diện nặng nề.

---

## Cấu trúc dự án

```text
github-diff-tool/
├── core/
│   ├── git_finder.py       # Tự động phát hiện git.exe và cấu hình môi trường
│   ├── git_service.py      # Git Engine: xử lý local/remote repo, branches, commits, diff
│   ├── diff_exporter.py    # Trích xuất file thay đổi vào before/after, tạo patch và báo cáo
│   └── config_manager.py   # Quản lý cấu hình tập trung từ config.json
├── ui/
│   ├── theme.py            # Bảng màu Clean Light và cấu hình ttk.Style
│   ├── diff_viewer.py      # Component xem diff tô màu và danh sách file thay đổi
│   └── main_window.py      # Cửa sổ chính và điều phối đa luồng
├── git_diff_tool.py        # Entry point chính của ứng dụng
├── run.py                  # Script khởi chạy có kiểm tra môi trường
├── config.json             # File cấu hình ứng dụng
├── requirements.txt        # Danh sách thư viện phụ thuộc
└── README.md               # Tài liệu dự án
```

---

## Yêu cầu hệ thống

- Python 3.10 trở lên
- Git (đã cài đặt trên máy)
- Hệ điều hành: Windows 10/11, Linux, hoặc macOS

---

## Cài đặt

1. Clone kho mã nguồn:
   ```bash
   git clone https://github.com/renadayne/github-diff-tool.git
   cd github-diff-tool
   ```

2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

---

## Hướng dẫn sử dụng

### Khởi chạy ứng dụng

```bash
python run.py
```

Hoặc trên Windows:
```cmd
run.bat
```

### Quy trình so sánh và xuất Diff

1. **Chọn nguồn Repository**:
   - Tab **Thư mục máy (Local Repo)**: Nhấn *Chọn thư mục...* trỏ đến thư mục dự án Git trên máy, sau đó nhấn *Mở Repository*.
   - Tab **Clone từ GitHub (Remote)**: Nhập URL repository (và Personal Access Token nếu là repo private), sau đó nhấn *Clone Repository*.
2. **Chọn phiên bản so sánh**:
   - Chọn chế độ *So sánh giữa 2 Nhánh* hoặc *So sánh giữa 2 Commit*.
   - Chọn phiên bản gốc (*Bản Trước / Before*) và phiên bản đích (*Bản Sau / After*). Có thể nhấn nút *⇄ Đổi* để đảo ngược chiều so sánh.
   - Nhấn *Xem trước Diff* để xem danh sách file thay đổi và nội dung diff trực tiếp trong ứng dụng.
3. **Xuất file**:
   - Chọn thư mục lưu kết quả (*Thư mục xuất*).
   - Chọn chế độ xuất (*Chỉ xuất file thay đổi* hoặc *Xuất toàn bộ snapshot*).
   - Nhấn *So sánh & Xuất Thư mục*.

### Cấu trúc kết quả sau khi xuất

```text
thư_mục_đích/
├── before/                 # Chứa các file ở phiên bản trước
│   └── src/
│       └── app.py
├── after/                  # Chứa các file ở phiên bản sau
│   └── src/
│       └── app.py
├── changes.patch           # Unified diff patch dùng cho git apply
├── diff_summary.md         # Báo cáo tóm tắt định dạng Markdown
└── diff_summary.json       # Dữ liệu thống kê định dạng JSON
```

---

## Cấu hình (config.json)

Bạn có thể tùy biến hành vi của ứng dụng thông qua file `config.json`:

| Khóa | Mặc định | Mô tả |
| :--- | :--- | :--- |
| `app_settings.window_size` | `"960x700"` | Kích thước khởi động của cửa sổ giao diện |
| `app_settings.max_commits` | `50` | Số lượng commit tối đa tải trong danh sách |
| `app_settings.export_mode` | `"changed_only"` | Chế độ xuất (`"changed_only"` hoặc `"full_snapshot"`) |
| `app_settings.generate_patch` | `true` | Tự động tạo file `changes.patch` |
| `app_settings.generate_summary` | `true` | Tự động tạo báo cáo markdown và JSON |
| `git_settings.clone_timeout` | `300` | Thời gian chờ tối đa khi clone repo (giây) |
| `git_settings.ignore_patterns` | `[...]` | Các mẫu file/thư mục bỏ qua khi quét |
| `ui_settings.theme` | `"clean_light"` | Giao diện hiển thị |
| `ui_settings.auto_cleanup` | `true` | Tự động dọn dẹp thư mục clone tạm khi đóng ứng dụng |

---

## Đóng gói thành file Executable (.exe)

Để đóng gói thành một file thực thi duy nhất trên Windows bằng PyInstaller:

```bash
python setup.py
```

File sau khi biên dịch sẽ nằm tại thư mục `dist/GitDiffTool.exe`.

---

## Giấy phép

Dự án được phân phối theo giấy phép MIT.