import sys
import os
# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QStackedWidget,
                            QFrame, QSplitter, QMessageBox, QDesktopWidget,
                            QTableWidget, QTableWidgetItem, QLineEdit, QFormLayout,
                            QSpinBox, QHeaderView, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap

# Import your existing domain, repository and services
from src.domain.Domain import Student, Discipline, Grade
from src.repository.TextFileRepos import Students_TextFile_Repository, Disciplines_TextFile_Repository, Grades_TextFile_Repository
from src.repository.MemoryRepos import Id_Error
from src.services.Services import Services
from src.services.undo_service import UndoService, Operation, FunctionCall, UndoRedoError

# Temporary placeholders for the missing GUI classes
class StudentManagementGUI(QWidget):
    def __init__(self, service, undo_service):
        super().__init__()
        self.service = service
        self.undo_service = undo_service
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Student Management")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Search and action buttons
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search students by name...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_students)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Add New Student")
        add_button.clicked.connect(self.add_student)
        buttons_layout.addWidget(add_button)
        
        refresh_button = QPushButton("Refresh List")
        refresh_button.clicked.connect(self.refresh_students)
        buttons_layout.addWidget(refresh_button)
        
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_action)
        buttons_layout.addWidget(undo_button)
        
        redo_button = QPushButton("Redo")
        redo_button.clicked.connect(self.redo_action)
        buttons_layout.addWidget(redo_button)
        
        layout.addLayout(buttons_layout)
        
        # Student table
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(3)
        self.student_table.setHorizontalHeaderLabels(["ID", "Name", "Actions"])
        self.student_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.student_table)
        
        # Load students
        self.refresh_students()
    
    def refresh_students(self):
        """Refresh the student list from the repository"""
        self.student_table.setRowCount(0)
        students = self.service._Services__student_repo.get_list_of_students
        
        for row, student in enumerate(students):
            self.student_table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(student.get_student_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.student_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(student.get_student_name)
            self.student_table.setItem(row, 1, name_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, s=student: self.edit_student(s))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, s=student: self.delete_student(s))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.student_table.setCellWidget(row, 2, actions_widget)
    
    def search_students(self):
        """Search students by name"""
        search_text = self.search_input.text()
        if not search_text:
            self.refresh_students()
            return
        
        found_students = self.service.search_student_by_name(search_text)
        
        self.student_table.setRowCount(0)
        for row, student in enumerate(found_students):
            self.student_table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(student.get_student_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.student_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(student.get_student_name)
            self.student_table.setItem(row, 1, name_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, s=student: self.edit_student(s))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, s=student: self.delete_student(s))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.student_table.setCellWidget(row, 2, actions_widget)
    
    def add_student(self):
        """Add a new student"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Student")
        
        layout = QFormLayout(dialog)
        
        # Student ID
        id_input = QSpinBox()
        id_input.setRange(1, 9999)
        layout.addRow("Student ID:", id_input)
        
        # Student Name
        name_input = QLineEdit()
        layout.addRow("Student Name:", name_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            student_id = id_input.value()
            student_name = name_input.text()
            
            if not student_name:
                QMessageBox.warning(self, "Input Error", "Student name cannot be empty!")
                return
            
            try:
                # Add student using repository
                student_repo = self.service._Services__student_repo
                
                # Create undo/redo operations
                undo_call = FunctionCall(student_repo.remove_student, student_id)
                redo_call = FunctionCall(student_repo.add_student, student_id, student_name)
                
                # Add student
                student_repo.add_student(student_id, student_name)
                
                # Record operation for undo/redo
                self.undo_service.record(Operation(undo_call, redo_call))
                
                self.refresh_students()
                QMessageBox.information(self, "Success", f"Student '{student_name}' added successfully!")
            except Id_Error as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def edit_student(self, student):
        """Edit an existing student"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Student")
        
        layout = QFormLayout(dialog)
        
        # Student ID (read-only)
        id_label = QLabel(str(student.get_student_id))
        layout.addRow("Student ID:", id_label)
        
        # Student Name
        name_input = QLineEdit(student.get_student_name)
        layout.addRow("Student Name:", name_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            new_name = name_input.text()
            
            if not new_name:
                QMessageBox.warning(self, "Input Error", "Student name cannot be empty!")
                return
            
            try:
                # Update student using repository
                student_repo = self.service._Services__student_repo
                old_name = student.get_student_name
                
                # Create undo/redo operations
                undo_call = FunctionCall(student_repo.update_student, student.get_student_id, old_name)
                redo_call = FunctionCall(student_repo.update_student, student.get_student_id, new_name)
                
                # Update student
                student_repo.update_student(student.get_student_id, new_name)
                
                # Record operation for undo/redo
                self.undo_service.record(Operation(undo_call, redo_call))
                
                self.refresh_students()
                QMessageBox.information(self, "Success", f"Student updated successfully!")
            except Id_Error as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def delete_student(self, student):
        """Delete a student"""
        confirm = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete student '{student.get_student_name}'?\n"
            "This will also delete all grades for this student.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                # Get repositories
                student_repo = self.service._Services__student_repo
                grade_repo = self.service._Services__grade_repo
                
                # Save student data for undo
                student_id = student.get_student_id
                student_name = student.get_student_name
                
                # Save grades for undo
                grades = []
                for grade in grade_repo.get_list_of_grades:
                    if grade.get_student_id == student_id:
                        grades.append(grade)
                
                # Create undo/redo operations
                undo_call = FunctionCall(student_repo.add_student, student_id, student_name)
                redo_call = FunctionCall(self.service.remove_student_service, student_id)
                
                # Delete student and grades
                self.service.remove_student_service(student_id)
                
                # Record operation for undo/redo
                self.undo_service.record(Operation(undo_call, redo_call))
                
                self.refresh_students()
                QMessageBox.information(self, "Success", "Student deleted successfully!")
            except Id_Error as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def undo_action(self):
        """Undo the last action"""
        try:
            self.undo_service.undo()
            self.refresh_students()
        except UndoRedoError as e:
            QMessageBox.information(self, "Undo", str(e))
    
    def redo_action(self):
        """Redo the last undone action"""
        try:
            self.undo_service.redo()
            self.refresh_students()
        except UndoRedoError as e:
            QMessageBox.information(self, "Redo", str(e))

class CourseManagementGUI(QWidget):
    def __init__(self, service, undo_service):
        super().__init__()
        self.service = service
        self.undo_service = undo_service
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Course Management")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Search and action buttons
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search courses by name...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_courses)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Add New Course")
        add_button.clicked.connect(self.add_course)
        buttons_layout.addWidget(add_button)
        
        refresh_button = QPushButton("Refresh List")
        refresh_button.clicked.connect(self.refresh_courses)
        buttons_layout.addWidget(refresh_button)
        
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_action)
        buttons_layout.addWidget(undo_button)
        
        redo_button = QPushButton("Redo")
        redo_button.clicked.connect(self.redo_action)
        buttons_layout.addWidget(redo_button)
        
        layout.addLayout(buttons_layout)
        
        # Course table
        self.course_table = QTableWidget()
        self.course_table.setColumnCount(3)
        self.course_table.setHorizontalHeaderLabels(["ID", "Name", "Actions"])
        self.course_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.course_table)
        
        # Load courses
        self.refresh_courses()
    
    def refresh_courses(self):
        """Refresh the course list from the repository"""
        self.course_table.setRowCount(0)
        courses = self.service._Services__discipline_repo.get_list_of_disciplines
        
        for row, course in enumerate(courses):
            self.course_table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(course.get_discipline_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.course_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(course.get_discipline_name)
            self.course_table.setItem(row, 1, name_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, c=course: self.edit_course(c))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, c=course: self.delete_course(c))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.course_table.setCellWidget(row, 2, actions_widget)
    
    def search_courses(self):
        """Search courses by name"""
        search_text = self.search_input.text()
        if not search_text:
            self.refresh_courses()
            return
        
        found_courses = self.service.search_discipline_by_name(search_text)
        
        self.course_table.setRowCount(0)
        for row, course in enumerate(found_courses):
            self.course_table.insertRow(row)
            
            # ID
            id_item = QTableWidgetItem(str(course.get_discipline_id))
            id_item.setFlags(id_item.flags() & ~Qt.ItemIsEditable)
            self.course_table.setItem(row, 0, id_item)
            
            # Name
            name_item = QTableWidgetItem(course.get_discipline_name)
            self.course_table.setItem(row, 1, name_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, c=course: self.edit_course(c))
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, c=course: self.delete_course(c))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            
            self.course_table.setCellWidget(row, 2, actions_widget)
    
    def add_course(self):
        """Add a new course"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Course")
        
        layout = QFormLayout(dialog)
        
        # Course ID
        id_input = QSpinBox()
        id_input.setRange(1, 9999)
        layout.addRow("Course ID:", id_input)
        
        # Course Name
        name_input = QLineEdit()
        layout.addRow("Course Name:", name_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            course_id = id_input.value()
            course_name = name_input.text()
            
            if not course_name:
                QMessageBox.warning(self, "Input Error", "Course name cannot be empty!")
                return
            
            try:
                # Add course using repository
                discipline_repo = self.service._Services__discipline_repo
                
                # Create undo/redo operations
                undo_call = FunctionCall(discipline_repo.remove_discipline, course_id)
                redo_call = FunctionCall(discipline_repo.add_discipline, course_id, course_name)
                
                # Add course
                discipline_repo.add_discipline(course_id, course_name)
                
                # Record operation for undo/redo
                self.undo_service.record(Operation(undo_call, redo_call))
                
                self.refresh_courses()
                QMessageBox.information(self, "Success", f"Course '{course_name}' added successfully!")
            except Id_Error as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def edit_course(self, course):
        """Edit an existing course"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Course")
        
        layout = QFormLayout(dialog)
        
        # Course ID (read-only)
        id_label = QLabel(str(course.get_discipline_id))
        layout.addRow("Course ID:", id_label)
        
        # Course Name
        name_input = QLineEdit(course.get_discipline_name)
        layout.addRow("Course Name:", name_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            new_name = name_input.text()
            
            if not new_name:
                QMessageBox.warning(self, "Input Error", "Course name cannot be empty!")
                return
            
            try:
                # Update course using repository
                discipline_repo = self.service._Services__discipline_repo
                old_name = course.get_discipline_name
                
                # Create undo/redo operations
                undo_call = FunctionCall(discipline_repo.update_discipline, course.get_discipline_id, old_name)
                redo_call = FunctionCall(discipline_repo.update_discipline, course.get_discipline_id, new_name)
                
                # Update course
                discipline_repo.update_discipline(course.get_discipline_id, new_name)
                
                # Record operation for undo/redo
                self.undo_service.record(Operation(undo_call, redo_call))
                
                self.refresh_courses()
                QMessageBox.information(self, "Success", f"Course updated successfully!")
            except Id_Error as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def delete_course(self, course):
        """Delete a course"""
        confirm = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete course '{course.get_discipline_name}'?\n"
            "This will also delete all grades for this course.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                # Get repositories
                discipline_repo = self.service._Services__discipline_repo
                grade_repo = self.service._Services__grade_repo
                
                # Save course data for undo
                course_id = course.get_discipline_id
                course_name = course.get_discipline_name
                
                # Save grades for undo
                grades = []
                for grade in grade_repo.get_list_of_grades:
                    if grade.get_discipline_id == course_id:
                        grades.append(grade)
                
                # Create undo/redo operations
                undo_call = FunctionCall(discipline_repo.add_discipline, course_id, course_name)
                redo_call = FunctionCall(self.service.remove_discipline_service, course_id)
                
                # Delete course and grades
                self.service.remove_discipline_service(course_id)
                
                # Record operation for undo/redo
                self.undo_service.record(Operation(undo_call, redo_call))
                
                self.refresh_courses()
                QMessageBox.information(self, "Success", "Course deleted successfully!")
            except Id_Error as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def undo_action(self):
        """Undo the last action"""
        try:
            self.undo_service.undo()
            self.refresh_courses()
        except UndoRedoError as e:
            QMessageBox.information(self, "Undo", str(e))
    
    def redo_action(self):
        """Redo the last undone action"""
        try:
            self.undo_service.redo()
            self.refresh_courses()
        except UndoRedoError as e:
            QMessageBox.information(self, "Redo", str(e))

class EnrollmentManagementGUI(QWidget):
    def __init__(self, service, undo_service):
        super().__init__()
        self.service = service
        self.undo_service = undo_service
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Grade Management")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Add New Grade")
        add_button.clicked.connect(self.add_grade)
        buttons_layout.addWidget(add_button)
        
        refresh_button = QPushButton("Refresh List")
        refresh_button.clicked.connect(self.refresh_grades)
        buttons_layout.addWidget(refresh_button)
        
        undo_button = QPushButton("Undo")
        undo_button.clicked.connect(self.undo_action)
        buttons_layout.addWidget(undo_button)
        
        redo_button = QPushButton("Redo")
        redo_button.clicked.connect(self.redo_action)
        buttons_layout.addWidget(redo_button)
        
        layout.addLayout(buttons_layout)
        
        # Grade table
        self.grade_table = QTableWidget()
        self.grade_table.setColumnCount(4)
        self.grade_table.setHorizontalHeaderLabels(["Student", "Course", "Grade", "Actions"])
        self.grade_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.grade_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.grade_table)
        
        # Load grades
        self.refresh_grades()
    
    def refresh_grades(self):
        """Refresh the grade list from the repository"""
        self.grade_table.setRowCount(0)
        grades = self.service._Services__grade_repo.get_list_of_grades
        student_repo = self.service._Services__student_repo
        discipline_repo = self.service._Services__discipline_repo
        
        for row, grade in enumerate(grades):
            self.grade_table.insertRow(row)
            
            # Student
            try:
                student = student_repo.find_by_id(grade.get_student_id)
                student_name = student.get_student_name
            except Id_Error:
                student_name = f"Unknown (ID: {grade.get_student_id})"
            
            student_item = QTableWidgetItem(student_name)
            student_item.setFlags(student_item.flags() & ~Qt.ItemIsEditable)
            self.grade_table.setItem(row, 0, student_item)
            
            # Course
            try:
                discipline = discipline_repo.find_by_id(grade.get_discipline_id)
                discipline_name = discipline.get_discipline_name
            except Id_Error:
                discipline_name = f"Unknown (ID: {grade.get_discipline_id})"
            
            discipline_item = QTableWidgetItem(discipline_name)
            discipline_item.setFlags(discipline_item.flags() & ~Qt.ItemIsEditable)
            self.grade_table.setItem(row, 1, discipline_item)
            
            # Grade
            grade_item = QTableWidgetItem(str(grade.get_grade_value))
            grade_item.setFlags(grade_item.flags() & ~Qt.ItemIsEditable)
            self.grade_table.setItem(row, 2, grade_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, g=grade, r=row: self.delete_grade(g, r))
            
            actions_layout.addWidget(delete_btn)
            
            self.grade_table.setCellWidget(row, 3, actions_widget)
    
    def add_grade(self):
        """Add a new grade"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Grade")
        
        layout = QFormLayout(dialog)
        
        # Student ID
        student_id_input = QSpinBox()
        student_id_input.setRange(1, 9999)
        layout.addRow("Student ID:", student_id_input)
        
        # Discipline ID
        discipline_id_input = QSpinBox()
        discipline_id_input.setRange(1, 9999)
        layout.addRow("Course ID:", discipline_id_input)
        
        # Grade Value
        grade_value_input = QSpinBox()
        grade_value_input.setRange(1, 10)
        layout.addRow("Grade Value:", grade_value_input)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        if dialog.exec_() == QDialog.Accepted:
            student_id = student_id_input.value()
            discipline_id = discipline_id_input.value()
            grade_value = grade_value_input.value()
            
            try:
                # Add grade using service
                self.service.grade_student(student_id, discipline_id, grade_value)
                
                # No direct undo/redo for grades as they don't have a unique ID
                # We would need to implement a more complex undo/redo mechanism
                
                self.refresh_grades()
                QMessageBox.information(self, "Success", f"Grade added successfully!")
            except Id_Error as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def delete_grade(self, grade, row):
        """Delete a grade"""
        confirm = QMessageBox.question(
            self, "Confirm Deletion", 
            f"Are you sure you want to delete this grade?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                # Get grade repository
                grade_repo = self.service._Services__grade_repo
                
                # Remove the grade from the list
                grades = grade_repo.get_list_of_grades
                grades.remove(grade)
                
                # Save the updated list
                grade_repo._Grades_TextFile_Repository__save()
                
                self.refresh_grades()
                QMessageBox.information(self, "Success", "Grade deleted successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
    
    def undo_action(self):
        """Undo the last action"""
        try:
            self.undo_service.undo()
            self.refresh_grades()
        except UndoRedoError as e:
            QMessageBox.information(self, "Undo", str(e))
    
    def redo_action(self):
        """Redo the last undone action"""
        try:
            self.undo_service.redo()
            self.refresh_grades()
        except UndoRedoError as e:
            QMessageBox.information(self, "Redo", str(e))

class DashboardGUI(QWidget):
    def __init__(self, service):
        super().__init__()
        self.service = service
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Dashboard")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Statistics section
        stats_frame = QFrame()
        stats_frame.setFrameShape(QFrame.StyledPanel)
        stats_frame.setStyleSheet("background-color: white; border-radius: 10px;")
        stats_layout = QVBoxLayout(stats_frame)
        
        stats_title = QLabel("Statistics")
        stats_title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        stats_layout.addWidget(stats_title)
        
        # Count statistics
        counts_layout = QHBoxLayout()
        
        # Student count
        student_count_frame = QFrame()
        student_count_frame.setStyleSheet("background-color: #3498db; color: white; border-radius: 8px;")
        student_count_layout = QVBoxLayout(student_count_frame)
        
        student_count_label = QLabel("Students")
        student_count_label.setFont(QFont("Segoe UI", 12))
        student_count_layout.addWidget(student_count_label)
        
        student_count = len(self.service._Services__student_repo.get_list_of_students)
        student_count_value = QLabel(str(student_count))
        student_count_value.setFont(QFont("Segoe UI", 24, QFont.Bold))
        student_count_value.setAlignment(Qt.AlignCenter)
        student_count_layout.addWidget(student_count_value)
        
        counts_layout.addWidget(student_count_frame)
        
        # Course count
        course_count_frame = QFrame()
        course_count_frame.setStyleSheet("background-color: #2ecc71; color: white; border-radius: 8px;")
        course_count_layout = QVBoxLayout(course_count_frame)
        
        course_count_label = QLabel("Courses")
        course_count_label.setFont(QFont("Segoe UI", 12))
        course_count_layout.addWidget(course_count_label)
        
        course_count = len(self.service._Services__discipline_repo.get_list_of_disciplines)
        course_count_value = QLabel(str(course_count))
        course_count_value.setFont(QFont("Segoe UI", 24, QFont.Bold))
        course_count_value.setAlignment(Qt.AlignCenter)
        course_count_layout.addWidget(course_count_value)
        
        counts_layout.addWidget(course_count_frame)
        
        # Grade count
        grade_count_frame = QFrame()
        grade_count_frame.setStyleSheet("background-color: #f39c12; color: white; border-radius: 8px;")
        grade_count_layout = QVBoxLayout(grade_count_frame)
        
        grade_count_label = QLabel("Grades")
        grade_count_label.setFont(QFont("Segoe UI", 12))
        grade_count_layout.addWidget(grade_count_label)
        
        grade_count = len(self.service._Services__grade_repo.get_list_of_grades)
        grade_count_value = QLabel(str(grade_count))
        grade_count_value.setFont(QFont("Segoe UI", 24, QFont.Bold))
        grade_count_value.setAlignment(Qt.AlignCenter)
        grade_count_layout.addWidget(grade_count_value)
        
        counts_layout.addWidget(grade_count_frame)
        
        stats_layout.addLayout(counts_layout)
        
        # Top students section
        top_students_label = QLabel("Top Students")
        top_students_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        stats_layout.addWidget(top_students_label)
        
        # Get top students
        try:
            top_students = self.service.get_students_with_best_school_situation()[:5]  # Top 5
            
            if top_students:
                for i, student_data in enumerate(top_students):
                    student_item = QFrame()
                    student_item.setStyleSheet("background-color: #f8f9fa; border-radius: 5px; margin: 5px;")
                    student_layout = QHBoxLayout(student_item)
                    
                    rank_label = QLabel(f"#{i+1}")
                    rank_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
                    student_layout.addWidget(rank_label)
                    
                    student_name = QLabel(student_data[0].get_student_name)
                    student_name.setFont(QFont("Segoe UI", 10))
                    student_layout.addWidget(student_name)
                    
                    avg_grade = QLabel(f"Average: {student_data[1]:.2f}")
                    avg_grade.setAlignment(Qt.AlignRight)
                    student_layout.addWidget(avg_grade)
                    
                    stats_layout.addWidget(student_item)
            else:
                no_data_label = QLabel("No student data available")
                no_data_label.setAlignment(Qt.AlignCenter)
                stats_layout.addWidget(no_data_label)
        except Exception as e:
            error_label = QLabel(f"Could not load top students: {str(e)}")
            error_label.setAlignment(Qt.AlignCenter)
            stats_layout.addWidget(error_label)
        
        layout.addWidget(stats_frame)
        
        # Add spacer
        layout.addStretch()

class SettingsGUI(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("Settings")
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Settings frame
        settings_frame = QFrame()
        settings_frame.setFrameShape(QFrame.StyledPanel)
        settings_frame.setStyleSheet("background-color: white; border-radius: 10px;")
        settings_layout = QVBoxLayout(settings_frame)
        
        # Application settings
        app_settings_label = QLabel("Application Settings")
        app_settings_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        settings_layout.addWidget(app_settings_label)
        
        # Data file locations
        data_files_label = QLabel("Data File Locations")
        data_files_label.setFont(QFont("Segoe UI", 12))
        settings_layout.addWidget(data_files_label)
        
        # Student data file
        student_file_layout = QHBoxLayout()
        student_file_label = QLabel("Student Data File:")
        student_file_path = QLineEdit("data/students.txt")
        student_file_path.setReadOnly(True)
        student_file_browse = QPushButton("Browse")
        student_file_layout.addWidget(student_file_label)
        student_file_layout.addWidget(student_file_path)
        student_file_layout.addWidget(student_file_browse)
        settings_layout.addLayout(student_file_layout)
        
        # Course data file
        course_file_layout = QHBoxLayout()
        course_file_label = QLabel("Course Data File:")
        course_file_path = QLineEdit("data/disciplines.txt")
        course_file_path.setReadOnly(True)
        course_file_browse = QPushButton("Browse")
        course_file_layout.addWidget(course_file_label)
        course_file_layout.addWidget(course_file_path)
        course_file_layout.addWidget(course_file_browse)
        settings_layout.addLayout(course_file_layout)
        
        # Grade data file
        grade_file_layout = QHBoxLayout()
        grade_file_label = QLabel("Grade Data File:")
        grade_file_path = QLineEdit("data/grades.txt")
        grade_file_path.setReadOnly(True)
        grade_file_browse = QPushButton("Browse")
        grade_file_layout.addWidget(grade_file_label)
        grade_file_layout.addWidget(grade_file_path)
        grade_file_layout.addWidget(grade_file_browse)
        settings_layout.addLayout(grade_file_layout)
        
        # About section
        about_label = QLabel("About")
        about_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        settings_layout.addWidget(about_label)
        
        about_text = QLabel(
            "Digital Student Catalogue\n"
            "Version 1.0.0\n\n"
            "A comprehensive student management system for educational institutions.\n"
            "Manage students, courses, and grades with ease."
        )
        about_text.setWordWrap(True)
        about_text.setAlignment(Qt.AlignCenter)
        settings_layout.addWidget(about_text)
        
        layout.addWidget(settings_frame)
        
        # Add spacer
        layout.addStretch()

class MainApplicationGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Digital Student Catalogue")
        self.setMinimumSize(1200, 800)
        
        # Initialize services
        self.init_services()
        
        # Center the window
        self.center()
        
        # Set up the main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create sidebar
        sidebar = QFrame()
        sidebar.setMaximumWidth(250)
        sidebar.setMinimumWidth(250)
        sidebar.setStyleSheet("background-color: #2c3e50;")
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # App title in sidebar
        title_container = QFrame()
        title_container.setStyleSheet("background-color: #1a2530; padding: 15px;")
        title_container.setMinimumHeight(100)
        title_layout = QVBoxLayout(title_container)
        
        app_title = QLabel("Digital Student\nCatalogue")
        app_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        app_title.setStyleSheet("color: white;")
        app_title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_layout.addWidget(app_title)
        
        sidebar_layout.addWidget(title_container)
        
        # Navigation buttons
        self.student_btn = SidebarButton("Student Management", "icons/student.png")
        self.course_btn = SidebarButton("Course Management", "icons/course.png")
        self.enrollment_btn = SidebarButton("Grade Management", "icons/enrollment.png")
        self.dashboard_btn = SidebarButton("Dashboard", "icons/dashboard.png")
        self.settings_btn = SidebarButton("Settings", "icons/settings.png")
        
        sidebar_layout.addWidget(self.student_btn)
        sidebar_layout.addWidget(self.course_btn)
        sidebar_layout.addWidget(self.enrollment_btn)
        sidebar_layout.addWidget(self.dashboard_btn)
        sidebar_layout.addWidget(self.settings_btn)
        
        # Add spacer
        sidebar_layout.addStretch()
        
        # Version info
        version_label = QLabel("Version 1.0.0")
        version_label.setStyleSheet("color: #7f8c8d; padding: 15px;")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)
        
        # Add sidebar to main layout
        main_layout.addWidget(sidebar)
        
        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #f5f6fa;")
        main_layout.addWidget(self.stacked_widget)
        
        # Create pages
        self.student_page = QWidget()
        self.course_page = QWidget()
        self.enrollment_page = QWidget()
        self.dashboard_page = QWidget()
        self.settings_page = QWidget()
        
        # Set up student management page
        student_layout = QVBoxLayout(self.student_page)
        student_layout.setContentsMargins(0, 0, 0, 0)
        self.student_gui = StudentManagementGUI(self.service, self.undo_service)
        student_layout.addWidget(self.student_gui)
        
        # Set up course management page
        course_layout = QVBoxLayout(self.course_page)
        course_layout.setContentsMargins(0, 0, 0, 0)
        self.course_gui = CourseManagementGUI(self.service, self.undo_service)
        course_layout.addWidget(self.course_gui)
        
        # Set up enrollment management page
        enrollment_layout = QVBoxLayout(self.enrollment_page)
        enrollment_layout.setContentsMargins(0, 0, 0, 0)
        self.enrollment_gui = EnrollmentManagementGUI(self.service, self.undo_service)
        enrollment_layout.addWidget(self.enrollment_gui)
        
        # Set up dashboard page
        dashboard_layout = QVBoxLayout(self.dashboard_page)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        self.dashboard_gui = DashboardGUI(self.service)
        dashboard_layout.addWidget(self.dashboard_gui)
        
        # Set up settings page
        settings_layout = QVBoxLayout(self.settings_page)
        settings_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_gui = SettingsGUI()
        settings_layout.addWidget(self.settings_gui)
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.student_page)
        self.stacked_widget.addWidget(self.course_page)
        self.stacked_widget.addWidget(self.enrollment_page)
        self.stacked_widget.addWidget(self.dashboard_page)
        self.stacked_widget.addWidget(self.settings_page)
        
        # Connect sidebar buttons
        self.student_btn.clicked.connect(lambda: self.change_page(0))
        self.course_btn.clicked.connect(lambda: self.change_page(1))
        self.enrollment_btn.clicked.connect(lambda: self.change_page(2))
        self.dashboard_btn.clicked.connect(lambda: self.change_page(3))
        self.settings_btn.clicked.connect(lambda: self.change_page(4))
        
        # Set default page
        self.change_page(0)
    
    
    def init_services(self):
        """Initialize the services and repositories"""
        try:
            # Initialize repositories
            student_repo = Students_TextFile_Repository([],"D:\\TraeAI\\Digital-Student--Catalogue\\src\\data\\students.txt")
            discipline_repo = Disciplines_TextFile_Repository([],"D:\\TraeAI\\Digital-Student--Catalogue\\src\\data\\disciplines.txt")
            grade_repo = Grades_TextFile_Repository([],"D:\\TraeAI\\Digital-Student--Catalogue\\src\\data\\grades.txt")
            
            # Initialize services
            self.undo_service = UndoService()
            self.service = Services(student_repo, discipline_repo, grade_repo)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to initialize services: {str(e)}")
            sys.exit(1)
    
    def change_page(self, index):
        """Change the current page in the stacked widget"""
        self.stacked_widget.setCurrentIndex(index)
        
        # Update button states
        self.student_btn.setChecked(index == 0)
        self.course_btn.setChecked(index == 1)
        self.enrollment_btn.setChecked(index == 2)
        self.dashboard_btn.setChecked(index == 3)
        self.settings_btn.setChecked(index == 4)
    
    def center(self):
        """Center the window on the screen"""
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def closeEvent(self, event):
        """Handle the close event"""
        reply = QMessageBox.question(
            self, "Exit Confirmation",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    window = MainApplicationGUI()
    window.show()
    sys.exit(app.exec_())

# Add this class before the MainApplicationGUI class

class SidebarButton(QPushButton):
    def __init__(self, text, icon_path=None):
        super().__init__(text)
        self.setCheckable(True)
        self.setAutoExclusive(True)
        self.setCursor(Qt.PointingHandCursor)
        
        # Set minimum size
        self.setMinimumHeight(50)
        
        # Set style
        self.setStyleSheet("""
            QPushButton {
                border: none;
                border-left: 4px solid transparent;
                color: #ecf0f1;
                text-align: left;
                padding: 10px 10px 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
            QPushButton:checked {
                background-color: #34495e;
                border-left: 4px solid #3498db;
            }
        """)
        
        # Add icon if provided
        if icon_path:
            try:
                icon = QIcon(icon_path)
                self.setIcon(icon)
                self.setIconSize(QSize(20, 20))
            except:
                # If icon loading fails, just continue without an icon
                pass
if __name__ == "__main__":
    main()