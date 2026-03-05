# 📱 Lecturer-Student Management System

A comprehensive mobile application for managing classroom activities, built with **Python** and **Kivy** framework. This app provides role-based access for Lecturers and Students with complete classroom management features.

## ✨ Features

### 👩‍🏫 Lecturer Features
- 📢 **Announcements** - Create, edit, delete announcements with timestamps
- 📚 **Resources** - Upload and manage study materials (PDF, PPT, Notes, Video links)
- 📝 **Assignments** - Create assignments, track submissions, and assign marks
- 📊 **Test Marks** - Add, edit, and manage test scores
- 👥 **Student Management** - Add, edit, delete student records
- ❓ **Q&A Dashboard** - View and respond to student questions

### 👨‍🎓 Student Features
- 📢 View announcements
- 📚 Search and access resources
- 📝 View assignments and submission status
- 📊 Check test marks and grades
- ❓ Ask questions and view lecturer responses
- 🔐 Secure login and registration

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/[your-username]/lecturer-student-manager.git
cd lecturer-student-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the App

#### Desktop Testing (Windows/Mac/Linux)
```bash
python main.py
```

#### Building for Android

**Note:** Building APK requires a Linux environment (WSL on Windows or native Linux/Mac).

1. Install Buildozer:
```bash
pip install buildozer
```

2. Build the APK:
```bash
buildozer android debug
```

3. The APK will be generated in the `bin/` folder.

4. Deploy to connected Android device:
```bash
buildozer android debug deploy run
```

## 📂 Project Structure

```
lecturer-student-manager/
├── main.py                    # Main application entry point
├── database.py                # SQLite database operations
├── screens.py                 # All UI screens
├── buildozer.spec             # Android build configuration
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── TESTING_GUIDE.md          # Comprehensive testing guide
├── IMPLEMENTATION_STATUS.md   # Development status
├── CONTRIBUTING.md            # Contribution guidelines
└── LICENSE                    # MIT License
```

## 🎓 Default Login Credentials

### Lecturer Account
- Email: `lecturer@app.com`
- Password: `lecturer123`

### Student Account
- Register through the app or
- Added by lecturer (default password: `student123`)

## 🔐 Security Features

- Password hashing using SHA256
- Role-based access control
- Secure authentication system
- Students cannot access lecturer features
- Data validation on all inputs

## 🛠️ Technologies Used

- **Python 3.8+** - Programming language
- **Kivy 2.3.0** - Cross-platform UI framework
- **SQLite** - Embedded database for data persistence
- **Buildozer** - Android packaging tool
- **SHA256** - Password hashing for security

## 💡 Key Features Explained

### Database-Based Assignment System
Unlike traditional file upload systems, this app uses a database approach where:
- Lecturers manually mark submissions as "Submitted" or "Not Submitted"
- Marks are entered directly into the system
- No file storage required - perfect for mobile devices
- Instant updates and real-time tracking

### Real-Time Q&A System
- Students post questions instantly
- Lecturers see all questions in dedicated dashboard
- Answers are immediately visible to students
- Complete question history maintained

### Resource Management
- Support for multiple file types (PDF, PPT, Notes, Videos)
- Searchable by resource name
- Direct links to external resources
- No local file storage needed

## 📱 Screenshots

*Screenshots will be added after testing*

## 🧪 Testing

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive testing instructions.

Quick test:
```bash
python main.py
# Login with: lecturer@app.com / lecturer123
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Abhishek R Sanganal**

- GitHub: [@your-github-username](https://github.com/your-github-username)

## 🌟 Show your support

Give a ⭐️ if you like this project!

## 📚 Documentation

- [Quick Start Guide](QUICKSTART.md) - Get started in 2 minutes
- [Testing Guide](TESTING_GUIDE.md) - Comprehensive testing instructions
- [Implementation Status](IMPLEMENTATION_STATUS.md) - Development details
- [Project Summary](PROJECT_SUMMARY.md) - Complete project overview
- [Deployment Checklist](DEPLOYMENT_CHECKLIST.md) - GitHub upload guide

## 📚 Learn More

- [Kivy Documentation](https://kivy.org/doc/stable/)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Python Official Docs](https://docs.python.org/3/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
