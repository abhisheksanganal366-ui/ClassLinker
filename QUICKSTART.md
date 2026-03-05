# 🚀 Quick Start Guide

## Installation (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python main.py
```

## First Login (30 seconds)

### As Lecturer
```
Email: lecturer@app.com
Password: lecturer123
```

### As Student
1. Click "Register as Student"
2. Fill the form
3. Login with your credentials

## Quick Feature Tour (5 minutes)

### Lecturer Workflow

1. **Add an Announcement**
   - Dashboard → Announcements → + Add Announcement
   - Enter title and content → Add

2. **Upload a Resource**
   - Dashboard → Resources → + Add Resource
   - Fill details → Add

3. **Create an Assignment**
   - Dashboard → Assignments → + Create Assignment
   - Enter details → Create
   - Click "Manage Submissions" to mark and grade

4. **Add a Test**
   - Dashboard → Test Marks → + Add Test
   - Enter test name and total marks → Add
   - Click "Enter/Edit Marks" to grade students

5. **Add a Student**
   - Dashboard → Student Management → + Add Student
   - Fill student details → Add
   - (Default password: student123)

6. **Answer Questions**
   - Dashboard → Q & A
   - Click "Reply" on any question → Submit

### Student Workflow

1. **Register**
   - Login screen → Register as Student
   - Fill all fields → Register

2. **View Content**
   - View Announcements - See all updates
   - View Resources - Search and access materials
   - View Assignments - Check status and marks
   - View Test Marks - See your scores

3. **Ask Questions**
   - Ask Question → Type your question → Submit
   - Check back later for lecturer's answer

## Build for Android (5 minutes)

```bash
# On Linux/WSL
buildozer android debug

# APK will be in bin/ folder
```

## Troubleshooting

**Issue:** Module not found
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Issue:** Permission denied
```bash
chmod +x main.py
python main.py
```

**Issue:** Database locked
- Close all app instances
- Delete `lecturer_student.db` (will recreate)
- Restart app

## File Structure

```
📁 Project Root
├── 📄 main.py              ← Start here
├── 📄 database.py          ← Database operations
├── 📄 screens.py           ← All UI screens
├── 📄 requirements.txt     ← Dependencies
└── 📄 README.md            ← Full documentation
```

## Key Features at a Glance

| Feature | Lecturer | Student |
|---------|----------|---------|
| Announcements | ✏️ Create/Edit/Delete | 👁️ View Only |
| Resources | ✏️ Upload/Manage | 👁️ View/Search |
| Assignments | ✏️ Create/Grade | 👁️ View Status |
| Test Marks | ✏️ Add/Edit | 👁️ View Scores |
| Students | ✏️ Add/Edit/Delete | ❌ No Access |
| Q&A | ✏️ Reply/Delete | ✏️ Ask Questions |

## Default Passwords

- **Lecturer:** lecturer123
- **Students (added by lecturer):** student123
- **Students (self-registered):** Their chosen password

## Database Location

The SQLite database is created automatically:
- **File:** `lecturer_student.db`
- **Location:** Same folder as main.py

## Support

For detailed testing instructions, see [TESTING_GUIDE.md](TESTING_GUIDE.md)

For full documentation, see [README.md](README.md)

---

**Ready to go! Start with:** `python main.py` 🎉
