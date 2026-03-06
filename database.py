"""
Database Module for Lecturer-Student Management System
Handles all database operations using SQLite

Author: Abhishek R Sanganal
Date: February 2026
"""

import sqlite3
from datetime import datetime
import hashlib


class Database:
    """Database handler for the application"""
    
    def __init__(self, db_name='lecturer_student.db'):
        self.db_name = db_name
        self.create_tables()
    
    def get_connection(self):
        """Create and return database connection"""
        return sqlite3.connect(self.db_name)
    
    def create_tables(self):
        """Create all required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table (Lecturers and Students)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                phone TEXT,
                roll_number TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Announcements table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                lecturer_id INTEGER,
                created_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                updated_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (lecturer_id) REFERENCES users(id)
            )
        ''')
        
        # Resources table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                file_type TEXT,
                file_link TEXT,
                lecturer_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lecturer_id) REFERENCES users(id)
            )
        ''')
        
        # Assignments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date DATE,
                total_marks INTEGER,
                lecturer_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lecturer_id) REFERENCES users(id)
            )
        ''')
        
        # Assignment submissions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assignment_submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                assignment_id INTEGER,
                student_id INTEGER,
                status TEXT DEFAULT 'Not Submitted',
                marks INTEGER DEFAULT 0,
                submitted_at TIMESTAMP,
                FOREIGN KEY (assignment_id) REFERENCES assignments(id),
                FOREIGN KEY (student_id) REFERENCES users(id)
            )
        ''')
        
        # Tests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT NOT NULL,
                total_marks INTEGER,
                lecturer_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lecturer_id) REFERENCES users(id)
            )
        ''')
        
        # Test marks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER,
                student_id INTEGER,
                marks INTEGER,
                FOREIGN KEY (test_id) REFERENCES tests(id),
                FOREIGN KEY (student_id) REFERENCES users(id)
            )
        ''')
        
        # Q&A table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                question TEXT NOT NULL,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                answered_at TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id)
            )
        ''')
        
        # Announcement views table (track which students have seen which announcements)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS announcement_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                announcement_id INTEGER,
                student_id INTEGER,
                viewed_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (announcement_id) REFERENCES announcements(id),
                FOREIGN KEY (student_id) REFERENCES users(id),
                UNIQUE(announcement_id, student_id)
            )
        ''')
        
        # Question views table (track which lecturers have seen which questions)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS question_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER,
                lecturer_id INTEGER,
                viewed_at TIMESTAMP DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (question_id) REFERENCES questions(id),
                FOREIGN KEY (lecturer_id) REFERENCES users(id),
                UNIQUE(question_id, lecturer_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Create default lecturer account
        self.create_default_lecturer()
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_default_lecturer(self):
        """Create default lecturer account if not exists"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE email = 'admin@123'")
        if not cursor.fetchone():
            hashed_pw = self.hash_password('1234')
            cursor.execute('''
                INSERT INTO users (name, email, password, role, phone)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Default Lecturer', 'admin@123', hashed_pw, 'lecturer', '1234567890'))
            conn.commit()
        
        conn.close()
    
    # User Management
    def register_student(self, name, email, password, phone, roll_number):
        """Register a new student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            hashed_pw = self.hash_password(password)
            
            cursor.execute('''
                INSERT INTO users (name, email, password, role, phone, roll_number)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, email, hashed_pw, 'student', phone, roll_number))
            
            conn.commit()
            conn.close()
            return True, "Registration successful"
        except sqlite3.IntegrityError:
            return False, "Email already exists"
        except Exception as e:
            return False, str(e)
    
    def login(self, email, password):
        """Login user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        hashed_pw = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, name, email, role FROM users 
            WHERE email = ? AND password = ?
        ''', (email, hashed_pw))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return True, {
                'id': user[0],
                'name': user[1],
                'email': user[2],
                'role': user[3]
            }
        return False, None
    
    def get_all_students(self):
        """Get all students"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, roll_number, email, phone 
            FROM users WHERE role = 'student'
            ORDER BY name
        ''')
        
        students = cursor.fetchall()
        conn.close()
        return students
    
    def add_student(self, name, email, phone, roll_number):
        """Add student by lecturer"""
        default_password = 'student123'
        return self.register_student(name, email, default_password, phone, roll_number)
    
    def update_student(self, student_id, name, email, phone, roll_number):
        """Update student details"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE users 
                SET name = ?, email = ?, phone = ?, roll_number = ?
                WHERE id = ? AND role = 'student'
            ''', (name, email, phone, roll_number, student_id))
            
            conn.commit()
            conn.close()
            return True, "Student updated successfully"
        except Exception as e:
            return False, str(e)
    
    def delete_student(self, student_id):
        """Delete student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM users WHERE id = ? AND role = "student"', (student_id,))
            
            conn.commit()
            conn.close()
            return True, "Student deleted successfully"
        except Exception as e:
            return False, str(e)

    # Announcements
    def add_announcement(self, title, content, lecturer_id):
        """Add new announcement"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO announcements (title, content, lecturer_id)
            VALUES (?, ?, ?)
        ''', (title, content, lecturer_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_announcements(self):
        """Get all announcements"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.title, a.content, a.created_at, u.name
            FROM announcements a
            JOIN users u ON a.lecturer_id = u.id
            ORDER BY a.created_at DESC
        ''')
        
        announcements = cursor.fetchall()
        conn.close()
        return announcements
    
    def update_announcement(self, announcement_id, title, content):
        """Update announcement"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE announcements 
            SET title = ?, content = ?, updated_at = datetime('now', 'localtime')
            WHERE id = ?
        ''', (title, content, announcement_id))
        
        conn.commit()
        conn.close()
        return True
    
    def delete_announcement(self, announcement_id):
        """Delete announcement"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM announcements WHERE id = ?', (announcement_id,))
        
        conn.commit()
        conn.close()
        return True
    
    # Resources
    def add_resource(self, name, description, file_type, file_link, lecturer_id):
        """Add new resource"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO resources (name, description, file_type, file_link, lecturer_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, description, file_type, file_link, lecturer_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_resources(self):
        """Get all resources"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, file_type, file_link, created_at
            FROM resources
            ORDER BY created_at DESC
        ''')
        
        resources = cursor.fetchall()
        conn.close()
        return resources
    
    def search_resources(self, search_term):
        """Search resources by name"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, description, file_type, file_link, created_at
            FROM resources
            WHERE name LIKE ?
            ORDER BY created_at DESC
        ''', (f'%{search_term}%',))
        
        resources = cursor.fetchall()
        conn.close()
        return resources
    
    def delete_resource(self, resource_id):
        """Delete a resource"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM resources WHERE id = ?', (resource_id,))
        
        conn.commit()
        conn.close()
        return True
    
    # Assignments
    def add_assignment(self, title, description, due_date, total_marks, lecturer_id):
        """Add new assignment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO assignments (title, description, due_date, total_marks, lecturer_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, due_date, total_marks, lecturer_id))
        
        assignment_id = cursor.lastrowid
        
        # Create submission entries for all students
        cursor.execute('SELECT id FROM users WHERE role = "student"')
        students = cursor.fetchall()
        
        for student in students:
            cursor.execute('''
                INSERT INTO assignment_submissions (assignment_id, student_id, status)
                VALUES (?, ?, 'Not Submitted')
            ''', (assignment_id, student[0]))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_assignments(self):
        """Get all assignments"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, description, due_date, total_marks, created_at
            FROM assignments
            ORDER BY due_date DESC
        ''')
        
        assignments = cursor.fetchall()
        conn.close()
        return assignments
    
    def get_assignment_submissions(self, assignment_id):
        """Get all submissions for an assignment"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT s.id, u.name, u.roll_number, s.status, s.marks
            FROM assignment_submissions s
            JOIN users u ON s.student_id = u.id
            WHERE s.assignment_id = ?
            ORDER BY u.name
        ''', (assignment_id,))
        
        submissions = cursor.fetchall()
        conn.close()
        return submissions
    
    def update_submission_status(self, submission_id, status, marks=None):
        """Update assignment submission status and marks"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if marks is not None:
            cursor.execute('''
                UPDATE assignment_submissions 
                SET status = ?, marks = ?, submitted_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (status, marks, submission_id))
        else:
            cursor.execute('''
                UPDATE assignment_submissions 
                SET status = ?
                WHERE id = ?
            ''', (status, submission_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_student_assignments(self, student_id):
        """Get assignments for a student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.title, a.description, a.due_date, a.total_marks,
                   s.status, s.marks
            FROM assignments a
            LEFT JOIN assignment_submissions s ON a.id = s.assignment_id 
                AND s.student_id = ?
            ORDER BY a.due_date DESC
        ''', (student_id,))
        
        assignments = cursor.fetchall()
        conn.close()
        return assignments
    
    # Tests
    def add_test(self, test_name, total_marks, lecturer_id):
        """Add new test"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tests (test_name, total_marks, lecturer_id)
            VALUES (?, ?, ?)
        ''', (test_name, total_marks, lecturer_id))
        
        test_id = cursor.lastrowid
        
        # Create mark entries for all students
        cursor.execute('SELECT id FROM users WHERE role = "student"')
        students = cursor.fetchall()
        
        for student in students:
            cursor.execute('''
                INSERT INTO test_marks (test_id, student_id, marks)
                VALUES (?, ?, 0)
            ''', (test_id, student[0]))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_tests(self):
        """Get all tests"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, test_name, total_marks, created_at
            FROM tests
            ORDER BY created_at DESC
        ''')
        
        tests = cursor.fetchall()
        conn.close()
        return tests
    
    def get_test_marks(self, test_id):
        """Get marks for a test"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT tm.id, u.name, u.roll_number, tm.marks, t.total_marks
            FROM test_marks tm
            JOIN users u ON tm.student_id = u.id
            JOIN tests t ON tm.test_id = t.id
            WHERE tm.test_id = ?
            ORDER BY u.name
        ''', (test_id,))
        
        marks = cursor.fetchall()
        conn.close()
        return marks
    
    def update_test_marks(self, mark_id, marks):
        """Update test marks"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE test_marks 
            SET marks = ?
            WHERE id = ?
        ''', (marks, mark_id))
        
        conn.commit()
        conn.close()
        return True
    
    def get_student_test_marks(self, student_id):
        """Get all test marks for a student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.test_name, tm.marks, t.total_marks, t.created_at
            FROM test_marks tm
            JOIN tests t ON tm.test_id = t.id
            WHERE tm.student_id = ?
            ORDER BY t.created_at DESC
        ''', (student_id,))
        
        marks = cursor.fetchall()
        conn.close()
        return marks
    
    # Q&A
    def add_question(self, student_id, question):
        """Add new question"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO questions (student_id, question)
            VALUES (?, ?)
        ''', (student_id, question))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_questions(self):
        """Get all questions"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT q.id, u.name, u.roll_number, q.question, q.answer, q.created_at
            FROM questions q
            JOIN users u ON q.student_id = u.id
            ORDER BY q.created_at DESC
        ''')
        
        questions = cursor.fetchall()
        conn.close()
        return questions
    
    def answer_question(self, question_id, answer):
        """Answer a question"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE questions 
            SET answer = ?, answered_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (answer, question_id))
        
        conn.commit()
        conn.close()
        return True
    
    def delete_question(self, question_id):
        """Delete question"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM questions WHERE id = ?', (question_id,))
        
        conn.commit()
        conn.close()
        return True
    
    def get_student_questions(self, student_id):
        """Get questions asked by a student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, question, answer, created_at, answered_at
            FROM questions
            WHERE student_id = ?
            ORDER BY created_at DESC
        ''', (student_id,))
        
        questions = cursor.fetchall()
        conn.close()
        return questions

    # Notification/View tracking
    def mark_announcement_as_viewed(self, announcement_id, student_id):
        """Mark announcement as viewed by student"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO announcement_views (announcement_id, student_id)
                VALUES (?, ?)
            ''', (announcement_id, student_id))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def get_unviewed_announcements_count(self, student_id):
        """Get count of announcements not yet viewed by student"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*)
            FROM announcements a
            LEFT JOIN announcement_views av ON a.id = av.announcement_id AND av.student_id = ?
            WHERE av.id IS NULL
        ''', (student_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def is_announcement_viewed(self, announcement_id, student_id):
        """Check if student has viewed this announcement"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM announcement_views
            WHERE announcement_id = ? AND student_id = ?
        ''', (announcement_id, student_id))
        
        result = cursor.fetchone()
        conn.close()
        return result is not None
    
    def mark_question_as_viewed(self, question_id, lecturer_id):
        """Mark question as viewed by lecturer"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO question_views (question_id, lecturer_id)
                VALUES (?, ?)
            ''', (question_id, lecturer_id))
            
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def get_unviewed_questions_count(self, lecturer_id):
        """Get count of questions not yet viewed by lecturer"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*)
            FROM questions q
            LEFT JOIN question_views qv ON q.id = qv.question_id AND qv.lecturer_id = ?
            WHERE qv.id IS NULL
        ''', (lecturer_id,))
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def is_question_viewed(self, question_id, lecturer_id):
        """Check if lecturer has viewed this question"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id FROM question_views
            WHERE question_id = ? AND lecturer_id = ?
        ''', (question_id, lecturer_id))
        
        result = cursor.fetchone()
        conn.close()
        return result is not None
