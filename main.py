"""
Lecturer-Student Management System - Main Application
A comprehensive mobile app for classroom management

Author: Abhishek R Sanganal
Date: February 2026
"""

from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from database import Database

# Set window size for desktop testing
Window.size = (400, 700)

# Global variables
current_user = None
db = Database()


class LoginScreen(Screen):
    """Login screen for both lecturers and students"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        layout.add_widget(Label(
            text='Lecturer-Student\nManagement System',
            font_size='24sp',
            size_hint=(1, 0.2),
            halign='center'
        ))
        
        # Email input
        layout.add_widget(Label(text='Email:', size_hint=(1, 0.1)))
        self.email_input = TextInput(
            multiline=False,
            size_hint=(1, 0.1),
            hint_text='Enter your email'
        )
        layout.add_widget(self.email_input)
        
        # Password input
        layout.add_widget(Label(text='Password:', size_hint=(1, 0.1)))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            size_hint=(1, 0.1),
            hint_text='Enter your password'
        )
        layout.add_widget(self.password_input)
        
        # Login button
        login_btn = Button(
            text='Login',
            size_hint=(1, 0.12),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        login_btn.bind(on_press=self.login)
        layout.add_widget(login_btn)
        
        # Register button
        register_btn = Button(
            text='Register as Student',
            size_hint=(1, 0.12),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        register_btn.bind(on_press=self.go_to_register)
        layout.add_widget(register_btn)
        
        self.add_widget(layout)
    
    def login(self, instance):
        """Handle login"""
        global current_user
        
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        
        if not email or not password:
            self.show_popup('Error', 'Please fill all fields')
            return
        
        success, user = db.login(email, password)
        
        if success:
            current_user = user  # Set global variable
            App.get_running_app().current_user = user  # Also set on app instance
            if user['role'] == 'lecturer':
                self.manager.current = 'lecturer_dashboard'
            else:
                self.manager.current = 'student_dashboard'
        else:
            self.show_popup('Error', 'Invalid email or password')
    
    def go_to_register(self, instance):
        """Navigate to registration screen"""
        self.manager.current = 'register'
    
    def show_popup(self, title, message):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class RegisterScreen(Screen):
    """Student registration screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'register'
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Title
        layout.add_widget(Label(
            text='Student Registration',
            font_size='24sp',
            size_hint=(1, 0.15)
        ))
        
        # Form fields
        layout.add_widget(Label(text='Name:', size_hint=(1, 0.08)))
        self.name_input = TextInput(multiline=False, size_hint=(1, 0.08))
        layout.add_widget(self.name_input)
        
        layout.add_widget(Label(text='Roll Number:', size_hint=(1, 0.08)))
        self.roll_input = TextInput(multiline=False, size_hint=(1, 0.08))
        layout.add_widget(self.roll_input)
        
        layout.add_widget(Label(text='Email:', size_hint=(1, 0.08)))
        self.email_input = TextInput(multiline=False, size_hint=(1, 0.08))
        layout.add_widget(self.email_input)
        
        layout.add_widget(Label(text='Phone:', size_hint=(1, 0.08)))
        self.phone_input = TextInput(multiline=False, size_hint=(1, 0.08))
        layout.add_widget(self.phone_input)
        
        layout.add_widget(Label(text='Password:', size_hint=(1, 0.08)))
        self.password_input = TextInput(multiline=False, password=True, size_hint=(1, 0.08))
        layout.add_widget(self.password_input)
        
        # Register button
        register_btn = Button(
            text='Register',
            size_hint=(1, 0.1),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        register_btn.bind(on_press=self.register)
        layout.add_widget(register_btn)
        
        # Back button
        back_btn = Button(text='Back to Login', size_hint=(1, 0.1))
        back_btn.bind(on_press=self.go_back)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
    
    def register(self, instance):
        """Handle registration"""
        name = self.name_input.text.strip()
        roll = self.roll_input.text.strip()
        email = self.email_input.text.strip()
        phone = self.phone_input.text.strip()
        password = self.password_input.text.strip()
        
        if not all([name, roll, email, phone, password]):
            self.show_popup('Error', 'Please fill all fields')
            return
        
        success, message = db.register_student(name, email, password, phone, roll)
        
        if success:
            self.show_popup('Success', 'Registration successful! Please login.')
            self.manager.current = 'login'
        else:
            self.show_popup('Error', message)
    
    def go_back(self, instance):
        """Go back to login"""
        self.manager.current = 'login'
    
    def show_popup(self, title, message):
        """Show popup message"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()


class LecturerDashboard(Screen):
    """Main dashboard for lecturer"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'lecturer_dashboard'
        self.build_ui()
    
    def build_ui(self):
        """Build the UI"""
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text=f'Welcome, Lecturer',
            font_size='20sp',
            size_hint=(1, 0.1)
        )
        layout.add_widget(header)
        
        # Menu buttons
        buttons = [
            ('Announcements', self.open_announcements),
            ('Resources', self.open_resources),
            ('Assignments', self.open_assignments),
            ('Test Marks', self.open_tests),
            ('Student Management', self.open_students),
            ('Q & A', self.open_qa),
            ('Logout', self.logout)
        ]
        
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.12),
                background_color=(0.2, 0.6, 0.8, 1)
            )
            btn.bind(on_press=callback)
            layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def open_announcements(self, instance):
        """Open announcements screen"""
        self.manager.current = 'announcements'
    
    def open_resources(self, instance):
        """Open resources screen"""
        self.manager.current = 'resources'
    
    def open_assignments(self, instance):
        """Open assignments screen"""
        self.manager.current = 'assignments'
    
    def open_tests(self, instance):
        """Open tests screen"""
        self.manager.current = 'tests'
    
    def open_students(self, instance):
        """Open student management screen"""
        self.manager.current = 'students'
    
    def open_qa(self, instance):
        """Open Q&A screen"""
        self.manager.current = 'qa'
    
    def logout(self, instance):
        """Logout"""
        global current_user
        current_user = None
        self.manager.current = 'login'


