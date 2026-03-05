"""
UI Screens for Lecturer-Student Management System

Author: Abhishek R Sanganal
Date: February 2026
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from database import Database
from kivy.app import App

db = Database()


def get_current_user():
    """Get current user from app"""
    app = App.get_running_app()
    return getattr(app, 'current_user', None)


class AnnouncementsScreen(Screen):
    """Lecturer announcements management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'announcements'
    
    def on_enter(self):
        """Called when screen is displayed"""
        self.build_ui()
    
    def build_ui(self):
        """Build the UI"""
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='Announcements', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=self.go_back)
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Add announcement button
        add_btn = Button(
            text='+ Add Announcement',
            size_hint=(1, 0.08),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        add_btn.bind(on_press=self.show_add_popup)
        layout.add_widget(add_btn)
        
        # Announcements list
        scroll = ScrollView(size_hint=(1, 0.82))
        self.announcements_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.announcements_layout.bind(
            minimum_height=self.announcements_layout.setter('height')
        )
        
        # Load announcements
        announcements = db.get_all_announcements()
        for ann in announcements:
            self.add_announcement_card(ann)
        
        scroll.add_widget(self.announcements_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def add_announcement_card(self, announcement):
        """Add announcement card to list"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=150,
            padding=10,
            spacing=5
        )
        
        # Title
        card.add_widget(Label(
            text=f"[b]{announcement[1]}[/b]",
            markup=True,
            size_hint_y=0.3,
            halign='left',
            valign='top'
        ))
        
        # Content
        card.add_widget(Label(
            text=announcement[2],
            size_hint_y=0.4,
            halign='left',
            valign='top',
            text_size=(350, None)
        ))
        
        # Date and author
        card.add_widget(Label(
            text=f"By: {announcement[4]} | {announcement[3][:16]}",
            size_hint_y=0.2,
            font_size='12sp'
        ))
        
        # Action buttons
        btn_layout = BoxLayout(size_hint_y=0.3, spacing=5)
        
        edit_btn = Button(text='Edit', background_color=(0.8, 0.6, 0.2, 1))
        edit_btn.bind(on_press=lambda x: self.edit_announcement(announcement))
        btn_layout.add_widget(edit_btn)
        
        delete_btn = Button(text='Delete', background_color=(0.8, 0.2, 0.2, 1))
        delete_btn.bind(on_press=lambda x: self.delete_announcement(announcement[0]))
        btn_layout.add_widget(delete_btn)
        
        card.add_widget(btn_layout)
        
        self.announcements_layout.add_widget(card)
    
    def show_add_popup(self, instance):
        """Show add announcement popup"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='Title:', size_hint_y=0.15))
        title_input = TextInput(multiline=False, size_hint_y=0.15)
        content.add_widget(title_input)
        
        content.add_widget(Label(text='Content:', size_hint_y=0.15))
        content_input = TextInput(size_hint_y=0.4)
        content.add_widget(content_input)
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        def add_announcement(x):
            if title_input.text.strip() and content_input.text.strip():
                current_user = get_current_user()
                if current_user:
                    db.add_announcement(
                        title_input.text.strip(),
                        content_input.text.strip(),
                        current_user['id']
                    )
                    popup.dismiss()
                    self.build_ui()
                else:
                    error_popup = Popup(
                        title='Error',
                        content=Label(text='Please login first'),
                        size_hint=(0.8, 0.3)
                    )
                    error_popup.open()
        
        add_btn = Button(text='Add', background_color=(0.3, 0.7, 0.3, 1))
        add_btn.bind(on_press=add_announcement)
        btn_layout.add_widget(add_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Add Announcement',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def edit_announcement(self, announcement):
        """Edit announcement"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='Title:', size_hint_y=0.15))
        title_input = TextInput(text=announcement[1], multiline=False, size_hint_y=0.15)
        content.add_widget(title_input)
        
        content.add_widget(Label(text='Content:', size_hint_y=0.15))
        content_input = TextInput(text=announcement[2], size_hint_y=0.4)
        content.add_widget(content_input)
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        def update_announcement(x):
            if title_input.text.strip() and content_input.text.strip():
                db.update_announcement(
                    announcement[0],
                    title_input.text.strip(),
                    content_input.text.strip()
                )
                popup.dismiss()
                self.build_ui()
        
        update_btn = Button(text='Update', background_color=(0.3, 0.7, 0.3, 1))
        update_btn.bind(on_press=update_announcement)
        btn_layout.add_widget(update_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Edit Announcement',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def delete_announcement(self, announcement_id):
        """Delete announcement"""
        db.delete_announcement(announcement_id)
        self.build_ui()
    
    def go_back(self, instance):
        """Go back to dashboard"""
        self.manager.current = 'lecturer_dashboard'



class ResourcesScreen(Screen):
    """Lecturer resources management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'resources'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='Resources', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'lecturer_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Add resource button
        add_btn = Button(
            text='+ Add Resource',
            size_hint=(1, 0.08),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        add_btn.bind(on_press=self.show_add_popup)
        layout.add_widget(add_btn)
        
        # Resources list
        scroll = ScrollView(size_hint=(1, 0.82))
        self.resources_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.resources_layout.bind(
            minimum_height=self.resources_layout.setter('height')
        )
        
        resources = db.get_all_resources()
        for res in resources:
            self.add_resource_card(res)
        
        scroll.add_widget(self.resources_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def add_resource_card(self, resource):
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=140,
            padding=10,
            spacing=5
        )
        
        card.add_widget(Label(
            text=f"[b]{resource[1]}[/b]",
            markup=True,
            size_hint_y=0.25,
            halign='left'
        ))
        
        card.add_widget(Label(
            text=resource[2] or 'No description',
            size_hint_y=0.3,
            halign='left',
            text_size=(350, None)
        ))
        
        card.add_widget(Label(
            text=f"Type: {resource[3]} | {resource[5][:16]}",
            size_hint_y=0.2,
            font_size='12sp'
        ))
        
        card.add_widget(Label(
            text=f"Link: {resource[4]}",
            size_hint_y=0.25,
            font_size='11sp'
        ))
        
        self.resources_layout.add_widget(card)
    
    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='Resource Name:', size_hint_y=0.12))
        name_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(name_input)
        
        content.add_widget(Label(text='Description:', size_hint_y=0.12))
        desc_input = TextInput(size_hint_y=0.2)
        content.add_widget(desc_input)
        
        content.add_widget(Label(text='Type:', size_hint_y=0.12))
        from kivy.uix.spinner import Spinner
        type_spinner = Spinner(
            text='PDF',
            values=('PDF', 'PPT', 'Notes', 'Video Link', 'Other'),
            size_hint_y=0.12
        )
        content.add_widget(type_spinner)
        
        content.add_widget(Label(text='File Link/URL:', size_hint_y=0.12))
        link_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(link_input)
        
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        
        def add_resource(x):
            if name_input.text.strip():
                current_user = get_current_user()
                if current_user:
                    db.add_resource(
                        name_input.text.strip(),
                        desc_input.text.strip(),
                        type_spinner.text,
                        link_input.text.strip(),
                        current_user['id']
                    )
                    popup.dismiss()
                    self.build_ui()
        
        add_btn = Button(text='Add', background_color=(0.3, 0.7, 0.3, 1))
        add_btn.bind(on_press=add_resource)
        btn_layout.add_widget(add_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Add Resource',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()


class AssignmentsScreen(Screen):
    """Lecturer assignments management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'assignments'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='Assignments', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'lecturer_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Add assignment button
        add_btn = Button(
            text='+ Create Assignment',
            size_hint=(1, 0.08),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        add_btn.bind(on_press=self.show_add_popup)
        layout.add_widget(add_btn)
        
        # Assignments list
        scroll = ScrollView(size_hint=(1, 0.82))
        self.assignments_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.assignments_layout.bind(
            minimum_height=self.assignments_layout.setter('height')
        )
        
        assignments = db.get_all_assignments()
        for assign in assignments:
            self.add_assignment_card(assign)
        
        scroll.add_widget(self.assignments_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def add_assignment_card(self, assignment):
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=150,
            padding=10,
            spacing=5
        )
        
        card.add_widget(Label(
            text=f"[b]{assignment[1]}[/b]",
            markup=True,
            size_hint_y=0.25,
            halign='left'
        ))
        
        card.add_widget(Label(
            text=assignment[2] or 'No description',
            size_hint_y=0.3,
            halign='left',
            text_size=(350, None)
        ))
        
        card.add_widget(Label(
            text=f"Due: {assignment[3]} | Total Marks: {assignment[4]}",
            size_hint_y=0.2,
            font_size='12sp'
        ))
        
        manage_btn = Button(
            text='Manage Submissions',
            size_hint_y=0.25,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        manage_btn.bind(on_press=lambda x: self.manage_submissions(assignment))
        card.add_widget(manage_btn)
        
        self.assignments_layout.add_widget(card)
    
    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='Title:', size_hint_y=0.12))
        title_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(title_input)
        
        content.add_widget(Label(text='Description:', size_hint_y=0.12))
        desc_input = TextInput(size_hint_y=0.2)
        content.add_widget(desc_input)
        
        content.add_widget(Label(text='Due Date (YYYY-MM-DD):', size_hint_y=0.12))
        date_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(date_input)
        
        content.add_widget(Label(text='Total Marks:', size_hint_y=0.12))
        marks_input = TextInput(multiline=False, input_filter='int', size_hint_y=0.12)
        content.add_widget(marks_input)
        
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        
        def add_assignment(x):
            if title_input.text.strip() and marks_input.text.strip():
                current_user = get_current_user()
                if current_user:
                    db.add_assignment(
                        title_input.text.strip(),
                        desc_input.text.strip(),
                        date_input.text.strip(),
                        int(marks_input.text.strip()),
                        current_user['id']
                    )
                    popup.dismiss()
                    self.build_ui()
        
        add_btn = Button(text='Create', background_color=(0.3, 0.7, 0.3, 1))
        add_btn.bind(on_press=add_assignment)
        btn_layout.add_widget(add_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Create Assignment',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def manage_submissions(self, assignment):
        """Manage assignment submissions"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(
            text=f"Assignment: {assignment[1]}",
            size_hint_y=0.1,
            font_size='18sp'
        ))
        
        scroll = ScrollView(size_hint=(1, 0.8))
        submissions_layout = BoxLayout(
            orientation='vertical',
            spacing=5,
            size_hint_y=None
        )
        submissions_layout.bind(
            minimum_height=submissions_layout.setter('height')
        )
        
        submissions = db.get_assignment_submissions(assignment[0])
        
        for sub in submissions:
            sub_card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=60,
                spacing=5
            )
            
            sub_card.add_widget(Label(
                text=f"{sub[1]}\n{sub[2]}",
                size_hint_x=0.4
            ))
            
            from kivy.uix.spinner import Spinner
            status_spinner = Spinner(
                text=sub[3],
                values=('Submitted', 'Not Submitted'),
                size_hint_x=0.3
            )
            sub_card.add_widget(status_spinner)
            
            marks_input = TextInput(
                text=str(sub[4]),
                multiline=False,
                input_filter='int',
                size_hint_x=0.2
            )
            sub_card.add_widget(marks_input)
            
            update_btn = Button(
                text='Update',
                size_hint_x=0.2,
                background_color=(0.3, 0.7, 0.3, 1)
            )
            update_btn.bind(on_press=lambda x, sid=sub[0], ss=status_spinner, mi=marks_input: 
                           self.update_submission(sid, ss.text, mi.text))
            sub_card.add_widget(update_btn)
            
            submissions_layout.add_widget(sub_card)
        
        scroll.add_widget(submissions_layout)
        content.add_widget(scroll)
        
        close_btn = Button(text='Close', size_hint_y=0.1)
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Manage Submissions',
            content=content,
            size_hint=(0.95, 0.9)
        )
        popup.open()
    
    def update_submission(self, submission_id, status, marks):
        """Update submission status and marks"""
        try:
            marks_val = int(marks) if marks else 0
            db.update_submission_status(submission_id, status, marks_val)
        except:
            pass



