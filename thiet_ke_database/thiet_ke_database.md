# Thiết kế Database cho phần mềm quản lý điểm THPT

## 1. Tổng quan kiến trúc Database

Database được thiết kế trên MySQL sử dụng InnoDB và bộ ký tự `utf8mb4` để đảm bảo hỗ trợ tiếng Việt và quan hệ giữa các bảng.

Mục tiêu thiết kế:
- Lưu trữ dữ liệu học sinh, giáo viên, lớp, môn học, điểm, học kỳ.
- Chuẩn hóa quan hệ và tránh dư thừa dữ liệu.
- Hỗ trợ mở rộng dễ dàng cho báo cáo, xuất dữ liệu và quản lý lớp học.

## 2. Các bảng chính

### 2.1 `students`

Mô tả thông tin học sinh.

Các cột:
- `student_id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(255) NOT NULL
- `date_of_birth` DATE
- `gender` VARCHAR(20)
- `email` VARCHAR(255) UNIQUE
- `phone` VARCHAR(50)
- `address` VARCHAR(255)
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### 2.2 `teachers`

Mô tả thông tin giáo viên.

Các cột:
- `teacher_id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(255) NOT NULL
- `email` VARCHAR(255) UNIQUE
- `phone` VARCHAR(50)
- `department` VARCHAR(255)
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### 2.3 `classes`

Mô tả các lớp học và gán giáo viên chủ nhiệm.

Các cột:
- `class_id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(255) NOT NULL UNIQUE
- `grade_level` INT
- `homeroom_teacher_id` INT
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Khóa ngoại: `FOREIGN KEY (homeroom_teacher_id) REFERENCES teachers(teacher_id)`

### 2.4 `subjects`

Mô tả môn học và một số thuộc tính mở rộng.

Các cột:
- `subject_id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(255) NOT NULL UNIQUE
- `code` VARCHAR(50) NOT NULL UNIQUE
- `credit` INT
- `class_name` VARCHAR(255)
- `class_shift` VARCHAR(255)
- `class_day` VARCHAR(255)
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

Ghi chú: bảng này có thể dùng để quản lý thêm lịch học, ca học, tên lớp giảng dạy.

### 2.5 `scores`

Lưu trữ điểm của học sinh theo môn học.

Các cột:
- `score_id` INT PRIMARY KEY AUTO_INCREMENT
- `student_id` INT NOT NULL
- `subject_id` INT NOT NULL
- `score_value` DOUBLE NOT NULL
- `midterm_score` DOUBLE DEFAULT 0
- `final_score` DOUBLE DEFAULT 0
- `semester` VARCHAR(100)
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Khóa ngoại: `FOREIGN KEY (student_id) REFERENCES students(student_id)`
- Khóa ngoại: `FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)`

### 2.6 `semesters`

Quản lý học kỳ / kỳ học.

Các cột:
- `semester_id` INT PRIMARY KEY AUTO_INCREMENT
- `name` VARCHAR(255) NOT NULL UNIQUE
- `start_date` DATE
- `end_date` DATE
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### 2.7 `enrollments`

Lưu quan hệ học sinh - lớp theo học kỳ.

Các cột:
- `enrollment_id` INT PRIMARY KEY AUTO_INCREMENT
- `student_id` INT NOT NULL
- `class_id` INT NOT NULL
- `semester` VARCHAR(100)
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Khóa ngoại: `FOREIGN KEY (student_id) REFERENCES students(student_id)`
- Khóa ngoại: `FOREIGN KEY (class_id) REFERENCES classes(class_id)`

### 2.8 `teacher_subjects`

Lưu quan hệ giáo viên - môn học.

Các cột:
- `id` INT PRIMARY KEY AUTO_INCREMENT
- `teacher_id` INT NOT NULL
- `subject_id` INT NOT NULL
- `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- Khóa ngoại: `FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)`
- Khóa ngoại: `FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)`

## 3. Quan hệ giữa các bảng

- `students` 1-n `scores`
- `subjects` 1-n `scores`
- `teachers` 1-n `classes` (qua `homeroom_teacher_id`)
- `students` n-n `classes` thông qua `enrollments`
- `teachers` n-n `subjects` thông qua `teacher_subjects`

## 4. Thiết kế và mở rộng

### 4.1 Thiết kế theo chuẩn quan hệ

- Mỗi bảng có khóa chính tự tăng (`AUTO_INCREMENT`).
- Các cột `UNIQUE` dùng cho email, mã môn học, tên lớp, tên học kỳ để tránh dữ liệu trùng.
- Sử dụng `FOREIGN KEY` để đảm bảo tính nhất quán và giúp xóa/cập nhật theo ràng buộc nếu mở rộng thêm.

### 4.2 Lý do sử dụng `TIMESTAMP`

- Dùng để lưu `created_at` cho mỗi bản ghi.
- Giúp audit, truy xuất lịch sử và hỗ trợ báo cáo theo thời gian.

### 4.3 Hỗ trợ tính toán điểm và báo cáo

- Bảng `scores` có `midterm_score`, `final_score` để lưu chi tiết điểm thành phần.
- Cột `semester` giúp lọc điểm theo học kỳ.
- Có thể mở rộng thêm bảng `score_types` hoặc `score_details` nếu cần lưu nhiều loại điểm hơn.

### 4.4 Khả năng mở rộng

Có thể thêm các bảng và trường sau:
- `users` để quản lý tài khoản người dùng, mật khẩu và quyền truy cập.
- `roles` + `user_roles` để phân quyền Admin/Teacher/User.
- `class_schedule` để quản lý lịch học chi tiết.
- `report_exports` để lưu lịch sử xuất Excel/CSV.

## 5. Cách khởi tạo database trong dự án

File `src/database/init_db.py` thực hiện:
- Tạo cơ sở dữ liệu nếu chưa tồn tại.
- Tạo các bảng `students`, `subjects`, `scores`, `semesters`, `teachers`, `classes`, `enrollments`, `teacher_subjects`.
- Kiểm tra và bổ sung các cột nếu bảng đã tồn tại nhưng chưa có cột mới.

## 6. Kết luận

Thiết kế database hiện tại đã cơ bản đáp ứng yêu cầu quản lý học sinh, giáo viên, lớp học, môn học và điểm số. Với cấu trúc quan hệ rõ ràng, hệ thống có thể mở rộng thêm báo cáo, phân quyền và dữ liệu lịch học trong tương lai.
