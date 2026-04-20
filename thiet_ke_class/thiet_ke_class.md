# Thiết kế class cho phần mềm quản lý điểm THPT

## 1. Tổng quan kiến trúc

Phần mềm được tổ chức theo mô hình hướng đối tượng kết hợp kiến trúc phân tách trách nhiệm kiểu MVC + DAO:

- `models/`: chứa các class thực thể (entity) đại diện cho dữ liệu trong hệ thống.
- `database/`: chứa các class DAO chịu trách nhiệm truy xuất CSDL.
- `services/`: chứa các class xử lý nghiệp vụ, thực hiện xác thực, tính toán và gọi DAO.
- `views/` và `ui/`: chứa các class giao diện người dùng, khung nhìn và điều khiển CRUD.
- `controllers/`: chứa các class kiểm soát hành vi ứng dụng nếu cần tách riêng giữa view và controller.

## 2. Class chính trong `models/`

### 2.1 `Student`

- File: `src/models/student.py`
- Vai trò: mô tả dữ liệu học sinh.
- Thuộc tính chính:
  - `student_id`
  - `name`
  - `date_of_birth`
  - `gender`
  - `email`
  - `phone`
  - `address`
  - `created_at`
- Phương thức:
  - `__repr__`: tiện cho debug và log.
  - `to_dict()`: chuyển đối tượng thành dict.

### 2.2 `Teacher`

- File: `src/models/teacher.py`
- Vai trò: mô tả dữ liệu giáo viên.
- Thuộc tính chính:
  - `teacher_id`
  - `name`
  - `email`
  - `phone`
  - `department`
  - `created_at`
- Phương thức tương tự `Student`.

### 2.3 `ClassRoom`

- File: `src/models/classroom.py`
- Vai trò: mô tả lớp học/lớp chủ nhiệm.
- Thuộc tính chính:
  - `class_id`
  - `name`
  - `grade_level`
  - `homeroom_teacher_id`
  - `created_at`

### 2.4 Các model khác (đề xuất theo cấu trúc)

- `src/models/subject.py`: mô tả môn học.
- `src/models/score.py`: mô tả điểm số của học sinh theo môn.
- `src/models/semester.py`: mô tả học kỳ.

Những model này nên giữ cấu trúc đơn giản, chỉ chứa dữ liệu và phương thức chuyển đổi hỗ trợ DAO.

## 3. Class truy xuất CSDL (`database/`)

### 3.1 `DatabaseConnection`

- File: `src/database/db_connect.py`
- Vai trò: quản lý kết nối MySQL, tạo database nếu cần và thực thi truy vấn chung.
- Thiết kế:
  - singleton connection: `DatabaseConnection._connection`
  - phương thức `get_connection()` trả về kết nối dùng lại.
  - phương thức `execute_query(query, params=None)` dùng cho truy vấn ghi/đọc.
  - `close_connection()` để giải phóng tài nguyên.

### 3.2 DAO cụ thể

Mỗi thực thể có DAO riêng chịu trách nhiệm các thao tác CRUD.

Ví dụ `ClassDAO` trong `src/database/class_dao.py`:
- `insert(classroom: ClassRoom)`
- `find_by_id(class_id)`
- `find_all()`
- `update(class_id, classroom: ClassRoom)`
- `delete(class_id)`
- `_row_to_class(row)` chuyển `tuple` kết quả DB thành đối tượng `ClassRoom`

Thiết kế tương tự nên áp dụng cho:
- `StudentDAO`
- `TeacherDAO`
- `SubjectDAO`
- `ScoreDAO`
- `SemesterDAO`

## 4. Class nghiệp vụ (`services/`)

### 4.1 Mục đích

Service acts as a bridge between controller/view and DAO.

- Nhận dữ liệu model từ giao diện.
- Thực hiện xác thực dữ liệu.
- Gọi DAO để lưu/truy vấn CSDL.
- Xử lý logic bổ sung như lọc, tính điểm trung bình, xếp loại.

### 4.2 Ví dụ `StudentService`

- File: `src/services/student_service.py`
- Phương thức:
  - `create_student(student_data)`
  - `get_student(student_id)`
  - `get_all_students()`
  - `update_student(student_id, student_data)`
  - `delete_student(student_id)`
  - `search_students(keyword)`

### 4.3 Đề xuất cho các service khác

- `TeacherService`: quản lý giáo viên.
- `ClassService`: quản lý lớp học và gán giáo viên chủ nhiệm.
- `SubjectService`: quản lý môn học.
- `ScoreService`: quản lý điểm, tính GPA, phân loại học lực.
- `ReportService`: tổng hợp và xuất báo cáo.