class TestsScreen(Screen):
    """Lecturer test marks management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'tests'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='Test Marks', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'lecturer_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Add test button
        add_btn = Button(
            text='+ Add Test',
            size_hint=(1, 0.08),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        add_btn.bind(on_press=self.show_add_popup)
        layout.add_widget(add_btn)
        
        # Tests list
        scroll = ScrollView(size_hint=(1, 0.82))
        self.tests_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.tests_layout.bind(
            minimum_height=self.tests_layout.setter('height')
        )
        
        tests = db.get_all_tests()
        for test in tests:
            self.add_test_card(test)
        
        scroll.add_widget(self.tests_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def add_test_card(self, test):
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=100,
            padding=10,
            spacing=5
        )
        
        card.add_widget(Label(
            text=f"[b]{test[1]}[/b]",
            markup=True,
            size_hint_y=0.4,
            halign='left'
        ))
        
        card.add_widget(Label(
            text=f"Total Marks: {test[2]} | Date: {test[3][:16]}",
            size_hint_y=0.3,
            font_size='12sp'
        ))
        
        manage_btn = Button(
            text='Enter/Edit Marks',
            size_hint_y=0.3,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        manage_btn.bind(on_press=lambda x: self.manage_marks(test))
        card.add_widget(manage_btn)
        
        self.tests_layout.add_widget(card)
    
    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='Test Name:', size_hint_y=0.2))
        name_input = TextInput(multiline=False, size_hint_y=0.2)
        content.add_widget(name_input)
        
        content.add_widget(Label(text='Total Marks:', size_hint_y=0.2))
        marks_input = TextInput(multiline=False, input_filter='int', size_hint_y=0.2)
        content.add_widget(marks_input)
        
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        def add_test(x):
            if name_input.text.strip() and marks_input.text.strip():
                current_user = get_current_user()
                if current_user:
                    db.add_test(
                        name_input.text.strip(),
                        int(marks_input.text.strip()),
                        current_user['id']
                    )
                    popup.dismiss()
                    self.build_ui()
        
        add_btn = Button(text='Add', background_color=(0.3, 0.7, 0.3, 1))
        add_btn.bind(on_press=add_test)
        btn_layout.add_widget(add_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Add Test',
            content=content,
            size_hint=(0.9, 0.6)
        )
        popup.open()
    
    def manage_marks(self, test):
        """Manage test marks"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(
            text=f"Test: {test[1]} (Total: {test[2]})",
            size_hint_y=0.1,
            font_size='18sp'
        ))
        
        scroll = ScrollView(size_hint=(1, 0.8))
        marks_layout = BoxLayout(
            orientation='vertical',
            spacing=5,
            size_hint_y=None
        )
        marks_layout.bind(
            minimum_height=marks_layout.setter('height')
        )
        
        marks_data = db.get_test_marks(test[0])
        
        for mark in marks_data:
            mark_card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=50,
                spacing=5
            )
            
            mark_card.add_widget(Label(
                text=f"{mark[1]} ({mark[2]})",
                size_hint_x=0.5
            ))
            
            marks_input = TextInput(
                text=str(mark[3]),
                multiline=False,
                input_filter='int',
                size_hint_x=0.3
            )
            mark_card.add_widget(marks_input)
            
            update_btn = Button(
                text='Update',
                size_hint_x=0.2,
                background_color=(0.3, 0.7, 0.3, 1)
            )
            update_btn.bind(on_press=lambda x, mid=mark[0], mi=marks_input: 
                           self.update_marks(mid, mi.text))
            mark_card.add_widget(update_btn)
            
            marks_layout.add_widget(mark_card)
        
        scroll.add_widget(marks_layout)
        content.add_widget(scroll)
        
        close_btn = Button(text='Close', size_hint_y=0.1)
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Manage Test Marks',
            content=content,
            size_hint=(0.95, 0.9)
        )
        popup.open()
    
    def update_marks(self, mark_id, marks):
        """Update test marks"""
        try:
            marks_val = int(marks) if marks else 0
            db.update_test_marks(mark_id, marks_val)
        except:
            pass


