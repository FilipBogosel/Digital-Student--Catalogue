import unittest
from src.services.Services import Services
from src.repository.MemoryRepos import Students_Memory_Repository, Disciplines_Memory_Repository, Grades_Memory_Repository
from src.domain.Domain import Grade
from src.repository.MemoryRepos import Id_Error

class TestServices(unittest.TestCase):
    def setUp(self):
        self.student_repo = Students_Memory_Repository([])
        self.discipline_repo = Disciplines_Memory_Repository([])
        self.grade_repo = Grades_Memory_Repository([])
        self.services = Services(self.student_repo, self.discipline_repo, self.grade_repo)
        # Adding initial data
        self.student_repo.add_student(120, "John Doe")
        self.discipline_repo.add_discipline(220, "Mathematics")

    def test_grade_student(self):
        self.services.grade_student(120, 220, 9)
        grades = self.grade_repo.get_list_of_grades
        self.assertEqual(len(grades), 21)
        self.assertEqual(grades[-1].get_grade_value, 9)

    def test_remove_student_service(self):
        self.services.remove_student_service(120)
        with self.assertRaises(Id_Error):
            self.student_repo.find_by_id(120)
        grades = self.grade_repo.get_list_of_grades
        self.assertEqual(len(grades), 20)

    def test_remove_discipline_service(self):
        self.services.remove_discipline_service(220)
        with self.assertRaises(Id_Error):
            self.discipline_repo.find_by_id(220)
        grades = self.grade_repo.get_list_of_grades
        self.assertEqual(len(grades), 20)
    def test_get_students_failing(self):
        #take into consideration that the list is initialised with 20 grades, 8 of which are failing
        self.grade_repo.add_grade(Grade(119, 119, 4))
        self.assertEqual(len(self.services.get_students_failing()), 9)

    def test_get_best_students(self):
        # Adding grades for students
        self.grade_repo.add_grade(Grade(120, 220, 10))
        self.grade_repo.add_grade(Grade(120, 220, 9))
        self.grade_repo.add_grade(Grade(121, 220, 8))
        self.grade_repo.add_grade(Grade(121, 220, 7))
        self.student_repo.add_student(121, "Jane Doe")

        best_students = self.services.get_best_students()
        self.assertEqual(len(best_students), 2)
        self.assertEqual(best_students[0].get_student_id, 120)
        self.assertEqual(best_students[1].get_student_id, 121)

if __name__ == '__main__':
    unittest.main()