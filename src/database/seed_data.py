# Seed Data Script
# Populate database with realistic Vietnamese high school data

import mysql.connector
from datetime import datetime, date
import random
from .db_connect import DatabaseConnection


def _is_database_empty():
    """Check if database has any data"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM teachers")
        return cursor.fetchone()[0] == 0
    except:
        return True
    finally:
        DatabaseConnection.close_connection()


def seed_database():
    """Seed database with realistic Vietnamese high school data"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    
    # Check if data already exists
    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] > 0:
        print("ℹ Database already contains data. Skipping seeding.")
        DatabaseConnection.close_connection()
        return
    
    try:
        print("🌱 Starting to seed database...")
        
        # 1. Add Teachers
        print("\n📚 Adding teachers...")
        teachers_data = [
            ("Nguyễn Văn A", "nguyenvana@school.edu.vn", "0912345678", "Toán"),
            ("Trần Thị B", "tranthib@school.edu.vn", "0912345679", "Ngôn ngữ Anh"),
            ("Phạm Văn C", "phamvanc@school.edu.vn", "0912345680", "Vật lý"),
            ("Hoàng Thị D", "hoangthid@school.edu.vn", "0912345681", "Hóa học"),
            ("Lê Văn E", "levane@school.edu.vn", "0912345682", "Sinh học"),
            ("Đỗ Thị F", "dothif@school.edu.vn", "0912345683", "Lịch sử"),
            ("Vũ Văn G", "vuvang@school.edu.vn", "0912345684", "Địa lý"),
            ("Bùi Thị H", "buithih@school.edu.vn", "0912345685", "Thể dục"),
            ("Trương Văn I", "truongvani@school.edu.vn", "0912345686", "Tin học"),
            ("Dương Thị K", "duongthik@school.edu.vn", "0912345687", "Tiếng Anh"),
        ]
        
        teacher_ids = []
        for name, email, phone, department in teachers_data:
            try:
                cursor.execute(
                    "INSERT INTO teachers (name, email, phone, department, created_at) VALUES (%s, %s, %s, %s, %s)",
                    (name, email, phone, department, datetime.now())
                )
                teacher_ids.append(cursor.lastrowid)
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠ Teacher '{email}' already exists")
                else:
                    raise
        
        conn.commit()
        print(f"✓ Added {len(teacher_ids)} teachers")
        
        # 2. Add Classes
        print("\n🏫 Adding classes...")
        classes_data = [
            ("10A", 10, teacher_ids[0]),
            ("10B", 10, teacher_ids[1]),
            ("10C", 10, teacher_ids[2]),
            ("11A", 11, teacher_ids[3]),
            ("11B", 11, teacher_ids[4]),
            ("12A", 12, teacher_ids[5]),
            ("12B", 12, teacher_ids[6]),
        ]
        
        class_ids = []
        for name, grade_level, teacher_id in classes_data:
            try:
                cursor.execute(
                    "INSERT INTO classes (name, grade_level, homeroom_teacher_id, created_at) VALUES (%s, %s, %s, %s)",
                    (name, grade_level, teacher_id, datetime.now())
                )
                class_ids.append(cursor.lastrowid)
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠ Class '{name}' already exists")
                else:
                    raise
        
        conn.commit()
        print(f"✓ Added {len(class_ids)} classes")
        
        # 3. Add Subjects
        print("\n📖 Adding subjects...")
        subjects_data = [
            ("Toán", "TOAN101", 3, "10A, 10B, 10C", "Buổi sáng", "Thứ 2, 3, 5"),
            ("Vật lý", "LY101", 3, "10A, 10B, 10C", "Buổi sáng", "Thứ 3, 4, 6"),
            ("Hóa học", "HOA101", 3, "10A, 10B, 10C", "Buổi sáng", "Thứ 2, 4, 7"),
            ("Sinh học", "SINH101", 3, "10A, 10B, 10C", "Buổi chiều", "Thứ 2, 5, 6"),
            ("Ngôn ngữ Anh", "ANH101", 3, "10A, 10B, 10C", "Buổi sáng", "Thứ 2, 3, 4"),
            ("Lịch sử", "SU101", 2, "10A, 10B, 10C", "Buổi chiều", "Thứ 3, 6"),
            ("Địa lý", "DIA101", 2, "10A, 10B, 10C", "Buổi chiều", "Thứ 4, 7"),
            ("Tin học", "TIN101", 2, "10A, 10B, 10C", "Buổi chiều", "Thứ 2, 5"),
            ("Thể dục", "THEDUC101", 1, "10A, 10B, 10C", "Buổi chiều", "Thứ 5"),
            ("Giáo dục công dân", "GDCD101", 1, "10A, 10B, 10C", "Buổi chiều", "Thứ 7"),
        ]
        
        subject_ids = []
        for name, code, credit, class_name, class_shift, class_day in subjects_data:
            try:
                cursor.execute(
                    "INSERT INTO subjects (name, code, credit, class_name, class_shift, class_day, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, code, credit, class_name, class_shift, class_day, datetime.now())
                )
                subject_ids.append(cursor.lastrowid)
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠ Subject '{name}' already exists")
                else:
                    raise
        
        conn.commit()
        print(f"✓ Added {len(subject_ids)} subjects")
        
        # 4. Add Students
        print("\n👥 Adding students...")
        vietnamese_names = [
            "Nguyễn Thanh Huy", "Trần Minh Hùng", "Phạm Đức Anh", "Hoàng Quốc Toàn",
            "Lê Văn Hưng", "Đỗ Minh Tuấn", "Vũ Ngọc Hà", "Bùi Thủy Tiên",
            "Trương Minh Châu", "Dương Thị Mai", "Ngô Thanh Nhàn", "Tô Thị Thanh",
            "Phan Thị Linh", "Võ Ngọc Khánh", "Trịnh Văn Lâm", "Khương Thị Hiệp",
            "Lý Quỳnh Liên", "Đinh Thị Thùy", "Nước Anh Tuấn", "Hạ Thị Ngọc",
            "Nguyễn Thị Hương", "Phạm Văn Sơn", "Trần Đức Long", "Hoàng Anh Tuấn",
            "Lê Minh Hiệu", "Đỗ Quang Huy", "Vũ Anh Đức", "Bùi Mạnh Cường",
            "Trương Thị Hồng", "Dương Văn Quý", "Ngô Quốc Hưng", "Tô Văn Phúc",
            "Phan Văn Cường", "Võ Đức Thái", "Trịnh Thị Liên", "Khương Văn Tuấn",
        ]
        
        student_ids = []
        current_year = datetime.now().year
        
        for i, name in enumerate(vietnamese_names):
            gender = "Nam" if i % 2 == 0 else "Nữ"
            year_of_birth = current_year - 15 - (i % 3)
            month = (i % 12) + 1
            day = (i % 28) + 1
            
            email = f"student{i+1:03d}@student.edu.vn"
            phone = f"098765{4321 - i:04d}"
            address = f"Số {i+1}, Phường {(i%10)+1}, Quận {(i%5)+1}, TP. Hồ Chí Minh"
            
            try:
                cursor.execute(
                    "INSERT INTO students (name, date_of_birth, gender, email, phone, address, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, date(year_of_birth, month, day), gender, email, phone, address, datetime.now())
                )
                student_ids.append(cursor.lastrowid)
            except mysql.connector.Error as e:
                if "Duplicate entry" in str(e):
                    print(f"  ⚠ Student email '{email}' already exists")
                else:
                    raise
        
        conn.commit()
        print(f"✓ Added {len(student_ids)} students")
        
        # 5. Add Enrollments (link students to classes)
        print("\n📋 Adding enrollments...")
        enrollments = 0
        students_per_class = len(student_ids) // len(class_ids)
        
        for class_idx, class_id in enumerate(class_ids):
            start_idx = class_idx * students_per_class
            end_idx = start_idx + students_per_class if class_idx < len(class_ids) - 1 else len(student_ids)
            
            for student_idx in range(start_idx, end_idx):
                cursor.execute(
                    "INSERT INTO enrollments (student_id, class_id, semester, created_at) VALUES (%s, %s, %s, %s)",
                    (student_ids[student_idx], class_id, "2024-2025", datetime.now())
                )
                enrollments += 1
        
        conn.commit()
        print(f"✓ Added {enrollments} enrollments")
        
        # 6. Add Scores
        print("\n📊 Adding scores...")
        score_count = 0
        
        for student_id in student_ids:
            for subject_id in subject_ids[:8]:  # Assign scores for main subjects
                # Random teacher
                teacher_id = teacher_ids[subject_ids.index(subject_id) % len(teacher_ids)]
                
                # Generate realistic scores
                midterm = round(random.uniform(4.0, 10.0), 2)
                final = round(random.uniform(4.0, 10.0), 2)
                average = round((midterm + final) / 2, 2)
                
                cursor.execute(
                    "INSERT INTO scores (student_id, subject_id, midterm_score, final_score, score_value, semester, teacher_id, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (student_id, subject_id, midterm, final, average, "2024-2025", teacher_id, datetime.now())
                )
                score_count += 1
        
        conn.commit()
        print(f"✓ Added {score_count} scores")
        
        print("\n✅ Database seeding completed successfully!")
        print(f"\nSummary:")
        print(f"  - Teachers: {len(teacher_ids)}")
        print(f"  - Classes: {len(class_ids)}")
        print(f"  - Subjects: {len(subject_ids)}")
        print(f"  - Students: {len(student_ids)}")
        print(f"  - Enrollments: {enrollments}")
        print(f"  - Scores: {score_count}")
        
    except mysql.connector.Error as e:
        print(f"❌ Error seeding database: {e}")
        conn.rollback()
        raise
    finally:
        DatabaseConnection.close_connection()


if __name__ == "__main__":
    seed_database()

