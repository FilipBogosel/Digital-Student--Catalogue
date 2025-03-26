import unittest

from src.repository.BinaryRepos import Students_Binary_Repository, Disciplines_Binary_Repository, Grades_Binary_Repository
from src.repository.MemoryRepos import Id_Error


class Test_Students_Binary_Repository(unittest.TestCase):
    def setUp(self):
        self.repo = Students_Binary_Repository([], "D:\\Github\\Digital-Student--Catalogue\\src\\data\\students.bin")

    def test_add_student(self):
        length = len(self.repo.get_list_of_students)
        self.repo.add_student(1000, "John")
        self.assertEqual(len(self.repo.get_list_of_students), length + 1)
        self.assertEqual(self.repo.get_list_of_students[-1].get_student_id, 1000)
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


class Test_Disciplines_Binary_Repository(unittest.TestCase):
    def setUp(self):
        self.repo = Disciplines_Binary_Repository([], "D:\\Github\\Digital-Student--Catalogue\\src\\data\\disciplines.bin")

    def test_add_discipline(self):
        length = len(self.repo.get_list_of_disciplines)
        self.repo.add_discipline(1000, "Math")
        self.assertEqual(len(self.repo.get_list_of_disciplines), length + 1)
        self.assertEqual(self.repo.get_list_of_disciplines[-1].get_discipline_id, 1000)
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

