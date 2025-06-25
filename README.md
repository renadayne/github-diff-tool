# Git Diff Tool - Công cụ so sánh Git

Một công cụ GUI đơn giản để so sánh 2 branch hoặc 2 commit trong Git repository và tạo ra các file tương ứng trong 2 thư mục `before/` và `after/`.

## 🎯 Tính năng

- **So sánh 2 branch**: Chọn 2 branch khác nhau để so sánh
- **So sánh 2 commit gần nhất**: Tự động lấy 2 commit mới nhất trên branch hiện tại
- **Hỗ trợ repository private**: Sử dụng Personal Access Token để xác thực
- **Giao diện thân thiện**: GUI đơn giản với tkinter
- **Xử lý đa luồng**: Không làm treo giao diện khi thực hiện các tác vụ nặng
- **Tự động dọn dẹp**: Xóa thư mục tạm khi đóng ứng dụng

## 📋 Yêu cầu hệ thống

- Python 3.6 trở lên
- Git (cài đặt trên máy)
- Kết nối internet để clone repository

## 🚀 Cài đặt

1. **Clone repository này:**
   ```bash
   git clone <repository-url>
   cd github-diff-tool
   ```

2. **Cài đặt các thư viện cần thiết:**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Cách sử dụng

### Chạy ứng dụng:
```bash
python run.py
```
hoặc
```bash
python git_diff_tool.py
```

### Hướng dẫn từng bước:

1. **Nhập GitHub Repository URL**
   - Ví dụ: `https://github.com/username/repository-name`
   - Hỗ trợ cả HTTPS và SSH URL

2. **Xác thực (nếu cần)**
   - Nếu repository là private, nhập Personal Access Token
   - Tạo token tại: GitHub Settings > Developer settings > Personal access tokens
   - Cần quyền `repo` để truy cập private repository

3. **Clone Repository**
   - Nhấn nút "Clone Repository"
   - Đợi quá trình clone hoàn tất

4. **Chọn chế độ so sánh**
   - **So sánh 2 branch**: Chọn 2 branch khác nhau
   - **So sánh 2 commit gần nhất**: Tự động lấy 2 commit mới nhất

5. **Chọn thư mục đích**
   - Nhấn "Browse" để chọn nơi lưu kết quả
   - Tool sẽ tạo 2 thư mục: `before/` và `after/`

6. **Thực hiện so sánh**
   - Nhấn "So sánh và Tạo Diff"
   - Đợi quá trình hoàn tất

## 📁 Kết quả

Sau khi hoàn tất, bạn sẽ có:
```
thư_mục_đích/
├── before/          # Phiên bản 1 (branch/commit đầu tiên)
│   ├── file1.py
│   ├── file2.py
│   └── ...
└── after/           # Phiên bản 2 (branch/commit thứ hai)
    ├── file1.py
    ├── file2.py
    └── ...
```

## 🔧 Cấu trúc dự án

```
github-diff-tool/
├── git_diff_tool.py     # File chính chứa GUI và logic
├── run.py              # Script để chạy tool
├── requirements.txt    # Danh sách thư viện cần thiết
└── README.md          # Tài liệu hướng dẫn
```

## 🛠 Thư viện sử dụng

- **tkinter**: Giao diện người dùng (có sẵn trong Python)
- **gitpython**: Thao tác với Git repository
- **requests**: Gọi API GitHub (nếu cần)
- **shutil, os, tempfile**: Thao tác file và thư mục
- **threading**: Xử lý đa luồng

## ⚠️ Lưu ý

1. **Bảo mật**: Personal Access Token sẽ được sử dụng để clone repository, không được lưu trữ
2. **Dung lượng**: Tool sẽ clone toàn bộ repository vào thư mục tạm
3. **Quyền truy cập**: Cần quyền đọc repository để clone
4. **Kết nối mạng**: Cần kết nối internet ổn định để clone repository

## 🐛 Xử lý lỗi thường gặp

### Lỗi "Repository not found"
- Kiểm tra URL repository có đúng không
- Đảm bảo repository tồn tại và có quyền truy cập
- Nếu là private repo, nhập Personal Access Token

### Lỗi "Authentication failed"
- Kiểm tra Personal Access Token có đúng không
- Đảm bảo token có quyền `repo` cho private repository
- Tạo token mới nếu cần

### Lỗi "Permission denied"
- Kiểm tra quyền ghi vào thư mục đích
- Chạy với quyền admin nếu cần

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo branch mới cho tính năng
3. Commit thay đổi
4. Push và tạo Pull Request

## 📄 Giấy phép

Dự án này được phát hành dưới giấy phép MIT.