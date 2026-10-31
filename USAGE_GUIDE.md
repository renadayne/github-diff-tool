# Hướng dẫn sử dụng Git Diff Tool

Tài liệu này cung cấp hướng dẫn chi tiết về các thao tác, tính năng nâng cao và cách giải quyết các tình huống thường gặp khi sử dụng Git Diff Tool.

---

## Mục lục

1. [Tổng quan](#tổng-quan)
2. [Thao tác cơ bản](#thao-tác-cơ-bản)
3. [Các tính năng nâng cao](#các-tính-năng-nâng-cao)
4. [Tích hợp công cụ ngoài](#tích-hợp-công-cụ-ngoài)
5. [Khắc phục sự cố](#khắc-phục-sự-cố)

---

## Tổng quan

Git Diff Tool giúp lập trình viên nhanh chóng:
- Xem trước sự khác biệt giữa hai nhánh (branch) hoặc hai commit.
- Trích xuất riêng các file bị thay đổi (giữ nguyên cấu trúc thư mục phân cấp tương đối) để gửi cho khách hàng, đối tác hoặc phục vụ đánh giá mã nguồn (code review).
- Tạo file patch chuẩn (`.patch`) và báo cáo tổng hợp thay đổi (`.md`, `.json`).

---

## Thao tác cơ bản

### 1. Mở Repository

Ứng dụng hỗ trợ hai phương thức nạp mã nguồn:

#### Cách 1: Sử dụng thư mục mã nguồn có sẵn trên máy (Local Repo)
1. Tại thẻ **Thư mục máy (Local Repo)**, nhấn **Chọn thư mục...**.
2. Chọn thư mục chứa repository (thư mục có chứa folder con `.git`).
3. Nhấn **Mở Repository**. Thanh trạng thái phía trên sẽ chuyển sang màu xanh hiển thị tên repo.

#### Cách 2: Clone từ GitHub (Remote Repo)
1. Chuyển sang thẻ **Clone từ GitHub (Remote)**.
2. Nhập URL HTTPS của repository (ví dụ: `https://github.com/torvalds/linux.git`).
3. Nếu là kho lưu trữ riêng tư (private repo), nhập mã **Personal Access Token** vào ô mật khẩu.
4. Nhấn **Clone Repository**. Ứng dụng sẽ clone về thư mục tạm trong nền mà không làm đơ giao diện.

### 2. Chọn phiên bản so sánh

1. Chọn chế độ:
   - **So sánh giữa 2 Nhánh**: Danh sách dropdown sẽ hiển thị toàn bộ các nhánh local và remote có sẵn.
   - **So sánh giữa 2 Commit**: Dropdown sẽ liệt kê các commit gần nhất kèm mã hash, thông điệp commit, tác giả và ngày tháng.
2. Chọn phiên bản gốc tại ô **Bản Trước (Before)** và phiên bản cần đối chiếu tại ô **Bản Sau (After)**.
3. Nếu muốn đổi chiều so sánh, nhấn nút **⇄ Đổi**.
4. Nhấn **Xem trước Diff**: Danh sách các file thay đổi sẽ hiển thị ngay trong bảng bên dưới.

### 3. Xuất file kết quả

1. Chọn thư mục đích tại ô **Thư mục xuất**.
2. Lựa chọn chế độ xuất:
   - **Chỉ xuất file thay đổi (Khuyên dùng)**: Chỉ trích xuất các file modified, added, deleted, renamed. Đây là phương thức nhanh nhất và tiết kiệm dung lượng ổ đĩa.
   - **Xuất toàn bộ snapshot**: Trích xuất toàn bộ cây mã nguồn của cả hai phiên bản.
3. Tích chọn **Tạo patch (.patch)** và **Báo cáo tóm tắt (.md/.json)** nếu cần.
4. Nhấn **So sánh & Xuất Thư mục**.

---

## Các tính năng nâng cao

### Trình xem Diff trực quan (In-app Diff Viewer)

Khi xem trước hoặc sau khi xuất file:
- Click vào bất kỳ file nào trong danh sách bên trái để xem nội dung diff tô màu ở khung bên phải:
  - Khối hunk header (`@@ ... @@`) được làm nổi bật với màu chàm (indigo).
  - Các dòng thêm mới (`+`) có màu xanh lá và nền xanh nhạt.
  - Các dòng bị xóa (`-`) có màu đỏ và nền đỏ nhạt.
- Nhấn **Sao chép Diff** để lưu nội dung unified diff của file (hoặc toàn bộ) vào bộ nhớ tạm (Clipboard).

### Tích hợp Visual Studio Code

Nếu máy tính đã cài đặt lệnh `code` trong PATH:
1. Chọn file cần so sánh trong danh sách.
2. Nhấn nút **Mở trong VS Code**.
3. VS Code sẽ tự động mở chế độ so sánh 2 file cạnh nhau (`code --diff before/file after/file`).

---

## Khắc phục sự cố

### 1. Ứng dụng không tìm thấy Git
- Git Diff Tool đã tích hợp sẵn module `core.git_finder` tự động quét các thư mục cài đặt thông dụng trên Windows.
- Nếu bạn cài Git ở một đường dẫn đặc thù, bạn có thể thiết lập biến môi trường `GIT_PYTHON_GIT_EXECUTABLE` trỏ trực tiếp đến file `git.exe` trước khi chạy ứng dụng, hoặc cấu hình trong `config.json` mục `git_settings.custom_git_path`.

### 2. Lỗi xác thực khi Clone Private Repository
- Kiểm tra lại Personal Access Token xem đã cấp quyền `repo` (đối với classic token) hoặc quyền đọc `Contents` (đối với fine-grained token) hay chưa.
- Đảm bảo URL bắt đầu bằng `https://github.com/...`.

### 3. File binary hoặc file quá lớn
- Với các file nhị phân (hình ảnh, file nén, file thực thi), trình xem diff sẽ hiển thị thông báo thay vì render văn bản để tránh làm chậm giao diện. Tuy nhiên, file vẫn được trích xuất đầy đủ và chính xác vào hai thư mục `before/` và `after/`.