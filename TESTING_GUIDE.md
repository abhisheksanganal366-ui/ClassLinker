# Testing Guide - Lecturer-Student Management System

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python main.py
```

## Test Accounts

### Default Lecturer Account
- Email: admin@123
- Password: 1234

### Student Accounts
Students need to register through the app or can be added by the lecturer.

Default password for lecturer-added students: student123

## Testing Scenarios

### For Lecturer Role

#### 1. Login
- Use default lecturer credentials
- Should navigate to Lecturer Dashboard

#### 2. Announcements
- Click "Announcements"
- Add a new announcement with title and content
- Edit an existing announcement
- Delete an announcement
- Verify all announcements show with timestamps

#### 3. Resources
- Click "Resources"
- Add a resource with:
  - Name: "Python Tutorial"
  - Description: "Complete Python guide"
  - Type: PDF
  - Link: "https://example.com/python.pdf"
- Verify resource appears in list

#### 4. Assignments
- Click "Assignments"
- Create assignment:
  - Title: "Assignment 1"
  - Description: "Complete exercises 1-10"
  - Due Date: 2026-03-01
  - Total Marks: 100
- Click "Manage Submissions"
- Change student status to "Submitted"
- Enter marks (e.g., 85)
- Click "Update"

#### 5. Test Marks
- Click "Test Marks"
- Add test:
  - Test Name: "Mid-term Exam"
  - Total Marks: 100
- Click "Enter/Edit Marks"
- Enter marks for each student
- Click "Update"

#### 6. Student Management
- Click "Student Management"
- Add student:
  - Name: "John Doe"
  - Roll Number: "CS001"
  - Email: "john@student.com"
  - Phone: "1234567890"
- Edit student details
- Delete a student (test only)

#### 7. Q&A
- Click "Q & A"
- View questions from students
- Click "Reply" on a question
- Enter answer and submit
- Delete a question

### For Student Role

#### 1. Registration
- Click "Register as Student"
- Fill all fields:
  - Name: "Jane Smith"
  - Roll Number: "CS002"
  - Email: "jane@student.com"
  - Phone: "0987654321"
  - Password: "password123"
- Click "Register"

#### 2. Login
- Use registered credentials
- Should navigate to Student Dashboard

#### 3. View Announcements
- Click "View Announcements"
- See all announcements posted by lecturer
- Verify read-only access

#### 4. View Resources
- Click "View Resources"
- See all resources
- Test search functionality:
  - Enter "Python" in search box
  - Click "Search"
  - Should filter results

#### 5. View Assignments
- Click "View Assignments"
- See all assignments
- Check submission status
- View marks received

#### 6. View Test Marks
- Click "View Test Marks"
- See all test scores
- Verify percentage calculation

#### 7. Ask Question
- Click "Ask Question"
- Type question: "What is the deadline for Assignment 1?"
- Click "Submit Question"
- View previous questions and answers

## Database Verification

The app creates a SQLite database file: `lecturer_student.db`

To inspect the database:
```bash
sqlite3 lecturer_student.db
.tables
SELECT * FROM users;
SELECT * FROM announcements;
```

## Testing on Android

### Build APK
```bash
buildozer android debug
```

### Install on Device
```bash
buildozer android debug deploy run
```

## Feature Checklist

### Lecturer Features
- [ ] Login with default account
- [ ] Create/Edit/Delete announcements
- [ ] Add resources with all fields
- [ ] Create assignments
- [ ] Mark submissions and assign marks
- [ ] Add tests and enter marks
- [ ] Add/Edit/Delete students
- [ ] Reply to student questions
- [ ] Delete questions

### Student Features
- [ ] Register new account
- [ ] Login successfully
- [ ] View all announcements
- [ ] Search and view resources
- [ ] View assignments and status
- [ ] View test marks with percentage
- [ ] Ask questions
- [ ] View answers from lecturer

### Security
- [ ] Passwords are hashed
- [ ] Students cannot access lecturer features
- [ ] Students cannot edit/delete content
- [ ] Role-based access control works

### Data Persistence
- [ ] Data survives app restart
- [ ] All CRUD operations work
- [ ] Timestamps are recorded correctly
- [ ] Relationships between tables work

## Common Issues

### Issue: "No module named 'kivy'"
Solution: Run `pip install -r requirements.txt`

### Issue: Database locked
Solution: Close all instances of the app and restart

### Issue: Screen doesn't update
Solution: The `on_enter()` method rebuilds UI automatically

### Issue: Buildozer fails on Windows
Solution: Use WSL (Windows Subsystem for Linux) for building APK

## Performance Testing

- Test with 50+ students
- Test with 100+ announcements
- Test search with large datasets
- Verify scroll performance

## Success Criteria

All features work as specified
No crashes or errors
Data persists correctly
UI is responsive and intuitive
Role-based access is enforced
Search functionality works
Marks calculation is accurate

## Notes

- Default window size for desktop: 400x700 (mobile-like)
- Database file is created automatically
- All dates use YYYY-MM-DD format
- Marks are integers only
- Email must be unique for each user
