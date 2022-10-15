import unittest

import helper
from dashboard.EtihadDb import EtihadDb


class MyTestCase(unittest.TestCase):
    def test_something(self):
        db = EtihadDb("db.db")
        db.create_db()
        db.add_file("file1", "abcd")
        db.add_file("file2", "abcd")
        db.add_file("file3", "abcd")
        db.add_file("file4", "abcd")
        result = db.get_file_list()
        self.assertEqual([('file1', 'abcd'), ('file2', 'abcd'), ('file3', 'abcd'), ('file4', 'abcd')] , result)

    def test_prepare_data(self):
        db = EtihadDb("db.db")
        db.create_db()
        db.add_file("CPM1.txt", helper.load_file_simple("../test/data/CPM1.txt"))
        db.add_file("CPM2.txt", helper.load_file_simple("../test/data/CPM2.txt"))

        result = db.get_file_list()

    def test_create_empty(self):
        db = EtihadDb("db.db")
        db.create_db()

if __name__ == '__main__':
    unittest.main()