## 5. Class giao diện / trình bày (`views/` và `ui/`)

### 5.1 `BaseTableView`

- File: `src/views/base_view.py`
- Vai trò: class cha chung cho các màn hình bảng dữ liệu có CRUD.
- Thiết kế:
  - tạo layout cơ bản, table và nút Thêm/Sửa/Xóa/Làm mới.
  - `add_search_bar()` thêm thanh tìm kiếm.
  - `load_table_data(data_list, row_mapper)` nạp dữ liệu vào table.
  - `get_selected_row_id()` lấy ID của dòng được chọn.
  - định nghĩa các phương thức trừu tượng `on_add()`, `on_edit()`, `on_delete()`, `on_refresh()` để subclass override.

### 5.2 `StudentView`

- File: `src/views/student_view.py`
- Kế thừa `BaseTableView`.
- Implement:
  - `load_data()` tải danh sách học sinh.
  - `on_add()`, `on_edit()`, `on_delete()`, `on_refresh()` xử lý CRUD.
- Tạo `StudentDialog` để nhập/sửa thông tin học sinh.

### 5.3 Các view tương tự

- `TeacherView`
- `ClassView`
- `SubjectView`
- `ScoreView`
- `ReportView`

Mỗi view nên tái sử dụng `BaseTableView` và mở rộng riêng cho từng đối tượng.

## 6. Class controller (`controllers/`)

### 6.1 Mục đích

Controller giữ trách nhiệm giao diện tương tác và xử lý sự kiện. Trong dự án này, một số màn hình có thể được triển khai trực tiếp trong `views/`, nhưng vẫn tồn tại `controllers/` để tách riêng logic UI.

### 6.2 Ví dụ `StudentController`

- File: `src/controllers/student_controller.py`
- Khởi tạo service `StudentService()`.
- Xây dựng giao diện với PyQt6 thủ công.
- Các phương thức:
  - `init_ui()` tạo form, bảng, nút.
  - `load_students()`, `add_student()`, `edit_student()`, `delete_student()`.
- `StudentDialog` riêng để nhập dữ liệu.

## 7. Mối quan hệ giữa các lớp

### 7.1 Luồng dữ liệu điển hình

1. Người dùng tương tác với `View` hoặc `Controller`.
2. `View/Controller` tạo hoặc cập nhật một model entity (`Student`, `Teacher`, `ClassRoom`, ...).
3. Gọi phương thức tương ứng trong `Service`.
4. `Service` gọi `DAO` để thực thi truy vấn đến `DatabaseConnection`.
5. DAO trả về entity hoặc danh sách entity.
6. `View` hiển thị kết quả trên giao diện.

### 7.2 Sơ đồ lớp logic

- `BaseTableView` <- `StudentView`, `TeacherView`, `ClassView`, ...
- `StudentService` -> `StudentDAO` -> `DatabaseConnection`
- `TeacherService` -> `TeacherDAO` -> `DatabaseConnection`
- `ClassService` -> `ClassDAO` -> `DatabaseConnection`
- `ScoreService` -> `ScoreDAO` -> `DatabaseConnection`
- `ReportService` -> các DAO tương ứng
- `StudentController` (hoặc `StudentView`) sử dụng `StudentService`

## 8. Đề xuất thiết kế mở rộng

### 8.1 Tách UI và logic rõ hơn

- `views/` chỉ nên tập trung hiển thị.
- `controllers/` chỉ xử lý sự kiện và điều phối service.
- `services/` giữ nghiệp vụ.
- `database/` giữ truy xuất dữ liệu.

### 8.2 Thêm lớp helper/utility

- `utils/validator.py`: validate email, số điện thoại, ngày sinh.
- `utils/helpers.py`: hàm hỗ trợ chuyển đổi, format ngày, xếp loại điểm.

### 8.3 Thiết kế interface/abstract class

- Tạo `BaseDAO` với các phương thức chung `insert`, `find_by_id`, `find_all`, `update`, `delete`.
- Tạo `BaseService` định nghĩa các phương thức phổ biến.

## 9. Kết luận

Thiết kế hiện tại đã có sự phân chia rõ ràng giữa dữ liệu, nghiệp vụ và giao diện. Để mở rộng và bảo trì tốt hơn, nên duy trì quy tắc:

- class entity chỉ lưu dữ liệu;
- DAO chỉ thao tác với CSDL;
- service xử lý nghiệp vụ và xác thực;
- view/controller xử lý giao diện và tương tác người dùng.

File này là tài liệu thiết kế class cho phần mềm quản lý điểm THPT, phù hợp để tiếp tục phát triển, mở rộng và nâng cấp sau này.
