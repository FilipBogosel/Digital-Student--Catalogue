import unittest

from src.repository.TextFileRepos import Students_TextFile_Repository, Disciplines_TextFile_Repository, \
    Grades_TextFile_Repository
from src.repository.MemoryRepos import Id_Error

from src.domain.Domain import Student, Discipline, Grade
class Test_Students_TextFile_Repository(unittest.TestCase):
    def setUp(self):
        self.repo = Students_TextFile_Repository([], "D:\\Github\\Digital-Student--Catalogue\\src\\data\\students.txt")

    def test_add_student(self):
        self.repo.add_student(128, "John")
        self.assertEqual(self.repo.get_list_of_students[-1].get_student_name, "John")


    def test_add_student_with_existing_id(self):
        self.assertRaises(Id_Error, self.repo.add_student, 102, "John")

    def test_remove_student(self):
        length = len(self.repo.get_list_of_students)
        self.repo.remove_student(105)
        self.assertEqual(len(self.repo.get_list_of_students), length - 1)

    def test_remove_student_with_non_existing_id(self):
        self.assertRaises(Id_Error, self.repo.remove_student, 300)

    def test_update_student(self):
        self.repo.update_student(107, "Alex")
        self.assertEqual(self.repo.find_by_id(107).get_student_name, "Alex")

    def test_update_student_with_non_existing_id(self):
        self.assertRaises(Id_Error, self.repo.update_student, 210, "Alex")

class Test_Disciplines_TextFile_Repository(unittest.TestCase):
    def setUp(self):
        self.repo = Disciplines_TextFile_Repository([], "D:\\Github\\Digital-Student--Catalogue\\src\\data\\disciplines.txt")

    def test_add_discipline(self):
        self.repo.add_discipline(127, "Math")
        self.assertEqual(self.repo.get_list_of_disciplines[-1].get_discipline_name, "Math")

    def test_add_discipline_with_existing_id(self):
        self.assertRaises(Id_Error, self.repo.add_discipline, 102, "Math")

    def test_remove_discipline(self):
        length = len(self.repo.get_list_of_disciplines)
        self.repo.remove_discipline(105)
        self.assertEqual(len(self.repo.get_list_of_disciplines), length - 1)

    def test_remove_discipline_with_non_existing_id(self):
        self.assertRaises(Id_Error, self.repo.remove_discipline, 300)

    def test_update_discipline(self):
        self.repo.update_discipline(107, "Physics")
        self.assertEqual(self.repo.find_by_id(107).get_discipline_name, "Physics")

    def test_update_discipline_with_non_existing_id(self):
        self.assertRaises(Id_Error, self.repo.update_discipline, 210, "Physics")

if __name__ == '__main__':
    unittest.main()
