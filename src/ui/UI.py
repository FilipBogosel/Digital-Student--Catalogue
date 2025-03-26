from texttable import Texttable

from src.repository.MemoryRepos import Students_Memory_Repository, Disciplines_Memory_Repository, \
    Grades_Memory_Repository, Id_Error, Grade_Error
from src.services.Services import Services
from src.repository.TextFileRepos import Students_TextFile_Repository, Disciplines_TextFile_Repository, \
    Grades_TextFile_Repository
from src.repository.BinaryRepos import Students_Binary_Repository, Disciplines_Binary_Repository, \
    Grades_Binary_Repository
from src.domain.Domain import Student, Discipline, Grade
from src.services.undo_service import *


class UI:
    def __init__(self):
        self.__student_repo = Students_Memory_Repository([])
        self.__discipline_repo = Disciplines_Memory_Repository([])
        self.__grade_repo = Grades_Memory_Repository([])
        self.choose_repo()
        self.__services = Services(self.__student_repo, self.__discipline_repo, self.__grade_repo)
        self.__undo_service = UndoService()

    def choose_repo(self):
        with open("D:\\Github\\Digital-Student--Catalogue\\src\\data\\settings.properties", 'r') as file:
            lines = file.readlines()
            option = lines[0].split('=')[1].strip()
            files = [line.split('=')[1].strip().strip('"') for line in lines[1:]]

            if option == 'memory':
                self.__student_repo = Students_Memory_Repository([])
                self.__discipline_repo = Disciplines_Memory_Repository([])
                self.__grade_repo = Grades_Memory_Repository([])
            elif option == 'text':
                self.__student_repo = Students_TextFile_Repository([], files[0])
                self.__discipline_repo = Disciplines_TextFile_Repository([], files[1])
                self.__grade_repo = Grades_TextFile_Repository([], files[2])
            elif option == 'binary':
                self.__student_repo = Students_Binary_Repository([], files[0])
                self.__discipline_repo = Disciplines_Binary_Repository([], files[1])
                self.__grade_repo = Grades_Binary_Repository([], files[2])
            else:
                raise ValueError('Invalid option in settings.properties')

        self.__services = Services(self.__student_repo, self.__discipline_repo, self.__grade_repo)

    def display_students_texttable(self):
        from texttable import Texttable
        table = Texttable()
        table.add_row(["ID", "Name"])
        students = self.__student_repo.get_list_of_students
        for student in students:
            table.add_row([student.get_student_id, student.get_student_name])
        print(table.draw())

    def display_disciplines_texttable(self):
        from texttable import Texttable
        table = Texttable()
        table.add_row(["ID", "Name"])
        disciplines = self.__discipline_repo.get_list_of_disciplines
        for discipline in disciplines:
            table.add_row([discipline.get_discipline_id, discipline.get_discipline_name])
        print(table.draw())

    def display_grades_texttable(self):
        from texttable import Texttable
        table = Texttable()
        table.add_row(["Student ID", "Discipline ID", "Grade"])
        grades = self.__grade_repo.get_list_of_grades
        for grade in grades:
            table.add_row([grade.get_student_id, grade.get_discipline_id, grade.get_grade_value])
        print(table.draw())

    @staticmethod
    def __print_menu():
        print("1. Manage students or disciplines")
        print("2. Grade student")
        print("3. Search for disciplines/students based on ID or name/title")
        print("4. Create statistics")
        print("5. Undo")
        print("6. Redo")
        print("7. Exit")

    def run(self):
        while True:
            self.__print_menu()
            try:
                option = input("Choose an option: ")
                if option == "1":
                    self.manage_students_disciplines()
                elif option == "2":
                    self.manage_grading()
                elif option == "3":
                    self.manage_searching()
                elif option == "4":
                    self.manage_statistics()
                elif option == "5":
                    self.__undo_service.undo()
                elif option == "6":
                    self.__undo_service.redo()
                elif option == "7":
                    break
                elif option == "8":
                    self.display_grades_texttable()
                else:
                    print("Invalid option")
            except (ValueError, Id_Error, Grade_Error, UndoRedoError) as e:
                print(e)

    def manage_statistics(self):
        print("1. Students failing at one or more disciplines")
        print("2. Students with the best school situation")
        print("3. Disciplines with the best school situation")
        option = input("Choose an option: ")
        if option == "1":
            self.display_students_failing()
        elif option == "2":
            self.display_students_with_best_situation()
        elif option == "3":
            self.display_disciplines_with_best_situation()
        else:
            print("Invalid option")

    def manage_grading(self):
        student_id = int(input("Enter the student ID: "))
        discipline_id = int(input("Enter the discipline ID: "))
        grade_value = int(input("Enter the grade value: "))
        self.__services.grade_student(student_id, discipline_id, grade_value)
        # we add the function to the undo stack
        grade = Grade(discipline_id, student_id, grade_value)
        undo_function = FunctionCall(self.__grade_repo.remove_grade, grade)
        redo_function = FunctionCall(self.__grade_repo.add_grade, grade)
        operation = Operation(undo_function, redo_function)
        self.__undo_service.record(operation)

    def manage_students_disciplines(self):
        print("What do you want to manage?")
        print("1. Students")
        print("2. Disciplines")
        option = input("Choose an option: ")
        if option == "1":
            print("1. Add student")
            print("2. Remove student")
            print("3. Update student")
            print("4. List students")
            option1 = input("Choose an option: ")
            if option1 == "1":
                student_id = int(input("Enter the student ID: "))
                student_name = input("Enter the student name: ")
                self.__student_repo.add_student(student_id, student_name)
                undo_function = FunctionCall(self.__student_repo.remove_student, student_id)
                redo_function = FunctionCall(self.__student_repo.add_student, student_id, student_name)
                operation = Operation(undo_function, redo_function)
                self.__undo_service.record(operation)

            elif option1 == "2":
                student_id = int(input("Enter the student ID: "))
                student = self.__student_repo.find_by_id(student_id)
                grades = self.__grade_repo.find_by_student_id(student_id)
                # Create undo and redo functions for student removal
                undo_student = FunctionCall(self.__student_repo.add_student, student_id, student.get_student_name)
                redo_student = FunctionCall(self.__student_repo.remove_student, student_id)
                # Create undo and redo functions for each grade removal
                undo_grades = [FunctionCall(self.__grade_repo.add_grade, grade) for grade in grades]
                redo_grades = [FunctionCall(self.__grade_repo.remove_grade, grade) for grade in grades]
                # Combine all undo and redo functions into cascaded operations
                undo_operations = [undo_student] + undo_grades
                redo_operations = [redo_student] + redo_grades
                # Record the cascaded operation
                cascaded_operation = CascadedOperation()
                for undo_operation in undo_operations:
                    cascaded_operation.add_undo_function(undo_operation)
                for redo_operation in redo_operations:
                    cascaded_operation.add_redo_function(redo_operation)
                self.__undo_service.record(cascaded_operation)
                # Perform the actual removal
                self.__services.remove_student_service(student_id)
            elif option1 == "3":
                student_id = int(input("Enter the student ID: "))
                new_name = input("Enter the new name: ")
                old_name = self.__student_repo.find_by_id(student_id).get_student_name
                self.__student_repo.update_student(student_id, new_name)
                undo_function = FunctionCall(self.__student_repo.update_student, student_id, old_name)
                redo_function = FunctionCall(self.__student_repo.update_student, student_id, new_name)
                operation = Operation(undo_function, redo_function)
                self.__undo_service.record(operation)
            elif option1 == "4":
                self.display_students_texttable()
            else:
                print("Invalid option")
        elif option == "2":
            print("1. Add discipline")
            print("2. Remove discipline")
            print("3. Update discipline")
            print("4. List disciplines")
            option1 = input("Choose an option: ")
            if option1 == "1":
                discipline_id = int(input("Enter the discipline ID: "))
                discipline_name = input("Enter the discipline name: ")
                self.__discipline_repo.add_discipline(discipline_id, discipline_name)
                undo_function = FunctionCall(self.__discipline_repo.remove_discipline, discipline_id)
                redo_function = FunctionCall(self.__discipline_repo.add_discipline, discipline_id, discipline_name)
                operation = Operation(undo_function, redo_function)
                self.__undo_service.record(operation)
            elif option1 == "2":
                discipline_id = int(input("Enter the discipline ID: "))
                discipline = self.__discipline_repo.find_by_id(discipline_id)
                grades = self.__grade_repo.find_by_discipline_id(discipline_id)
                # Create undo and redo functions for discipline removal
                undo_discipline = FunctionCall(self.__discipline_repo.add_discipline, discipline_id, discipline.get_discipline_name)
                redo_discipline = FunctionCall(self.__discipline_repo.remove_discipline, discipline_id)
                # Create undo and redo functions for each grade removal
                undo_grades = [FunctionCall(self.__grade_repo.add_grade, grade) for grade in grades]
                redo_grades = [FunctionCall(self.__grade_repo.remove_grade, grade) for grade in grades]
                # Combine all undo and redo functions into cascaded operations
                undo_operations = [undo_discipline] + undo_grades
                redo_operations = [redo_discipline] + redo_grades
                # Record the cascaded operation
                cascaded_operation = CascadedOperation()
                for undo_operation in undo_operations:
                    cascaded_operation.add_undo_function(undo_operation)
                for redo_operation in redo_operations:
                    cascaded_operation.add_redo_function(redo_operation)
                self.__undo_service.record(cascaded_operation)
                # Perform the actual removal
                self.__services.remove_discipline_service(discipline_id)
            elif option1 == "3":
                discipline_id = int(input("Enter the discipline ID: "))
                new_name = input("Enter the new name: ")
                old_name = self.__discipline_repo.find_by_id(discipline_id).get_discipline_name
                self.__discipline_repo.update_discipline(discipline_id, new_name)
                undo_function = FunctionCall(self.__discipline_repo.update_discipline, discipline_id, old_name)
                redo_function = FunctionCall(self.__discipline_repo.update_discipline, discipline_id, new_name)
                operation = Operation(undo_function, redo_function)
                self.__undo_service.record(operation)

            elif option1 == "4":
                self.display_disciplines_texttable()
            else:
                print("Invalid option")

    def manage_searching(self):
        print("1. Search for students")
        print("2. Search for disciplines")
        option = input("Choose an option: ")
        if option == "1":
            print("1. Search by ID")
            print("2. Search by name")
            option1 = input("Choose an option: ")
            if option1 == "1":
                student_id = int(input("Enter the student ID: "))
                try:
                    student = self.__student_repo.find_by_id(student_id)
                    print(student)
                except Id_Error as ide:
                    print(ide)
            elif option1 == "2":
                student_name = input("Enter the student name: ")
                students = self.__services.search_student_by_name(student_name)
                for student in students:
                    print(student)
                if len(students) == 0:
                    print("No students with similar name found")
            else:
                print("Invalid option")
        elif option == "2":
            print("1. Search by ID")
            print("2. Search by name")
            option1 = input("Choose an option: ")
            if option1 == "1":
                discipline_id = int(input("Enter the discipline ID: "))
                try:
                    discipline = self.__discipline_repo.find_by_id(discipline_id)
                    print(discipline)
                except Id_Error as ide:
                    print(ide)
            elif option1 == "2":
                discipline_name = input("Enter the discipline name: ")
                disciplines = self.__services.search_discipline_by_name(discipline_name)
                for discipline in disciplines:
                    print(discipline)
        else:
            print("Invalid option")

    def display_students_failing(self):
        failed_students_list = self.__services.get_students_failing()
        table = Texttable()
        table.add_row(["ID", "Name"])
        for failed_student in failed_students_list:
            table.add_row([failed_student.get_student_id, failed_student.get_student_name])
        print(table.draw())

    def display_students_with_best_situation(self):
        best_students_list = self.__services.get_best_students()
        table = Texttable()
        table.add_row(["ID", "Name", "Average"])
        for element in best_students_list:
            student = self.__student_repo.find_by_id(element[0])
            table.add_row([student.get_student_id, student.get_student_name, element[1]])
        print(table.draw())

    def display_disciplines_with_best_situation(self):
        best_disciplines = self.__services.get_disciplines_with_best_situation()
        table = Texttable()
        table.add_row(["ID", "Name", "Average"])
        for element in best_disciplines:
            discipline = element[0]
            table.add_row([discipline.get_discipline_id, discipline.get_discipline_name, element[1]])
        print(table.draw())


if __name__ == '__main__':
    ui = UI()

