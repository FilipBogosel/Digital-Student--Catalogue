from audioop import reverse

from src.domain.Domain import Student, Discipline, Grade
from src.repository.MemoryRepos import Students_Memory_Repository, Disciplines_Memory_Repository, \
    Grades_Memory_Repository, Id_Error
from src.repository.TextFileRepos import Students_TextFile_Repository, Disciplines_TextFile_Repository, \
    Grades_TextFile_Repository
from src.repository.BinaryRepos import Students_Binary_Repository, Disciplines_Binary_Repository, \
    Grades_Binary_Repository


class Services:
    def __init__(self, student_repo, discipline_repo, grade_repo):
        self.__student_repo = student_repo
        self.__discipline_repo = discipline_repo
        self.__grade_repo = grade_repo

    def grade_student(self, student_id, discipline_id, grade_value):
        grade = Grade(discipline_id,student_id, grade_value)
        found_student = False
        for student in self.__student_repo.get_list_of_students:
            if student.get_student_id == student_id:
                found_student = True
                break
        if not found_student:
            raise Id_Error("The student with given ID does not exist")
        found_discipline = False
        for discipline in self.__discipline_repo.get_list_of_disciplines:
            if discipline.get_discipline_id == discipline_id:
                found_discipline = True
                break
        if not found_discipline:
            raise Id_Error("The discipline with given ID does not exist")
        self.__grade_repo.add_grade(grade)

    # Remove a student from the list, and also remove all the grades for that student
    def remove_student_service(self, student_id: int) -> None:
        """
        The function that removes a student from the list and also removes all the grades for that student
        :param student_id: The id of the student
        :return: nothing, the list is modified
        """
        self.__student_repo.remove_student(student_id)
        self.__grade_repo.remove_student_grades(student_id)

    # Remove a discipline from the list, and also remove all the grades for that discipline
    def remove_discipline_service(self, discipline_id: int) -> None:
        """
        The function that removes a discipline from the list and also removes all the grades for that discipline
        :param discipline_id: The id of the discipline
        :return: Nothing, the list is modified
        """
        self.__discipline_repo.remove_discipline(discipline_id)
        self.__grade_repo.remove_discipline_grades(discipline_id)

    def search_student_by_name(self, student_name):
        student_name = student_name.strip()  # remove the extra spaces
        student_name = student_name.lower()  # make the name lowercase
        students = self.__student_repo.get_list_of_students
        found_students = []
        for student in students:
            if student.get_student_name.lower().find(student_name) != -1:
                found_students.append(student)

        return found_students

    # Search for a discipline by name
    def search_discipline_by_name(self, discipline_name):
        discipline_name = discipline_name.strip()  # remove the extra spaces
        discipline_name = discipline_name.lower()
        disciplines = self.__discipline_repo.get_list_of_disciplines
        found_disciplines = []
        for discipline in disciplines:
            if discipline.get_discipline_name.lower().find(discipline_name) != -1:
                found_disciplines.append(discipline)

        return found_disciplines

    def get_students_failing(self):
        failed_students_list = []
        grades = self.__grade_repo.get_list_of_grades
        for grade in grades:
            if grade.get_grade_value < 5:
                try:
                    failed_student = self.__student_repo.find_by_id(grade.get_student_id)
                    if failed_student not in failed_students_list:
                        failed_students_list.append(failed_student)
                except Id_Error:
                    continue
        return failed_students_list

    def get_best_students(self):
        average_grades_list = []
        for student in self.__student_repo.get_list_of_students:
            average_grade = 0
            discipline_counter = 0
            for discipline in self.__discipline_repo.get_list_of_disciplines:
                average_grade_at_discipline = self.__grade_repo.get_average_grade_at_discipline(student.get_student_id,
                                                                                                discipline.get_discipline_id)
                average_grade += average_grade_at_discipline
                if average_grade_at_discipline != 0:
                    discipline_counter += 1
            if discipline_counter != 0:
                average_grade = average_grade // discipline_counter
            average_grades_list.append([student.get_student_id, average_grade])

        average_grades_list.sort(key=lambda x: x[1], reverse=True)
        return average_grades_list

    def get_disciplines_with_best_situation(self):
        disciplines_list = []
        for discipline in self.__discipline_repo.get_list_of_disciplines:
            found = False
            for grade in self.__grade_repo.get_list_of_grades:
                if grade.get_discipline_id == discipline.get_discipline_id:
                    found = True
            if found:
                disciplines_list.append(
                    [discipline, self.__grade_repo.get_discipline_status(discipline.get_discipline_id)])

        disciplines_list.sort(key=lambda x: x[1], reverse = True)
        return disciplines_list