class StudentsScreen(Screen):
    """Student management screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'students'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='Student Management', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'lecturer_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Add student button
        add_btn = Button(
            text='+ Add Student',
            size_hint=(1, 0.08),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        add_btn.bind(on_press=self.show_add_popup)
        layout.add_widget(add_btn)
        
        # Students list
        scroll = ScrollView(size_hint=(1, 0.82))
        self.students_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.students_layout.bind(
            minimum_height=self.students_layout.setter('height')
        )
        
        students = db.get_all_students()
        for student in students:
            self.add_student_card(student)
        
        scroll.add_widget(self.students_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def add_student_card(self, student):
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=120,
            padding=10,
            spacing=5
        )
        
        card.add_widget(Label(
            text=f"[b]{student[1]}[/b]",
            markup=True,
            size_hint_y=0.3,
            halign='left'
        ))
        
        card.add_widget(Label(
            text=f"Roll: {student[2]} | Email: {student[3]}",
            size_hint_y=0.25,
            font_size='12sp'
        ))
        
        card.add_widget(Label(
            text=f"Phone: {student[4]}",
            size_hint_y=0.2,
            font_size='12sp'
        ))
        
        btn_layout = BoxLayout(size_hint_y=0.25, spacing=5)
        
        edit_btn = Button(text='Edit', background_color=(0.8, 0.6, 0.2, 1))
        edit_btn.bind(on_press=lambda x: self.edit_student(student))
        btn_layout.add_widget(edit_btn)
        
        delete_btn = Button(text='Delete', background_color=(0.8, 0.2, 0.2, 1))
        delete_btn.bind(on_press=lambda x: self.delete_student(student[0]))
        btn_layout.add_widget(delete_btn)
        
        card.add_widget(btn_layout)
        
        self.students_layout.add_widget(card)
    
    def show_add_popup(self, instance):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='Name:', size_hint_y=0.12))
        name_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(name_input)
        
        content.add_widget(Label(text='Roll Number:', size_hint_y=0.12))
        roll_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(roll_input)
        
        content.add_widget(Label(text='Email:', size_hint_y=0.12))
        email_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(email_input)
        
        content.add_widget(Label(text='Phone:', size_hint_y=0.12))
        phone_input = TextInput(multiline=False, size_hint_y=0.12)
        content.add_widget(phone_input)
        
        content.add_widget(Label(
            text='Default password: student123',
            size_hint_y=0.1,
            font_size='12sp'
        ))
        
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        
        def add_student(x):
            if all([name_input.text.strip(), roll_input.text.strip(), 
                   email_input.text.strip(), phone_input.text.strip()]):
                success, msg = db.add_student(
                    name_input.text.strip(),
                    email_input.text.strip(),
                    phone_input.text.strip(),
                    roll_input.text.strip()
                )
                popup.dismiss()
                self.build_ui()
        
        add_btn = Button(text='Add', background_color=(0.3, 0.7, 0.3, 1))
        add_btn.bind(on_press=add_student)
        btn_layout.add_widget(add_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Add Student',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def edit_student(self, student):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(text='Name:', size_hint_y=0.12))
        name_input = TextInput(text=student[1], multiline=False, size_hint_y=0.12)
        content.add_widget(name_input)
        
        content.add_widget(Label(text='Roll Number:', size_hint_y=0.12))
        roll_input = TextInput(text=student[2], multiline=False, size_hint_y=0.12)
        content.add_widget(roll_input)
        
        content.add_widget(Label(text='Email:', size_hint_y=0.12))
        email_input = TextInput(text=student[3], multiline=False, size_hint_y=0.12)
        content.add_widget(email_input)
        
        content.add_widget(Label(text='Phone:', size_hint_y=0.12))
        phone_input = TextInput(text=student[4], multiline=False, size_hint_y=0.12)
        content.add_widget(phone_input)
        
        btn_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        
        def update_student(x):
            if all([name_input.text.strip(), roll_input.text.strip(), 
                   email_input.text.strip(), phone_input.text.strip()]):
                db.update_student(
                    student[0],
                    name_input.text.strip(),
                    email_input.text.strip(),
                    phone_input.text.strip(),
                    roll_input.text.strip()
                )
                popup.dismiss()
                self.build_ui()
        
        update_btn = Button(text='Update', background_color=(0.3, 0.7, 0.3, 1))
        update_btn.bind(on_press=update_student)
        btn_layout.add_widget(update_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Edit Student',
            content=content,
            size_hint=(0.9, 0.8)
        )
        popup.open()
    
    def delete_student(self, student_id):
        db.delete_student(student_id)
        self.build_ui()


class QAScreen(Screen):
    """Q&A management screen for lecturer"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'qa'
    
    def on_enter(self):
        self.build_ui()
    
    def mark_and_refresh(self, question_id, lecturer_id):
        """Mark question as viewed and refresh the screen"""
        db.mark_question_as_viewed(question_id, lecturer_id)
        self.build_ui()  # Refresh to remove star
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header with notification count
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        current_user = get_current_user()
        if current_user:
            unviewed_count = db.get_unviewed_questions_count(current_user['id'])
            title_text = f'Q & A ({unviewed_count} new)' if unviewed_count > 0 else 'Q & A Dashboard'
        else:
            title_text = 'Q & A Dashboard'
            
        header.add_widget(Label(text=title_text, font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'lecturer_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Questions list
        scroll = ScrollView(size_hint=(1, 0.9))
        self.questions_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.questions_layout.bind(
            minimum_height=self.questions_layout.setter('height')
        )
        
        questions = db.get_all_questions()
        for q in questions:
            self.add_question_card(q)
        
        scroll.add_widget(self.questions_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def add_question_card(self, question):
        # Check if new question
        current_user = get_current_user()
        is_new = False
        if current_user:
            is_new = not db.is_question_viewed(question[0], current_user['id'])
        
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=180,
            padding=10,
            spacing=5
        )
        
        # Add star if new
        from_text = f"[b]⭐ From: {question[1]} ({question[2]})[/b]" if is_new else f"[b]From: {question[1]} ({question[2]})[/b]"
        
        card.add_widget(Label(
            text=from_text,
            markup=True,
            size_hint_y=0.15,
            halign='left'
        ))
        
        card.add_widget(Label(
            text=f"Q: {question[3]}",
            size_hint_y=0.25,
            halign='left',
            text_size=(350, None)
        ))
        
        if question[4]:
            card.add_widget(Label(
                text=f"A: {question[4]}",
                size_hint_y=0.25,
                halign='left',
                text_size=(350, None),
                color=(0.3, 0.7, 0.3, 1)
            ))
        else:
            card.add_widget(Label(
                text="Not answered yet",
                size_hint_y=0.25,
                color=(0.8, 0.2, 0.2, 1)
            ))
        
        card.add_widget(Label(
            text=f"Asked: {question[5][:16]}",
            size_hint_y=0.15,
            font_size='11sp'
        ))
        
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=5)
        
        # Add "Mark as Read" button if new
        if is_new and current_user:
            mark_btn = Button(text='Mark Read', background_color=(0.5, 0.5, 0.5, 1))
            mark_btn.bind(on_press=lambda x, qid=question[0], uid=current_user['id']: self.mark_and_refresh(qid, uid))
            btn_layout.add_widget(mark_btn)
        
        reply_btn = Button(text='Reply', background_color=(0.2, 0.6, 0.8, 1))
        reply_btn.bind(on_press=lambda x: self.reply_question(question))
        btn_layout.add_widget(reply_btn)
        
        delete_btn = Button(text='Delete', background_color=(0.8, 0.2, 0.2, 1))
        delete_btn.bind(on_press=lambda x: self.delete_question(question[0]))
        btn_layout.add_widget(delete_btn)
        
        card.add_widget(btn_layout)
        
        self.questions_layout.add_widget(card)
    
    def reply_question(self, question):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        content.add_widget(Label(
            text=f"Question: {question[3]}",
            size_hint_y=0.3,
            text_size=(350, None)
        ))
        
        content.add_widget(Label(text='Your Answer:', size_hint_y=0.15))
        answer_input = TextInput(
            text=question[4] if question[4] else '',
            size_hint_y=0.4
        )
        content.add_widget(answer_input)
        
        btn_layout = BoxLayout(size_hint_y=0.15, spacing=10)
        
        def submit_answer(x):
            if answer_input.text.strip():
                db.answer_question(question[0], answer_input.text.strip())
                popup.dismiss()
                self.build_ui()
        
        submit_btn = Button(text='Submit', background_color=(0.3, 0.7, 0.3, 1))
        submit_btn.bind(on_press=submit_answer)
        btn_layout.add_widget(submit_btn)
        
        cancel_btn = Button(text='Cancel')
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        btn_layout.add_widget(cancel_btn)
        
        content.add_widget(btn_layout)
        
        popup = Popup(
            title='Reply to Question',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def delete_question(self, question_id):
        db.delete_question(question_id)
        self.build_ui()



# STUDENT SCREENS

class ViewAnnouncementsScreen(Screen):
    """Student view announcements screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'view_announcements'
    
    def on_enter(self):
        self.build_ui()
    
    def mark_and_refresh(self, announcement_id, student_id):
        """Mark announcement as viewed and refresh the screen"""
        db.mark_announcement_as_viewed(announcement_id, student_id)
        self.build_ui()  # Refresh to remove star
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header with notification count
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        
        current_user = get_current_user()
        if current_user:
            unviewed_count = db.get_unviewed_announcements_count(current_user['id'])
            title_text = f'Announcements ({unviewed_count} new)' if unviewed_count > 0 else 'Announcements'
        else:
            title_text = 'Announcements'
            
        header.add_widget(Label(text=title_text, font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'student_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Announcements list
        scroll = ScrollView(size_hint=(1, 0.9))
        announcements_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        announcements_layout.bind(
            minimum_height=announcements_layout.setter('height')
        )
        
        announcements = db.get_all_announcements()
        for ann in announcements:
            # Check if viewed
            is_new = False
            if current_user:
                is_new = not db.is_announcement_viewed(ann[0], current_user['id'])
            
            # Make card clickable
            card = Button(
                size_hint_y=None,
                height=130,
                background_color=(0.2, 0.2, 0.2, 1) if not is_new else (0.3, 0.3, 0.1, 1),
                background_normal=''
            )
            
            # Create content layout
            content = BoxLayout(orientation='vertical', padding=10, spacing=5)
            
            # Add star if new
            title_text = f"[b]⭐ {ann[1]}[/b]" if is_new else f"[b]{ann[1]}[/b]"
            
            content.add_widget(Label(
                text=title_text,
                markup=True,
                size_hint_y=0.3,
                halign='left',
                valign='middle'
            ))
            
            content.add_widget(Label(
                text=ann[2],
                size_hint_y=0.5,
                halign='left',
                valign='middle',
                text_size=(350, None)
            ))
            
            content.add_widget(Label(
                text=f"By: {ann[4]} | {ann[3][:16]}",
                size_hint_y=0.2,
                font_size='12sp'
            ))
            
            card.add_widget(content)
            
            # Mark as viewed when clicked
            if current_user and is_new:
                card.bind(on_press=lambda x, aid=ann[0], uid=current_user['id']: self.mark_and_refresh(aid, uid))
            
            announcements_layout.add_widget(card)
        
        scroll.add_widget(announcements_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)


class ViewResourcesScreen(Screen):
    """Student view resources screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'view_resources'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='Resources', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'student_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Search bar
        search_layout = BoxLayout(size_hint=(1, 0.08), spacing=5)
        self.search_input = TextInput(
            hint_text='Search resources...',
            multiline=False,
            size_hint=(0.7, 1)
        )
        search_layout.add_widget(self.search_input)
        
        search_btn = Button(
            text='Search',
            size_hint=(0.3, 1),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        search_btn.bind(on_press=self.search_resources)
        search_layout.add_widget(search_btn)
        
        layout.add_widget(search_layout)
        
        # Resources list
        scroll = ScrollView(size_hint=(1, 0.82))
        self.resources_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.resources_layout.bind(
            minimum_height=self.resources_layout.setter('height')
        )
        
        self.load_resources()
        
        scroll.add_widget(self.resources_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_resources(self, search_term=None):
        self.resources_layout.clear_widgets()
        
        if search_term:
            resources = db.search_resources(search_term)
        else:
            resources = db.get_all_resources()
        
        for res in resources:
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=130,
                padding=10,
                spacing=5
            )
            
            card.add_widget(Label(
                text=f"[b]{res[1]}[/b]",
                markup=True,
                size_hint_y=0.25,
                halign='left'
            ))
            
            card.add_widget(Label(
                text=res[2] or 'No description',
                size_hint_y=0.3,
                halign='left',
                text_size=(350, None)
            ))
            
            card.add_widget(Label(
                text=f"Type: {res[3]} | {res[5][:16]}",
                size_hint_y=0.2,
                font_size='12sp'
            ))
            
            card.add_widget(Label(
                text=f"Link: {res[4]}",
                size_hint_y=0.25,
                font_size='11sp'
            ))
            
            self.resources_layout.add_widget(card)
    
    def search_resources(self, instance):
        search_term = self.search_input.text.strip()
        self.load_resources(search_term if search_term else None)


class ViewAssignmentsScreen(Screen):
    """Student view assignments screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'view_assignments'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='My Assignments', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'student_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Assignments list
        scroll = ScrollView(size_hint=(1, 0.9))
        assignments_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        assignments_layout.bind(
            minimum_height=assignments_layout.setter('height')
        )
        
        current_user = get_current_user()
        if not current_user:
            layout.add_widget(Label(text='Please login first'))
            self.add_widget(layout)
            return
            
        assignments = db.get_student_assignments(current_user['id'])
        
        for assign in assignments:
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=150,
                padding=10,
                spacing=5
            )
            
            card.add_widget(Label(
                text=f"[b]{assign[1]}[/b]",
                markup=True,
                size_hint_y=0.25,
                halign='left'
            ))
            
            card.add_widget(Label(
                text=assign[2] or 'No description',
                size_hint_y=0.3,
                halign='left',
                text_size=(350, None)
            ))
            
            card.add_widget(Label(
                text=f"Due: {assign[3]} | Total Marks: {assign[4]}",
                size_hint_y=0.2,
                font_size='12sp'
            ))
            
            status_color = (0.3, 0.7, 0.3, 1) if assign[5] == 'Submitted' else (0.8, 0.2, 0.2, 1)
            card.add_widget(Label(
                text=f"Status: {assign[5]} | Marks: {assign[6]}/{assign[4]}",
                size_hint_y=0.25,
                font_size='13sp',
                color=status_color
            ))
            
            assignments_layout.add_widget(card)
        
        scroll.add_widget(assignments_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)


class ViewMarksScreen(Screen):
    """Student view test marks screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'view_marks'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='My Test Marks', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'student_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Marks list
        scroll = ScrollView(size_hint=(1, 0.9))
        marks_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        marks_layout.bind(
            minimum_height=marks_layout.setter('height')
        )
        
        current_user = get_current_user()
        if not current_user:
            layout.add_widget(Label(text='Please login first'))
            self.add_widget(layout)
            return
            
        marks = db.get_student_test_marks(current_user['id'])
        
        for mark in marks:
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=100,
                padding=10,
                spacing=5
            )
            
            card.add_widget(Label(
                text=f"[b]{mark[0]}[/b]",
                markup=True,
                size_hint_y=0.4,
                halign='left'
            ))
            
            percentage = (mark[1] / mark[2] * 100) if mark[2] > 0 else 0
            card.add_widget(Label(
                text=f"Marks: {mark[1]}/{mark[2]} ({percentage:.1f}%)",
                size_hint_y=0.3,
                font_size='14sp'
            ))
            
            card.add_widget(Label(
                text=f"Date: {mark[3][:16]}",
                size_hint_y=0.3,
                font_size='12sp'
            ))
            
            marks_layout.add_widget(card)
        
        scroll.add_widget(marks_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)


class AskQuestionScreen(Screen):
    """Student ask question screen"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'ask_question'
    
    def on_enter(self):
        self.build_ui()
    
    def build_ui(self):
        self.clear_widgets()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1), spacing=10)
        header.add_widget(Label(text='Q & A', font_size='20sp'))
        back_btn = Button(text='Back', size_hint=(0.3, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'student_dashboard'))
        header.add_widget(back_btn)
        layout.add_widget(header)
        
        # Ask question section
        layout.add_widget(Label(text='Ask a Question:', size_hint=(1, 0.08)))
        self.question_input = TextInput(size_hint=(1, 0.15))
        layout.add_widget(self.question_input)
        
        submit_btn = Button(
            text='Submit Question',
            size_hint=(1, 0.08),
            background_color=(0.3, 0.7, 0.3, 1)
        )
        submit_btn.bind(on_press=self.submit_question)
        layout.add_widget(submit_btn)
        
        layout.add_widget(Label(text='My Questions:', size_hint=(1, 0.08)))
        
        # Questions list
        scroll = ScrollView(size_hint=(1, 0.61))
        self.questions_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.questions_layout.bind(
            minimum_height=self.questions_layout.setter('height')
        )
        
        self.load_questions()
        
        scroll.add_widget(self.questions_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def load_questions(self):
        self.questions_layout.clear_widgets()
        
        current_user = get_current_user()
        if not current_user:
            return
            
        questions = db.get_student_questions(current_user['id'])
        
        for q in questions:
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=140,
                padding=10,
                spacing=5
            )
            
            card.add_widget(Label(
                text=f"[b]Q: {q[1]}[/b]",
                markup=True,
                size_hint_y=0.35,
                halign='left',
                text_size=(350, None)
            ))
            
            if q[2]:
                card.add_widget(Label(
                    text=f"A: {q[2]}",
                    size_hint_y=0.35,
                    halign='left',
                    text_size=(350, None),
                    color=(0.3, 0.7, 0.3, 1)
                ))
            else:
                card.add_widget(Label(
                    text="Waiting for answer...",
                    size_hint_y=0.35,
                    color=(0.8, 0.6, 0.2, 1)
                ))
            
            card.add_widget(Label(
                text=f"Asked: {q[3][:16]}",
                size_hint_y=0.3,
                font_size='11sp'
            ))
            
            self.questions_layout.add_widget(card)
    
    def submit_question(self, instance):
        question = self.question_input.text.strip()
        
        if question:
            current_user = get_current_user()
            if current_user:
                db.add_question(current_user['id'], question)
                self.question_input.text = ''
                self.load_questions()
            
            popup = Popup(
                title='Success',
                content=Label(text='Question submitted successfully!'),
                size_hint=(0.8, 0.3)
            )
            popup.open()
