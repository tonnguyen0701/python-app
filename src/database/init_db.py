# Database Initialization
# Create tables and initialize database schema

import mysql.connector
from .db_connect import DatabaseConnection


def clear_database():
    """Clear all tables and data from the database."""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        cursor.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_SCHEMA = %s",
            (DatabaseConnection.DB_CONFIG["database"],),
        )
        tables = [row[0] for row in cursor.fetchall()]
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS `{table}`")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        conn.commit()
        print("Database cleared successfully!")
    except mysql.connector.Error as e:
        print(f"Error clearing database: {e}")
        conn.rollback()
    finally:
        DatabaseConnection.close_connection()


def init_database():
    """Initialize database with tables"""
    conn = DatabaseConnection.get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                date_of_birth DATE,
                gender VARCHAR(20),
                email VARCHAR(255) UNIQUE,
                phone VARCHAR(50),
                address VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                subject_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                code VARCHAR(50) NOT NULL UNIQUE,
                credit INT,
                class_name VARCHAR(255),
                class_shift VARCHAR(255),
                class_day VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        cursor.execute("SHOW COLUMNS FROM subjects")
        existing_columns = {row[0] for row in cursor.fetchall()}
        if "class_name" not in existing_columns:
            cursor.execute("ALTER TABLE subjects ADD COLUMN class_name VARCHAR(255)")
        if "class_shift" not in existing_columns:
            cursor.execute("ALTER TABLE subjects ADD COLUMN class_shift VARCHAR(255)")
        if "class_day" not in existing_columns:
            cursor.execute("ALTER TABLE subjects ADD COLUMN class_day VARCHAR(255)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS semesters (
                semester_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                start_date DATE,
                end_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE,
                phone VARCHAR(50),
                department VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                score_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT NOT NULL,
                subject_id INT NOT NULL,
                score_value DOUBLE NOT NULL,
                midterm_score DOUBLE DEFAULT 0,
                final_score DOUBLE DEFAULT 0,
                semester VARCHAR(100),
                teacher_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        cursor.execute("SHOW COLUMNS FROM scores")
        score_columns = {row[0] for row in cursor.fetchall()}
        if "midterm_score" not in score_columns:
            cursor.execute("ALTER TABLE scores ADD COLUMN midterm_score DOUBLE DEFAULT 0")
        if "final_score" not in score_columns:
            cursor.execute("ALTER TABLE scores ADD COLUMN final_score DOUBLE DEFAULT 0")
        if "teacher_id" not in score_columns:
            cursor.execute("ALTER TABLE scores ADD COLUMN teacher_id INT")
            cursor.execute("ALTER TABLE scores ADD FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                class_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL UNIQUE,
                grade_level INT,
                homeroom_teacher_id INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (homeroom_teacher_id) REFERENCES teachers(teacher_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT NOT NULL,
                class_id INT NOT NULL,
                semester VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(student_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher_subjects (
                id INT PRIMARY KEY AUTO_INCREMENT,
                teacher_id INT NOT NULL,
                subject_id INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher_class_permissions (
                permission_id INT PRIMARY KEY AUTO_INCREMENT,
                teacher_id INT NOT NULL,
                class_id INT NOT NULL,
                subject_id INT NOT NULL,
                can_enter_score BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_teacher_class_subject (teacher_id, class_id, subject_id),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
                FOREIGN KEY (class_id) REFERENCES classes(class_id),
                FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        conn.commit()
        print("✓ Database initialized successfully!")
        
    except mysql.connector.Error as e:
        print(f"❌ Error initializing database: {e}")
        conn.rollback()
    finally:
        DatabaseConnection.close_connection()


if __name__ == "__main__":
    init_database()
