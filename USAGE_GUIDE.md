# Hướng dẫn sử dụng Git Diff Tool

## 📖 Mục lục
1. [Giới thiệu](#giới-thiệu)
2. [Cài đặt](#cài-đặt)
3. [Sử dụng cơ bản](#sử-dụng-cơ-bản)
4. [Sử dụng nâng cao](#sử-dụng-nâng-cao)
5. [Xử lý lỗi](#xử-lý-lỗi)
6. [FAQ](#faq)

## 🎯 Giới thiệu

Git Diff Tool là một công cụ GUI đơn giản giúp bạn so sánh 2 phiên bản khác nhau của một Git repository và tạo ra các file tương ứng trong 2 thư mục riêng biệt.

### Khi nào sử dụng?
- So sánh code giữa 2 branch khác nhau
- Xem sự thay đổi giữa 2 commit gần nhất
- Phân tích sự khác biệt trong dự án
- Backup và so sánh phiên bản code

## 🚀 Cài đặt

### Bước 1: Kiểm tra yêu cầu hệ thống
```bash
# Kiểm tra Python
python --version  # Phải >= 3.6

# Kiểm tra Git
git --version
```

### Bước 2: Tải và cài đặt
```bash
# Clone repository
git clone <repository-url>
cd github-diff-tool

# Cài đặt thư viện
pip install -r requirements.txt
```

### Bước 3: Chạy ứng dụng
```bash
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh

# Hoặc trực tiếp
python run.py
```

## 💻 Sử dụng cơ bản

### 1. Nhập Repository URL
- Mở ứng dụng
- Nhập URL GitHub repository vào ô đầu tiên
- Ví dụ: `https://github.com/username/project-name`

### 2. Xác thực (nếu cần)
- Nếu repository là private, nhập Personal Access Token
- Token có thể tạo tại: GitHub Settings > Developer settings > Personal access tokens
- Cần quyền `repo` để truy cập private repository

### 3. Clone Repository
- Nhấn nút "Clone Repository"
- Đợi quá trình clone hoàn tất
- Thanh tiến trình sẽ hiển thị trạng thái

### 4. Chọn chế độ so sánh
- **So sánh 2 branch**: Chọn 2 branch khác nhau
- **So sánh 2 commit gần nhất**: Tự động lấy 2 commit mới nhất

### 5. Chọn thư mục đích
- Nhấn "Browse" để chọn nơi lưu kết quả
- Tool sẽ tạo 2 thư mục: `before/` và `after/`

### 6. Thực hiện so sánh
- Nhấn "So sánh và Tạo Diff"
- Đợi quá trình hoàn tất
- Kết quả sẽ được hiển thị trong popup

## 🔧 Sử dụng nâng cao

### So sánh Repository Private
1. Tạo Personal Access Token trên GitHub
2. Chọn quyền `repo` (full control of private repositories)
3. Copy token và paste vào ô "Personal Access Token"
4. Clone repository như bình thường

### So sánh 2 Commit cụ thể
1. Chọn chế độ "So sánh 2 commit gần nhất"
2. Danh sách commit sẽ hiển thị với format: `hash - message`
3. Chọn 2 commit muốn so sánh
4. Thực hiện so sánh

### Tùy chỉnh cấu hình
Chỉnh sửa file `config.json`:
```json
{
    "app_settings": {
        "max_commits": 20,  // Số commit tối đa hiển thị
        "window_size": "800x600"  // Kích thước cửa sổ
    }
}
```

## 🐛 Xử lý lỗi

### Lỗi "Repository not found"
**Nguyên nhân:**
- URL repository không đúng
- Repository không tồn tại
- Không có quyền truy cập

**Giải pháp:**
1. Kiểm tra lại URL repository
2. Đảm bảo repository tồn tại
3. Nếu là private repo, nhập Personal Access Token

### Lỗi "Authentication failed"
**Nguyên nhân:**
- Personal Access Token không đúng
- Token hết hạn
- Token không có đủ quyền

**Giải pháp:**
1. Tạo token mới tại GitHub
2. Đảm bảo token có quyền `repo`
3. Copy token chính xác (không có khoảng trắng)

### Lỗi "Permission denied"
**Nguyên nhân:**
- Không có quyền ghi vào thư mục đích
- Thư mục đích bị khóa

**Giải pháp:**
1. Chọn thư mục khác có quyền ghi
2. Chạy ứng dụng với quyền admin (Windows)
3. Kiểm tra quyền thư mục (Linux/Mac)

### Lỗi "Network timeout"
**Nguyên nhân:**
- Kết nối mạng chậm
- Repository quá lớn
- Firewall chặn kết nối

**Giải pháp:**
1. Kiểm tra kết nối internet
2. Thử lại sau vài phút
3. Tắt firewall tạm thời
4. Sử dụng VPN nếu cần

## ❓ FAQ

### Q: Tool có hỗ trợ repository từ GitLab/Bitbucket không?
A: Hiện tại tool được thiết kế cho GitHub, nhưng có thể hoạt động với các Git repository khác nếu URL format tương tự.

### Q: Có thể so sánh nhiều hơn 2 branch/commit không?
A: Hiện tại tool chỉ hỗ trợ so sánh 2 phiên bản. Để so sánh nhiều hơn, bạn có thể chạy tool nhiều lần.

### Q: Tool có lưu trữ Personal Access Token không?
A: Không, token chỉ được sử dụng để clone repository và không được lưu trữ trên máy.

### Q: Có thể hủy quá trình clone/so sánh không?
A: Hiện tại chưa có tính năng hủy. Bạn có thể đóng ứng dụng và chạy lại.

### Q: Tool có hỗ trợ so sánh file cụ thể không?
A: Hiện tại tool so sánh toàn bộ repository. Bạn có thể sử dụng công cụ diff khác để so sánh file cụ thể sau khi có kết quả.

### Q: Có thể tùy chỉnh file/folder bị loại trừ không?
A: Có thể chỉnh sửa `config.json` để thêm pattern loại trừ:
```json
"ignore_patterns": [
    ".git",
    "node_modules",
    "*.log",
    "temp/"
]
```

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần "Xử lý lỗi" ở trên
2. Tạo issue trên GitHub repository
3. Cung cấp thông tin chi tiết về lỗi và môi trường hệ thống 