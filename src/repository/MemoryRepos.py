from faker import Faker
from src.domain.Domain import Student, Discipline, Grade


class Id_Error(Exception):
    def __init__(self, message="Invalid ID provided"):
        self.message = message
        super().__init__(self.message)


class Grade_Error(Exception):
    def __init__(self):
        self.message = "Invalid grade provided, must be an integer between 1 and 10"
        super().__init__(self.message)


class Students_Memory_Repository:
    def __init__(self, previous: list):
        self._data = previous
        self.initialize_list_with_20()

    # we will use faker to generate random names
    def initialize_list_with_20(self) -> None:
        fake = Faker()
        if len(self._data) == 0:
            for i in range(20):
                self._data.append(Student(100 + i, fake.name()))

    @property
    def get_list_of_students(self) -> list:
        return self._data.copy()

    def add_student(self, student_id: int, student_name: str) -> None:
        """
        The function that adds a student to the list
        :param student_id: the id of the student(should be unique)
        :param student_name: student's name
        :return: nothing, the list is modified
        :raises: Id_Error if the student with the given id does
        """
        for student in self._data:
            if student.get_student_id == student_id:
                raise Id_Error("The ID is already taken")
        student = Student(student_id, student_name)
        self._data.append(student)

    def remove_student(self, student_id: int) -> None:
        """
        The function that removes a student from the list
        :param student_id: the id of the student
        :return: nothing, the list is modified
        :raises: Id_Error if the student with the given id does
        """
        found = False
        for student in self._data:
            if student.get_student_id == student_id:
                self._data.remove(student)
                found = True
                break
        if not found:
            raise Id_Error("The student with given ID does not exist")

    def update_student(self, student_id: int, new_student_name: str) -> None:
        """
        The function that updates a student's name
        :param student_id: the id of the student
        :param new_student_name: the new name of the student
        :return: nothing, the list is modified
        :raises: Id_Error if the student with the given id does
        """
        found = False
        for student in self._data:
            if student.get_student_id == student_id:
                student.set_student_name(new_student_name)
                found = True
                break
        if not found:
            raise Id_Error("The student with given ID does not exist")

    def find_by_id(self, student_id: int) -> Student:
        """
        The function that finds a student by its id
        :param student_id: The id of the student
        :return: the student with the given id
        :raises: Id_Error if the student with the given id does not exist
        """
        for student in self._data:
            if student.get_student_id == student_id:
                return student
        raise Id_Error("The student with given ID does not exist")


class Disciplines_Memory_Repository:
    def __init__(self, previous: list):
        self._data = previous
        self.initialize_list_with_20()

    def initialize_list_with_20(self) -> None:
        disciplines = [
            "Mathematics", "Physics", "Chemistry", "Biology", "History",
            "Geography", "English", "Literature", "Art", "Music",
            "Physical Education", "Computer Science", "Economics", "Philosophy",
            "Psychology", "Sociology", "Political Science", "Environmental Science",
            "Foreign Languages", "Health Education"
        ]
        if len(self._data) == 0:
            for i in range(20):
                self._data.append(Discipline(100 + i, disciplines[i]))

    @property
    def get_list_of_disciplines(self) -> list:
        return self._data.copy()

    def add_discipline(self, discipline_id: int, discipline_name: str) -> None:
        """
        The function that adds a discipline to the list
        :param discipline_id: the id of the discipline(should be unique)
        :param discipline_name: discipline's name
        :return: nothing, the list is modified
        :raises: Id_Error if the discipline with the given id does
        """
        for discipline in self._data:
            if discipline.get_discipline_id == discipline_id:
                raise Id_Error("The ID is already taken")
        discipline = Discipline(discipline_id, discipline_name)
        self._data.append(discipline)

    def remove_discipline(self, discipline_id: int) -> None:
        """
        The function that removes a discipline from the list
        :param discipline_id: the id of the discipline
        :return: nothing, the list is modified
        :raises: Id_Error if the discipline with the given id does
        """
        found = False
        for discipline in self._data:
            if discipline.get_discipline_id == discipline_id:
                self._data.remove(discipline)
                found = True
                break
        if not found:
            raise Id_Error("The discipline with given ID does not exist")

    def update_discipline(self, discipline_id: int, new_discipline_name: str) -> None:
        """
        The function that updates a discipline's name
        :param discipline_id: the id of the discipline
        :param new_discipline_name: the new name of the discipline
        :return: nothing, the list is modified
        :raises: Id_Error if the discipline with the given id does not exist
        """
        found = False
        for discipline in self._data:
            if discipline.get_discipline_id == discipline_id:
                discipline.set_discipline_name(new_discipline_name)
                found = True
                break
        if not found:
            raise Id_Error("The discipline with given ID does not exist")

    def find_by_id(self, discipline_id: int) -> Discipline:
        """
        The function that finds a discipline by its id
        :param discipline_id: The id of the discipline
        :return: the discipline with the given id
        :raises: Id_Error if the discipline with the given id does not exist
        """
        for discipline in self._data:
            if discipline.get_discipline_id == discipline_id:
                return discipline
        raise Id_Error("The discipline with given ID does not exist")


