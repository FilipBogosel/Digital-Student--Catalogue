from src.domain.Domain import Student, Discipline, Grade
from faker import Faker
from src.repository.MemoryRepos import Students_Memory_Repository, Disciplines_Memory_Repository, \
    Grades_Memory_Repository
from pickle import dump, load
from src.repository.MemoryRepos import Id_Error


class Students_Binary_Repository(Students_Memory_Repository):
    def __init__(self, initial_list: list, file_name: str):
        super().__init__(initial_list)
        self.__file_name = file_name
        with open(file_name, "rb") as file:
            if file.read(1):
                self.__load()
            else:
                self.__save()

    def __load(self):
        """
        The function that loads the students from the file
        :return: nothing, the list is modified
        """
        try:
            file_in = open(self.__file_name, "rb")
            self._data = load(file_in)
            file_in.close()
        except FileNotFoundError as fnf_error:
            self._data = []
            raise ValueError(fnf_error)

    def __save(self):
        """
        The function that saves the students to the file
        :return: nothing, the list is modified
        """
        file_out = open(self.__file_name, "wb")
        dump(self._data, file_out)
        file_out.close()

    def add_student(self, student_id: int, student_name: str):
        """
        The function that adds a student to the list, and saves the list to the file
        :param student_id: the id of the new student(should be unique)
        :param student_name: the name of the new student
        :return: nothing, the list is modified
        """
        super().add_student(student_id, student_name)
        self.__save()

    def remove_student(self, student_id):
        """
        The function that removes a student from the list, and saves the list to the file
        :param student_id: the id of the student to be removed
        :return: nothing, the list is modified
        """
        super().remove_student(student_id)
        self.__save()

    def update_student(self, student_id, new_name):
        """
        The function that updates a student's name, and saves the list to the file
        :param student_id: the id of the student to be updated
        :param new_name: the new name of the student with the given id
        :return: nothing, the list is modified
        """
        super().update_student(student_id, new_name)
        self.__save()


class Disciplines_Binary_Repository(Disciplines_Memory_Repository):
    def __init__(self, initial_list: list, file_name: str):
        super().__init__(initial_list)
        self.__file_name = file_name
        with open(self.__file_name, "rb") as file:
            if file.read(1):
                self.__load()
            else:
                self.__save()

    def __load(self):
        """
        The function that loads the disciplines from the file
        :return: nothing, the list is modified
        """
        try:
            file_in = open(self.__file_name, "rb")
            self._data = load(file_in)
            file_in.close()
        except FileNotFoundError as fnf_error:
            self._data = []
            raise ValueError(fnf_error)

    def __save(self):
        """
        The function that saves the disciplines to the file
        :return: nothing, the list is modified
        """
        file_out = open(self.__file_name, "wb")
        dump(self._data, file_out)
        file_out.close()

    def add_discipline(self, discipline_id, discipline_name):
        """
        The function that adds a discipline to the list, and saves the list to the file
        :param discipline_id: the id of the discipline(should be unique)
        :param discipline_name: the name of the discipline
        :return: nothing, the list is modified
        """
        super().add_discipline(discipline_id, discipline_name)
        self.__save()

    def remove_discipline(self, discipline_id):
        """
        The function that removes a discipline from the list, and saves the list to the file
        :param discipline_id: the id of the discipline to be removed
        :return: nothing, the list is modified
        """
        super().remove_discipline(discipline_id)
        self.__save()

    def update_discipline(self, discipline_id, new_name):
        """
        The function that updates a discipline's name, and saves the list to the file
        :param discipline_id: the id of the discipline to be updated
        :param new_name: the new name of the discipline with the given id
        :return: nothing, the list is modified
        """
        super().update_discipline(discipline_id, new_name)
        self.__save()


class Grades_Binary_Repository(Grades_Memory_Repository):
    def __init__(self, initial_list: list, file_name: str):
        super().__init__(initial_list)
        self.__file_name = file_name
        with open(self.__file_name, "rb") as file:
            if file.read(1):
                self.__load()
            else:
                self.__save()

    def __load(self):
        try:
            with open(self.__file_name, "rb") as file_in:
                self._data = load(file_in)
        except FileNotFoundError as fnf_error:
            self._data = []
            raise ValueError(fnf_error)

    def __save(self):
        with open(self.__file_name, "wb") as file_out:
            dump(self._data, file_out)

    def add_grade(self, grade: Grade):
        super().add_grade(grade)
        self.__save()

    def remove_discipline_grades(self, discipline_id: int) -> None:
        super().remove_discipline_grades(discipline_id)
        self.__save()

    def remove_student_grades(self, student_id: int) -> None:
        super().remove_student_grades(student_id)
        self.__save()