class StudentDashboard(Screen):
    """Main dashboard for student"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'student_dashboard'
        self.build_ui()
    
    def build_ui(self):
        """Build the UI"""
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text=f'Welcome, Student',
            font_size='20sp',
            size_hint=(1, 0.1)
        )
        layout.add_widget(header)
        
        # Menu buttons
        buttons = [
            ('View Announcements', self.view_announcements),
            ('View Resources', self.view_resources),
            ('View Assignments', self.view_assignments),
            ('View Test Marks', self.view_marks),
            ('Ask Question', self.ask_question),
            ('Logout', self.logout)
        ]
        
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.14),
                background_color=(0.3, 0.7, 0.3, 1)
            )
            btn.bind(on_press=callback)
            layout.add_widget(btn)
        
        self.add_widget(layout)
    
    def view_announcements(self, instance):
        """View announcements"""
        self.manager.current = 'view_announcements'
    
    def view_resources(self, instance):
        """View resources"""
        self.manager.current = 'view_resources'
    
    def view_assignments(self, instance):
        """View assignments"""
        self.manager.current = 'view_assignments'
    
    def view_marks(self, instance):
        """View test marks"""
        self.manager.current = 'view_marks'
    
    def ask_question(self, instance):
        """Ask question"""
        self.manager.current = 'ask_question'
    
    def logout(self, instance):
        """Logout"""
        global current_user
        current_user = None
        self.manager.current = 'login'


class LecturerStudentApp(App):
    """Main application class"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None  # Store current_user in app instance
    
    def build(self):
        """Build the application"""
        from screens import (
            AnnouncementsScreen, ResourcesScreen, AssignmentsScreen,
            TestsScreen, StudentsScreen, QAScreen,
            ViewAnnouncementsScreen, ViewResourcesScreen, ViewAssignmentsScreen,
            ViewMarksScreen, AskQuestionScreen
        )
        
        sm = ScreenManager()
        
        # Add authentication screens
        sm.add_widget(LoginScreen())
        sm.add_widget(RegisterScreen())
        
        # Add dashboard screens
        sm.add_widget(LecturerDashboard())
        sm.add_widget(StudentDashboard())
        
        # Add lecturer screens
        sm.add_widget(AnnouncementsScreen())
        sm.add_widget(ResourcesScreen())
        sm.add_widget(AssignmentsScreen())
        sm.add_widget(TestsScreen())
        sm.add_widget(StudentsScreen())
        sm.add_widget(QAScreen())
        
        # Add student screens
        sm.add_widget(ViewAnnouncementsScreen())
        sm.add_widget(ViewResourcesScreen())
        sm.add_widget(ViewAssignmentsScreen())
        sm.add_widget(ViewMarksScreen())
        sm.add_widget(AskQuestionScreen())
        
        return sm


if __name__ == '__main__':
    LecturerStudentApp().run()
