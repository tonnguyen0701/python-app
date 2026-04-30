from pathlib import Path
from collections import OrderedDict
import re

root = Path(__file__).resolve().parent
py_files = list(root.rglob('*.py'))
ui_files = list(root.rglob('*.ui'))

py_replacements = OrderedDict([
    ('QDialog.DialogCode', 'QDialog.DialogCode'),
    (' is None', ' is None'),
    ('= None', '= None'),
    (', None)', ', None)'),
    ('SubjectService', 'SubjectService'),
    ('Tất cả học sinh', 'Tất cả học sinh'),
    ('Báo cáo & Thống kê', 'Báo cáo & Thống kê'),
    ('Điểm trung bình', 'Điểm trung bình'),
    ('Điểm trung bình', 'Điểm trung bình'),
    ('Chào mừng đến với hệ thống quản lý điểm học sinh', 'Chào mừng đến với hệ thống quản lý điểm học sinh'),
    ('QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?"', 'QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa điểm này?"'),
    ('QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa học sinh này?"', 'QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa học sinh này?"'),
    ('QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa giáo viên này?"', 'QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa giáo viên này?"'),
    ('QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa môn học này?"', 'QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa môn học này?"'),
    ('QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa lớp học này?"', 'QMessageBox.question(self, "Xác nhận", "Bạn có chắc chắn muốn xóa lớp học này?"'),
    ('QMessageBox.information(self, "Kết quả", f"Điểm trung bình:', 'QMessageBox.information(self, "Kết quả", f"Điểm trung bình:'),
    ('self.setWindowTitle("Học sinh" if student is None else f"Sửa học sinh - {student.name}")', 'self.setWindowTitle("Học sinh" if student is None else f"Sửa học sinh - {student.name}")'),
    ('self.setWindowTitle("Thêm môn học" if subject is None else f"Sửa môn học - {subject.name}")', 'self.setWindowTitle("Thêm môn học" if subject is None else f"Sửa môn học - {subject.name}")'),
    ('self.setWindowTitle("Thêm giáo viên" if teacher is None else f"Sửa giáo viên - {teacher.name}")', 'self.setWindowTitle("Thêm giáo viên" if teacher is None else f"Sửa giáo viên - {teacher.name}")'),
    ('self.setWindowTitle("Thông tin học sinh")', 'self.setWindowTitle("Thông tin học sinh")'),
    ('self.setWindowTitle("Thông tin giáo viên")', 'self.setWindowTitle("Thông tin giáo viên")'),
    ('self.setWindowTitle("Thông tin môn học")', 'self.setWindowTitle("Thông tin môn học")'),
    ('self.setWindowTitle("Thông tin lớp học")', 'self.setWindowTitle("Thông tin lớp học")'),
    ('self.setWindowTitle("Thông tin điểm")', 'self.setWindowTitle("Thông tin điểm")'),
])

ui_replacements = OrderedDict([
    ('Chào mừng đến với hệ thống quản lý điểm học sinh', 'Chào mừng đến với hệ thống quản lý điểm học sinh'),
    ('Điểm trung bình', 'Điểm trung bình'),
    ('Điểm trung bình', 'Điểm trung bình'),
    ('Export Data', 'Xuất dữ liệu'),
    ('Export Data As:', 'Xuất dữ liệu thành:'),
])

changed_files = []

for path in py_files:
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in py_replacements.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed_files.append(path.relative_to(root))

for path in ui_files:
    text = path.read_text(encoding='utf-8')
    original = text
    for old, new in ui_replacements.items():
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding='utf-8')
        changed_files.append(path.relative_to(root))

print('Changed files:')
for f in changed_files:
    print(f)
