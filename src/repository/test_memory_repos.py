import unittest
from src.repository.MemoryRepos import Students_Memory_Repository, Disciplines_Memory_Repository, Id_Error
from src.domain.Domain import Student, Discipline

class TestStudentsMemoryRepository(unittest.TestCase):
    def setUp(self):
        self.repo = Students_Memory_Repository([])

    def test_add_student(self):
        self.repo.add_student(120, "John Doe")
        self.assertEqual(len(self.repo.get_list_of_students), 21)
        self.assertEqual(self.repo.get_list_of_students[-1].get_student_name, "John Doe")

    def test_add_student_with_existing_id(self):
        with self.assertRaises(Id_Error):
            self.repo.add_student(100, "Jane Doe")

    def test_remove_student(self):
        self.repo.remove_student(100)
        self.assertEqual(len(self.repo.get_list_of_students), 19)

    def test_remove_nonexistent_student(self):
        with self.assertRaises(Id_Error):
            self.repo.remove_student(999)

    def test_update_student(self):
        self.repo.update_student(100, "Updated Name")
        self.assertEqual(self.repo.get_list_of_students[0].get_student_name, "Updated Name")

    def test_update_nonexistent_student(self):
        with self.assertRaises(Id_Error):
            self.repo.update_student(999, "Nonexistent Name")


class TestDisciplinesMemoryRepository(unittest.TestCase):
    def setUp(self):
        self.repo = Disciplines_Memory_Repository([])

    def test_add_discipline(self):
        self.repo.add_discipline(120, "Mathematics")
        self.assertEqual(len(self.repo.get_list_of_disciplines), 21)
        self.assertEqual(self.repo.get_list_of_disciplines[-1].get_discipline_name, "Mathematics")

    def test_add_discipline_with_existing_id(self):
        with self.assertRaises(Id_Error):
            self.repo.add_discipline(100, "Physics")

    def test_remove_discipline(self):
        self.repo.remove_discipline(100)
        self.assertEqual(len(self.repo.get_list_of_disciplines), 19)

    def test_remove_nonexistent_discipline(self):
        with self.assertRaises(Id_Error):
            self.repo.remove_discipline(999)

    def test_update_discipline(self):
        self.repo.update_discipline(100, "Updated Discipline")
        self.assertEqual(self.repo.get_list_of_disciplines[0].get_discipline_name, "Updated Discipline")

    def test_update_nonexistent_discipline(self):
        with self.assertRaises(Id_Error):
            self.repo.update_discipline(999, "Nonexistent Discipline")


if __name__ == '__main__':
    unittest.main()