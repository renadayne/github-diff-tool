# Hướng dẫn đóng gói Git Diff Tool

Tài liệu này hướng dẫn cách đóng gói Git Diff Tool thành một file thực thi độc lập (`.exe` trên Windows) sử dụng PyInstaller.

---

## Yêu cầu trước khi đóng gói

1. Đã cài đặt Python 3.10 trở lên.
2. Đã cài đặt các gói trong `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
   Gói `pyinstaller` đã được khai báo sẵn trong file này.

---

## Quy trình đóng gói

### 1. Đóng gói tự động qua script

Trên hệ điều hành Windows:
```cmd
build.bat
```

Hoặc chạy trực tiếp qua Python:
```bash
python setup.py
```

### 2. Các thông số cấu hình đóng gói (trong setup.py)

Script `setup.py` tự động thiết lập các cờ tối ưu cho PyInstaller:
- `--onefile`: Đóng gói toàn bộ mã nguồn và dependencies vào 1 file `.exe` duy nhất.
- `--windowed`: Chạy ở chế độ giao diện đồ họa không hiển thị cửa sổ console nền đen.
- `--add-data`: Tự động nhúng file cấu hình `config.json`.
- `--hidden-import`: Khai báo tường minh các module `core` và `ui` để tránh lỗi thiếu module động khi chạy file `.exe`.

---

## Kết quả xuất xưởng

Sau khi lệnh kết thúc thành công, các file thành phẩm sẽ nằm trong thư mục `dist/`:

```text
dist/
├── GitDiffTool.exe          # File thực thi chính của ứng dụng
├── install.bat              # Script cài đặt tiện lợi và tạo shortcut Desktop
├── README.md                # Tài liệu hướng dẫn
├── USAGE_GUIDE.md           # Hướng dẫn sử dụng chi tiết
└── config.json              # File cấu hình mặc định
```

Người dùng có thể sao chép thư mục `dist` sang bất kỳ máy tính Windows nào khác và khởi chạy trực tiếp file `GitDiffTool.exe` mà không cần cài đặt Python.