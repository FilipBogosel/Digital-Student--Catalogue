import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from texttable import Texttable
from src.repository.MemoryRepos import *
from src.repository.TextFileRepos import *
from src.repository.BinaryRepos import *
from src.services.Services import Services
from src.services.undo_service import UndoService, Operation, FunctionCall, CascadedOperation


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("School Management System")
        self.root.geometry("1200x800")

        # Initialize repositories and services
        self.student_repo = None
        self.discipline_repo = None
        self.grade_repo = None
        self.services = None
        self.undo_service = UndoService()

        self.choose_repositories()
        self.initialize_services()
        self.setup_ui()

    def choose_repositories(self):
        with open("D:\\Github\\Digital-Student--Catalogue\\src\\data\\settings.properties", 'r') as f:
            lines = f.readlines()
            repo_type = lines[0].split('=')[1].strip()
            files = [line.split('=')[1].strip().strip('"') for line in lines[1:]]

        if repo_type == "memory":
            self.student_repo = Students_Memory_Repository([])
            self.discipline_repo = Disciplines_Memory_Repository([])
            self.grade_repo = Grades_Memory_Repository([])
        elif repo_type == "text":
            self.student_repo = Students_TextFile_Repository([], files[0])
            self.discipline_repo = Disciplines_TextFile_Repository([], files[1])
            self.grade_repo = Grades_TextFile_Repository([], files[2])
        elif repo_type == "binary":
            self.student_repo = Students_Binary_Repository([], files[0])
            self.discipline_repo = Disciplines_Binary_Repository([], files[1])
            self.grade_repo = Grades_Binary_Repository([], files[2])

    def initialize_services(self):
        self.services = Services(
            self.student_repo,
            self.discipline_repo,
            self.grade_repo
        )

    def setup_ui(self):
        self.notebook = ttk.Notebook(self.root)

        # Students Tab
        self.student_frame = ttk.Frame(self.notebook)
        self.setup_student_tab()

        # Disciplines Tab
        self.discipline_frame = ttk.Frame(self.notebook)
        self.setup_discipline_tab()

        # Grades Tab
        self.grade_frame = ttk.Frame(self.notebook)
        self.setup_grade_tab()

        # Statistics Tab
        self.stats_frame = ttk.Frame(self.notebook)
        self.setup_stats_tab()

        self.notebook.pack(expand=True, fill='both')
        self.setup_undo_redo()

    def setup_student_tab(self):
        self.notebook.add(self.student_frame, text="Students")

        # Treeview
        self.student_tree = ttk.Treeview(self.student_frame, columns=("ID", "Name"), show='headings')
        self.student_tree.heading("ID", text="Student ID")
        self.student_tree.heading("Name", text="Name")
        self.student_tree.pack(fill='both', expand=True, padx=10, pady=10)

        # Controls
        btn_frame = ttk.Frame(self.student_frame)
        ttk.Button(btn_frame, text="Add", command=self.student_repo.add_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove", command=self.student_repo.remove_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.student_repo.update_student).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_students).pack(side=tk.RIGHT, padx=5)
        btn_frame.pack(fill='x', padx=10, pady=5)

        self.refresh_students()

    def setup_discipline_tab(self):
        self.notebook.add(self.discipline_frame, text="Disciplines")

        self.discipline_tree = ttk.Treeview(self.discipline_frame, columns=("ID", "Name"), show='headings')
        self.discipline_tree.heading("ID", text="Discipline ID")
        self.discipline_tree.heading("Name", text="Name")
        self.discipline_tree.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.discipline_frame)
        ttk.Button(btn_frame, text="Add", command=self.discipline_repo.add_discipline).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove", command=self.discipline_repo.remove_discipline).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.discipline_repo.update_discipline).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_disciplines).pack(side=tk.RIGHT, padx=5)
        btn_frame.pack(fill='x', padx=10, pady=5)

        self.refresh_disciplines()

    def setup_grade_tab(self):
        self.notebook.add(self.grade_frame, text="Grades")
        self.grade_tree = ttk.Treeview(self.grade_frame, columns=("Student ID", "Discipline ID", "Grade"), show='headings')
        self.grade_tree.heading("Student ID", text="Student ID")
        self.grade_tree.heading("Discipline ID", text="Discipline ID")
        self.grade_tree.heading("Grade", text="Grade")
        self.grade_tree.pack(fill='both', expand=True, padx=10, pady=10)

        form_frame = ttk.Frame(self.grade_frame)
        ttk.Label(form_frame, text="Student ID:").grid(row=0, column=0, padx=5, pady=5)
        self.student_id_entry = ttk.Entry(form_frame)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Discipline ID:").grid(row=1, column=0, padx=5, pady=5)
        self.discipline_id_entry = ttk.Entry(form_frame)
        self.discipline_id_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Grade:").grid(row=2, column=0, padx=5, pady=5)
        self.grade_entry = ttk.Entry(form_frame)
        self.grade_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Add Grade", command=self.add_grade).grid(row=3, columnspan=2, pady=10)
        form_frame.pack(pady=20)

    def setup_stats_tab(self):
        self.notebook.add(self.stats_frame, text="Statistics")

        self.stats_text = tk.Text(self.stats_frame, wrap=tk.WORD)
        self.stats_text.pack(fill='both', expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(self.stats_frame)
        ttk.Button(btn_frame, text="Failing Students", command=self.show_failing).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Best Students", command=self.show_best_students).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Discipline Averages", command=self.show_discipline_averages).pack(side=tk.LEFT,
                                                                                                      padx=5)
        btn_frame.pack(fill='x', padx=10, pady=5)

    def setup_undo_redo(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill='x', pady=10)
        ttk.Button(control_frame, text="Undo", command=self.undo).pack(side=tk.LEFT, padx=20)
        ttk.Button(control_frame, text="Redo", command=self.redo).pack(side=tk.RIGHT, padx=20)

    # Student operations
    def add_student(self):
        student_id = simpledialog.askinteger("Add Student", "Enter student ID:")
        student_name = simpledialog.askstring("Add Student", "Enter student name:")
        if student_id and student_name:
            try:
                self.student_repo.add_student(student_id, student_name)
                self.record_undo(
                    FunctionCall(self.student_repo.remove_student, student_id),
                    FunctionCall(self.student_repo.add_student, student_id, student_name)
                )
                self.refresh_students()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def remove_student(self):
        selected = self.student_tree.selection()
        if selected:
            student_id = self.student_tree.item(selected[0])['values'][0]
            try:
                student = self.student_repo.find_by_id(student_id)
                grades = self.grade_repo.find_by_student_id(student_id)

                # Create cascaded operation
                cascade = CascadedOperation()

                # Student removal
                cascade.add_undo_function(FunctionCall(
                    self.student_repo.add_student,
                    student.get_student_id,
                    student.get_student_name
                ))
                cascade.add_redo_function(FunctionCall(
                    self.student_repo.remove_student,
                    student.get_student_id
                ))

                # Grade removals
                for grade in grades:
                    cascade.add_undo_function(FunctionCall(
                        self.grade_repo.add_grade,
                        grade
                    ))
                    cascade.add_redo_function(FunctionCall(
                        self.grade_repo.remove_grade,
                        grade
                    ))

                self.undo_service.record(cascade)
                self.services.remove_student_service(student_id)
                self.refresh_students()
                self.refresh_disciplines()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def update_student(self):
        selected = self.student_tree.selection()
        if selected:
            student_id = self.student_tree.item(selected[0])['values'][0]
            new_name = simpledialog.askstring("Update Student", "Enter new name:")
            if new_name:
                try:
                    old_name = self.student_repo.find_by_id(student_id).get_student_name
                    self.student_repo.update_student(student_id, new_name)
                    self.record_undo(
                        FunctionCall(self.student_repo.update_student, student_id, old_name),
                        FunctionCall(self.student_repo.update_student, student_id, new_name)
                    )
                    self.refresh_students()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def refresh_students(self):
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)
        for student in self.student_repo.get_list_of_students:
            self.student_tree.insert("", tk.END, values=(
                student.get_student_id,
                student.get_student_name
            ))

    def refresh_disciplines(self):
        for item in self.discipline_tree.get_children():
            self.discipline_tree.delete(item)
        for discipline in self.discipline_repo.get_list_of_disciplines:
            self.discipline_tree.insert("", tk.END, values=(
                discipline.get_discipline_id,
                discipline.get_discipline_name
            ))

    def run(self):
        self.root.mainloop()

    # Other necessary methods (undo/redo, statistics, etc.)...
    def record_undo(self, undo_function, redo_function):
        self.undo_service.record(Operation(undo_function, redo_function))

    def undo(self):
        self.undo_service.undo()
        self.refresh_students()
        self.refresh_disciplines()
    def redo(self):
        self.undo_service.redo()
        self.refresh_students()
        self.refresh_disciplines()
    def add_grade(self):
        student_id = int(self.student_id_entry.get())
        discipline_id = int(self.discipline_id_entry.get())
        grade_value = int(self.grade_entry.get())
        try:
            self.services.add_grade_service(student_id, discipline_id, grade_value)
            self.record_undo(
                FunctionCall(self.services.remove_grade_service, student_id, discipline_id),
                FunctionCall(self.services.add_grade_service, student_id, discipline_id, grade_value)
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def show_failing(self):
        failing_students = self.services.get_students_failing()
        self.stats_text.delete(1.0, tk.END)
        for student in failing_students:
            self.stats_text.insert(tk.END, str(student) + "\n")
    def show_best_students(self):
        best_students = self.services.get_best_students()
        self.stats_text.delete(1.0, tk.END)
        for student in best_students:
            self.stats_text.insert(tk.END, str(student) + "\n")
    def show_discipline_averages(self):
        discipline_averages = self.services.get_discipline_averages()
        self.stats_text.delete(1.0, tk.END)
        for discipline in discipline_averages:
            self.stats_text.insert(tk.END, str(discipline) + "\n")
    def add_discipline(self):
        discipline_id = simpledialog.askinteger("Add Discipline", "Enter discipline ID:")
        discipline_name = simpledialog.askstring("Add Discipline", "Enter discipline name:")
        if discipline_id and discipline_name:
            try:
                self.discipline_repo.add_discipline(discipline_id, discipline_name)
                self.record_undo(
                    FunctionCall(self.discipline_repo.remove_discipline, discipline_id),
                    FunctionCall(self.discipline_repo.add_discipline, discipline_id, discipline_name)
                )
                self.refresh_disciplines()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    def remove_discipline(self):
        selected = self.discipline_tree.selection()
        if selected:
            discipline_id = self.discipline_tree.item(selected[0])['values'][0]
            try:
                discipline = self.discipline_repo.find_by_id(discipline_id)
                grades = self.grade_repo.find_by_discipline_id(discipline_id)
                cascade = CascadedOperation()
                cascade.add_undo_function(FunctionCall(
                    self.discipline_repo.add_discipline,
                    discipline.get_discipline_id,
                    discipline.get_discipline_name
                ))
                cascade.add_redo_function(FunctionCall(
                    self.discipline_repo.remove_discipline,
                    discipline.get_discipline_id
                ))
                for grade in grades:
                    cascade.add_undo_function(FunctionCall(
                        self.grade_repo.add_grade,
                        grade
                    ))
                    cascade.add_redo_function(FunctionCall(
                        self.grade_repo.remove_grade,
                        grade
                    ))
                self.undo_service.record(cascade)
                self.services.remove_discipline_service(discipline_id)
                self.refresh_disciplines()
                self.refresh_students()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    def update_discipline(self):
        selected = self.discipline_tree.selection()
        if selected:
            discipline_id = self.discipline_tree.item(selected[0])['values'][0]
            new_name = simpledialog.askstring("Update Discipline", "Enter new name:")
            if new_name:
                try:
                    old_name = self.discipline_repo.find_by_id(discipline_id).get_discipline_name
                    self.discipline_repo.update_discipline(discipline_id, new_name)
                    self.record_undo(
                        FunctionCall(self.discipline_repo.update_discipline, discipline_id, old_name),
                        FunctionCall(self.discipline_repo.update_discipline, discipline_id, new_name)
                    )
                    self.refresh_disciplines()
                except Exception as e:
                    messagebox.showerror("Error", str(e))
    def refresh_grades(self):
        for item in self.grade_tree.get_children():
            self.grade_tree.delete(item)
        for grade in self.grade_repo.get_list_of_grades:
            self.grade_tree.insert("", tk.END, values=(
                grade.get_student_id,
                grade.get_discipline_id,
                grade.get_grade_value
            ))
    def refresh_stats(self):
        self.stats_text.delete(1.0, tk.END)
    def remove_grade(self):
        selected = self.grade_tree.selection()
        if selected:
            student_id = self.grade_tree.item(selected[0])['values'][0]
            discipline_id = self.grade_tree.item(selected[0])['values'][1]
            try:
                grade = self.grade_repo.find_by_ids(student_id, discipline_id)
                self.services.remove_grade_service(student_id, discipline_id)
                self.record_undo(
                    FunctionCall(self.services.add_grade_service, student_id, discipline_id, grade.get_grade_value),
                    FunctionCall(self.services.remove_grade_service, student_id, discipline_id)
                )
                self.refresh_grades()
            except Exception as e:
                messagebox.showerror("Error", str(e))
    def update_grade(self):
        selected = self.grade_tree.selection()
        if selected:
            student_id = self.grade_tree.item(selected[0])['values'][0]
            discipline_id = self.grade_tree.item(selected[0])['values'][1]
            new_grade = simpledialog.askinteger("Update Grade", "Enter new grade:")
            if new_grade:
                try:
                    old_grade = self.grade_repo.find_by_ids(student_id, discipline_id).get_grade_value
                    self.services.update_grade_service(student_id, discipline_id, new_grade)
                    self.record_undo(
                        FunctionCall(self.services.update_grade_service, student_id, discipline_id, old_grade),
                        FunctionCall(self.services.update_grade_service, student_id, discipline_id, new_grade)
                    )
                    self.refresh_grades()
                except Exception as e:
                    messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    ui = GUI()
    ui.run()