import os
import shutil
import unittest

from cvs_trees.index import Index
from cvs_trees.working_directory import WorkingDirectory
from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class TestCommit(unittest.TestCase):

    def setUp(self) -> None:
        self.commit = Commit("NONE")
        self.wd = WorkingDirectory()
        self.di = DirectoryInfo()
        path = os.path.join(os.getcwd(), 'TESTING')
        self.di.init(path)
        self.file_path = os.path.join(self.di.working_path, 'TESTING.txt')
        with open(self.file_path, "w+") as file:
            file.write('SOME STRING')
        self.wd.set_directory_info(self.di)

    def tearDown(self) -> None:
        if os.path.exists(self.di.cvs_path):
            shutil.rmtree(self.di.cvs_path)

    def test_freeze_files_should_remember_copy_path_of_indexed_files(self):
        index = Index()
        index.set_directory_info(self.di)
        index.add_new_file('TESTING.txt')
        self.commit.freeze_files(index.indexed_files, self.di)
        keys = self.commit.files_with_copying_paths.keys()
        self.assertTrue('TESTING.txt' in keys)

    def test_freeze_files_should_make_hash_from_indexed_files(self):
        index = Index()
        index.set_directory_info(self.di)
        index.add_new_file('TESTING.txt')
        self.commit.freeze_files(index.indexed_files, self.di)
        path = self.commit.files_with_copying_paths['TESTING.txt']
        keys = self.commit.files_hashes.keys()
        self.assertTrue(path in keys)

    def test_commit_number_should_return_unique_commit_number(self):
        first_number = self.commit.commit_number
        other_commit = Commit("Other")
        second_number = other_commit.commit_number
        self.assertNotEqual(first_number, second_number)


if __name__ == '__main__':
    unittest.main()
