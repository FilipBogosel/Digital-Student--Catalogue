# Assignment 8 -3 entities
#
# -console based app
# -3 functionalities
#
# 1.Manage the list
# ->add
# ->remove
# ->update
# for all 3 entities
# 2.Search/...
# 3.
#
# layered arhitecture:
# Ui
# service
# repository
# -Memory
# -Binary file
# -Text file
#
# Tests + specifications required for functions related to first functionality
# PyUnit to implement tests
#
# Validations of user input- app should not crash(recomanded to implement a validation class for the domain entities)
# Use custom exception classes(Ex: GradeError)
# Create settings.properties
# Generate 20 random entities at startup if the list is empty
# Hint - the faker library can generate many of the required class fields
# MyProblem : 1
#1. Manage students and disciplines. The user can add, remove, update, and list both students
# and disciplines.
#2. Grade students at a given discipline. Any student may receive one or several grades at
# any discipline. Deleting a student also removes their grades. Deleting a discipline deletes
# all grades at that discipline for all students.
#3. Search for disciplines/students based on ID or name/title. The search must work using
# case-insensitive, partial string matching, and must return all matching disciplines/students.
#4. Create statistics:
# -All students failing at one or more disciplines (students having an average <5 for a discipline are failing it)
# -Students with the best school situation, sorted in descending order of their aggregated average (the
# average between their average grades per discipline)
# -All disciplines at which there is at least one grade, sorted in descending order of the average grade(s)
# received by all students
#Implement a solid undo/redo mechanism using the Command design pattern. Each operation will be
# encapsulated in a command object. We will have a stack for undo and one for redo.


class Student:#the class for the student entity
    def __init__(self, student_id, student_name):
        self.__student_id = student_id
        self.__student_name = student_name

    @property
    def get_student_id(self):
        return self.__student_id

    @property
    def get_student_name(self):
        return self.__student_name


    def set_student_name(self, new_name):
        self.__student_name = new_name

    def __str__(self):
        return str(self.get_student_id) + "," + self.get_student_name


class Discipline:#the class for the discipline entity
    def __init__(self, discipline_id, discipline_name):
        self.__discipline_id = discipline_id
        self.__discipline_name = discipline_name

    @property
    def get_discipline_id(self):
        return self.__discipline_id

    @property
    def get_discipline_name(self):
        return self.__discipline_name

    def set_discipline_name(self, new_name):
        self.__discipline_name = new_name

    def __str__(self):
        return str(self.get_discipline_id) + "," + self.get_discipline_name


class Grade:#the class for the grade entity
    def __init__(self, discipline_id, student_id, grade_value):
        self.__discipline_id = discipline_id
        self.__student_id = student_id
        self.__grade_value = grade_value

    @property
    def get_discipline_id(self):
        return self.__discipline_id
    @property
    def get_student_id(self):
        return self.__student_id
    @property
    def get_grade_value(self):
        return self.__grade_value

    def __str__(self):
        return str(self.get_student_id) + "," + str(self.get_discipline_id) + "," + str(self.get_grade_value)