class Grades_Memory_Repository:
    def __init__(self, previous: list):
        self._data = previous
        self.initialize_list_with_20()

    def initialize_list_with_20(self) -> None:
        if len(self._data) == 0:
            for i in range(20):
                self._data.append(Grade(100 + i, 100 + i, i % 10 + 1))

    @property
    def get_list_of_grades(self) -> list:
        return self._data.copy()

    def remove_student_grades(self, student_id: int) -> None:
        """
        The function that removes all the grades of a student
        :param student_id: the id of the student
        :return: nothing, the list is modified
        """
        for grade in self._data:
            if grade.get_student_id == student_id:
                self._data.remove(grade)

    def remove_discipline_grades(self, discipline_id: int) -> None:
        """
        The function that removes all the grades of a discipline
        :param discipline_id: the id of the discipline
        :return: nothing, the list is modified
        """
        for grade in self._data:
            if grade.get_discipline_id == discipline_id:
                self._data.remove(grade)

    def add_grade(self, grade: Grade) -> None:
        """
        The function that adds a grade to the list
        :param grade: the grade to be added
        :return: nothing, the list is modified
        """
        if grade.get_grade_value < 1 or grade.get_grade_value > 10:
            raise Grade_Error()
        self._data.append(grade)

    def remove_grade(self, grade: Grade) -> None:
        """
        The function that removes a grade from the list
        :param grade: the grade to be removed
        :return: nothing, the list is modified
        """
        for g in self._data:
            if g.get_student_id == grade.get_student_id and g.get_discipline_id == grade.get_discipline_id:
                self._data.remove(g)
                break

    def get_average_grade_at_discipline(self, student_id, discipline_id):
        summ = 0
        grades_counter = 0
        for grade in self._data:
            if grade.get_student_id == student_id and grade.get_discipline_id == discipline_id:
                summ += grade.get_grade_value
                grades_counter += 1

        if grades_counter == 0:
            return 0

        return summ // grades_counter

    def get_discipline_status(self, discipline_id):
        total_grades = 0
        grade_count = 0
        for grade in self._data:
            if grade.get_discipline_id == discipline_id:
                grade_count += 1
                total_grades += grade.get_grade_value

        if grade_count == 0:
            return 0

        average_status = total_grades / grade_count
        return average_status

    def find_by_student_id(self, student_id):
        """
        The function that finds all the grades of a student by its id
        :param student_id: The id of the student
        :return: a list of all the grades of the student
        """
        grades = []
        for grade in self._data:
            if grade.get_student_id == student_id:
                grades.append(grade)
        return grades

    def find_by_discipline_id(self, discipline_id):
        """
        The function that finds all the grades of a discipline by its id
        :param discipline_id: The id of the discipline
        :return: a list of all the grades of the discipline
        """
        grades = []
        for grade in self._data:
            if grade.get_discipline_id == discipline_id:
                grades.append(grade)
        return grades


if __name__ == '__main__':
    initial_data = []
    repo = Students_Memory_Repository(initial_data)
    for student in repo.get_list_of_students:
        print(student)
