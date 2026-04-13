# Student Score Management System

Hệ thống quản lý điểm học sinh THPT - ứng dụng desktop được xây dựng với PyQt6

## 🎯 Tính năng

### Đăng nhập / Phân quyền
- 👤 Hệ thống xác thực an toàn với hash password
- 🔐 3 vai trò: Admin, Teacher, User
- 📋 Phân quyền theo vai trò (Role-based Access Control)

### Quản lý Dữ liệu
- 👨‍🎓 **Quản lý học sinh**: Thêm, sửa, xóa, tìm kiếm học sinh
- 👨‍🏫 **Quản lý giáo viên**: Quản lý thông tin giáo viên (Admin only)
- 🏫 **Quản lý lớp học**: Gán giao viên, cập nhật thông tin lớp (Admin only)
- 📖 **Quản lý môn học**: Tạo, chỉnh sửa danh sách môn học và tín chỉ
- 📊 **Quản lý điểm số**: Nhập, cập nhật, xem điểm theo từng học sinh

### Tính Toán & Thống Kê
- 📈 Tính toán điểm trung bình (GPA)
- ⭐ Xếp loại học lực: Giỏi, Khá, Trung bình, Yếu, Kém
- 📊 Báo cáo thống kê trực quan
- 📉 Biểu đồ phân phối điểm

### Xuất Dữ Liệu
- 📥 Xuất dữ liệu ra Excel (.xlsx)
- 📄 Xuất dữ liệu ra CSV
- 🖼️ Tạo biểu đồ và lưu dưới dạng PNG

## ⚙️ Yêu cầu

- Python 3.8+
- PyQt6==6.6.1
- pandas==2.2.3
- matplotlib==3.8.1
- openpyxl==3.1.2
- python-docx==0.8.11
- SQLite3 (có sẵn)

## 🚀 Cài đặt & Chạy

### 1. Clone/Tải về
```bash
git clone <repository-url>
cd student-score-management
```

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Chạy ứng dụng
```bash
python main.py
```

## 📝 Hướng Dẫn Sử Dụng

### Mở ứng dụng
- Chỉ cần chạy `main.py` hoặc double-click `run_main.bat`
- Ứng dụng sẽ mở thẳng vào cửa sổ chính, không cần đăng nhập

### Quản lý học sinh
- Click "View/Edit Students" từ menu chính
- Có thể thêm, sửa, xóa, tìm kiếm học sinh
- Nhập đủ thông tin: Tên, ngày sinh, giới tính, email, SĐT, địa chỉ

### Quản lý giáo viên (Admin only)
- Click "Manage Teachers"
- Thêm/sửa/xóa giáo viên
- Quản lý thông tin: Tên, email, SĐT, bộ môn

### Quản lý lớp (Admin only)
- Click "Manage Classes"
- Tạo lớp, gán giao viên chủ nhiệm
- Cập nhật thông tin lớp

### Quản lý môn học
- Click "Manage Subjects"
- Thêm/sửa/xóa môn học
- Cấu hình mã môn, tín chỉ

### Nhập điểm
- Click "Input/View Scores"
- Chọn học sinh để xem điểm của họ
- Thêm/sửa/xóa điểm theo môn học
- Tính toán điểm trung bình tự động

### Xem báo cáo
- Click "View Reports & Statistics"
- Tab "Average Scores": Xem danh sách và thống kê
- Tab "Export Data": Xuất dữ liệu ra Excel / CSV / PNG

## 💾 Database Schema

### Bảng chính:
- **users**: Tài khoản người dùng (username, password hash, role)
- **students**: Thông tin học sinh
- **teachers**: Thông tin giáo viên
- **classes**: Lớp học
- **subjects**: Môn học
- **scores**: Điểm số (student_id, subject_id, score_value, semester)
- **enrollments**: Đăng ký lớp (student & class mapping)
- **teacher_subjects**: Gán dạy (teacher & subject mapping)

## 🐛 Khắc Phục Sự Cố

### Lỗi: "Database is locked"
- Đóng tất cả các cửa sổ ứng dụng
- Xóa file `.db-journal` nếu có
- Chạy lại ứng dụng

### Lỗi: "Module not found"
- Đảm bảo đã chạy: `pip install -r requirements.txt`
- Kiểm tra phiên bản Python (3.8+)

### Không thể đăng nhập
- Kiểm tra database đã được khởi tạo: `python setup_db.py`
- Mật khẩu mặc định: `admin123` cho tài khoản admin

## 🤝 Vai Trò Người Dùng

### Admin
- Toàn quyền truy cập tất cả chức năng
- Quản lý giáo viên, lớp học
- Quản lý user
- Xem báo cáo

### Teacher
- Quản lý học sinh
- Nhập/xem điểm
- Xem báo cáo

### User
- Xem thông tin cá nhân
- Xem điểm của mình

## 📝 License

MIT License

## 👨‍💻 Tác giả

NT

Username: admin
Password: admin123