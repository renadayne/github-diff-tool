# Hướng dẫn đóng gói Git Diff Tool

## 📦 Tổng quan

Dự án này sử dụng PyInstaller để đóng gói thành file executable (.exe) độc lập, không cần cài đặt Python trên máy người dùng.

## 🚀 Cách đóng gói nhanh

### Windows
```bash
# Chạy script build tự động
build.bat
```

### Linux/Mac
```bash
# Cấp quyền thực thi
chmod +x build.sh

# Chạy script build
./build.sh
```

### Thủ công
```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build executable
python setup.py
```

## 📁 Kết quả đóng gói

Sau khi build thành công, bạn sẽ có:

```
dist/
├── GitDiffTool.exe          # File executable chính
├── install.bat              # Script cài đặt tự động
├── README.md                # Tài liệu hướng dẫn
├── USAGE_GUIDE.md           # Hướng dẫn sử dụng chi tiết
├── run.bat                  # Script chạy (Windows)
└── run.sh                   # Script chạy (Linux/Mac)
```

## 🔧 Tùy chỉnh build

### Thêm icon
1. Tạo file `icon.ico` trong thư mục gốc
2. Chạy lại build script
3. Icon sẽ được tự động nhúng vào executable

### Thay đổi tên file
Chỉnh sửa file `setup.py`:
```python
"--name=TenMoi",  # Thay đổi tên executable
```

### Thêm file dữ liệu
Chỉnh sửa file `setup.py`:
```python
"--add-data=file.txt;.",  # Thêm file vào executable
```

## 📦 Phân phối

### Cách 1: Cài đặt tự động
1. Chạy `dist/install.bat`
2. Tool sẽ được cài vào `%USERPROFILE%\GitDiffTool`
3. Shortcut được tạo trên Desktop

### Cách 2: Chạy trực tiếp
1. Copy toàn bộ thư mục `dist/` đến máy đích
2. Chạy `GitDiffTool.exe` trực tiếp

### Cách 3: Tạo installer
Sử dụng công cụ như Inno Setup để tạo installer chuyên nghiệp.

## 🐛 Xử lý lỗi build

### Lỗi "Module not found"
- Kiểm tra `requirements.txt` có đầy đủ thư viện
- Chạy `pip install -r requirements.txt`

### Lỗi "PyInstaller not found"
- Cài đặt PyInstaller: `pip install pyinstaller`

### Lỗi "Permission denied" (Linux/Mac)
- Cấp quyền thực thi: `chmod +x build.sh`

### Executable quá lớn
- Sử dụng `--onefile` thay vì `--onedir`
- Loại bỏ thư viện không cần thiết

## 📊 Kích thước file

- **GitDiffTool.exe**: ~50-100MB (bao gồm Python runtime)
- **Thư mục dist/**: ~150-200MB (bao gồm tài liệu)

## 🔒 Bảo mật

- Executable được tạo không chứa source code gốc
- Personal Access Token không được lưu trữ
- Thư mục tạm được tự động xóa

## 📝 Ghi chú

- Executable chỉ hoạt động trên cùng hệ điều hành build
- Windows build chỉ chạy trên Windows
- Linux build chỉ chạy trên Linux
- Mac build chỉ chạy trên macOS

## 🤝 Đóng góp

Nếu gặp vấn đề khi build, vui lòng:
1. Kiểm tra phiên bản Python (>= 3.6)
2. Cài đặt đầy đủ thư viện
3. Tạo issue với thông tin lỗi chi tiết 