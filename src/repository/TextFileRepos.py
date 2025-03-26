from src.repository.MemoryRepos import Students_Memory_Repository, Disciplines_Memory_Repository, Grades_Memory_Repository
from src.domain.Domain import Student, Discipline, Grade
from src.repository.MemoryRepos import Id_Error

class Students_TextFile_Repository(Students_Memory_Repository):
    def __init__(self, initial_list, file_name: str):
        super().__init__(initial_list)
        self.__file_name = file_name
        with open(self.__file_name, "r") as file:
            content = file.read()
            if content:
                self._data = []
                self.__load()
            else:
                self.__save()

    @staticmethod
    def __create_student_from_text(student):
        student = student.strip()
        student = student.split(",")
        return Student(int(student[0]), student[1])

    def __load(self):
        """
        The function that loads the students from the file
        :return: Nothing, the list is modified
        """
        try:
            file_in = open(self.__file_name, "r")
            student_list_from_file = file_in.readlines()
            for student in student_list_from_file:
                self._data.append(self.__create_student_from_text(student))
            file_in.close()
        except FileNotFoundError as fnf_error:
            self._data = []
            raise ValueError(fnf_error)

    def __save(self):
        """
        The function that saves the students to the file
        :return: Nothing, the list is modified
        """
        file_out = open(self.__file_name, "w")
        for student in self._data:
            file_out.write(str(student.get_student_id) + "," + student.get_student_name + "\n")
        file_out.close()

    def add_student(self, student_id: int, student_name: str) -> None:
        """
        The function that adds a student to the list, and saves the list to the file
        It calls the add_student method from the parent class
        :param student_id: the id of the student(should be unique)
        :param student_name: the name of the student(string)
        :return: nothing, the list is modified
        """
        super().add_student(student_id, student_name)
        self.__save()

    def remove_student(self, student_id: int) -> None:
        """
        The function that removes a student from the list, and saves the list to the file
        It calls the remove_student method from the parent class
        :param student_id: The id of the student
        :return: nothing, the list is modified
        """
        super().remove_student(student_id)
        self.__save()

    def update_student(self, student_id: int, new_name: str) -> None:
        """
        The function that updates a student's name, and saves the list to the file
        It calls the update_student method from the parent class
        :param student_id: the id of the student
        :param new_name: the new name of the student with the given id
        :return: nothing, the list is modified
        """
        super().update_student(student_id, new_name)
        self.__save()

class Disciplines_TextFile_Repository(Disciplines_Memory_Repository):
    def __init__(self, initial_list, file_name: str):
        super().__init__(initial_list)
        self.__file_name = file_name
        with open(self.__file_name, "r") as file:
            content = file.read()
            if content:
                self._data = []
                self.__load()
            else:
                self.__save()

    @staticmethod
    def __create_discipline_from_text(discipline : str):
        discipline = discipline.strip()
        discipline = discipline.split(",")
        return Discipline(int(discipline[0]), discipline[1])

    def __load(self):
        """
        The function that loads the disciplines from the file
        :return: nothing, the list is modified
        """
        try:
            file_in = open(self.__file_name, "r")
            discipline_list_from_file = file_in.readlines()
            for discipline in discipline_list_from_file:
                self._data.append(self.__create_discipline_from_text(discipline))
            file_in.close()
        except FileNotFoundError as fnf_error:
            self._data = []
            raise ValueError(fnf_error)

    def __save(self):
        """
        The function that saves the disciplines to the file
        :return: nothing, the list is modified
        """
        file_out = open(self.__file_name, "w")
        for discipline in self._data:
            file_out.write(str(discipline.get_discipline_id) + "," + discipline.get_discipline_name + "\n")
        file_out.close()

    def add_discipline(self, discipline_id: int, discipline_name: str) -> None:
        """
        The function that adds a discipline to the list, and saves the list to the file
        :param discipline_id: the id of the discipline(should be unique)
        :param discipline_name: the name of the discipline(string)
        :return: nothing, the list is modified
        """
        super().add_discipline(discipline_id, discipline_name)
        self.__save()

    def remove_discipline(self, discipline_id: int) -> None:
        """
        The function that removes a discipline from the list, and saves the list to the file
        :param discipline_id: the id of the discipline
        :return: nothing, the list is modified
        """
        super().remove_discipline(discipline_id)
        self.__save()

    def update_discipline(self, discipline_id: int, new_name: str) -> None:
        """
        The function that updates a discipline's name, and saves the list to the file
        :param discipline_id: the id of the discipline
        :param new_name: the new name of the discipline with the given id
        :return: nothing, the list is modified
        """
        super().update_discipline(discipline_id, new_name)
        self.__save()

class Grades_TextFile_Repository(Grades_Memory_Repository):
    def __init__(self, initial_list, file_name: str):
        super().__init__(initial_list)
        self.__file_name = file_name
        with open(self.__file_name, "r") as file:
            content = file.read()
            if content:
                self._data = []
                self.__load()
            else:
                self.__save()

    @staticmethod
    def __create_grade_from_text(grade):
        grade = grade.strip()
        grade = grade.split(",")
        return Grade(int(grade[0]), int(grade[1]), int(grade[2]))

    def __load(self):
        try:
            file_in = open(self.__file_name, "r")
            grade_list_from_file = file_in.readlines()
            for grade in grade_list_from_file:
                self._data.append(self.__create_grade_from_text(grade))
            file_in.close()
        except FileNotFoundError as fnf_error:
            self._data = []
            raise ValueError(fnf_error)

    def __save(self):
        file_out = open(self.__file_name, "w")
        for grade in self._data:
            file_out.write(str(grade.get_student_id) + "," + str(grade.get_discipline_id) + "," + str(grade.get_grade_value) + "\n")
        file_out.close()

    def add_grade(self, grade : Grade) -> None:
        super().add_grade(grade)
        self.__save()

    def remove_discipline_grades(self, discipline_id: int) -> None:
        super().remove_discipline_grades(discipline_id)
        self.__save()

    def remove_student_grades(self, student_id: int) -> None:
        super().remove_student_grades(student_id)
        self.__save()
