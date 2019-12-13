import unittest
import shutil
import os

from cvs_trees.head import Head
from cvs_trees.index import Index
from data_objects.branch import Branch
from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class TestIndex(unittest.TestCase):

    def setUp(self) -> None:
        self.index = Index()
        self.di = DirectoryInfo()
        path = os.getcwd()
        self.di.init(path)
        self.file_path = os.path.join(self.di.working_path, 'TESTING.txt')
        with open(self.file_path, "w+") as file:
            file.write('SOME STRING')
        self.index.set_directory_info(self.di)

    def tearDown(self) -> None:
        if os.path.exists(self.di.cvs_path):
            shutil.rmtree(self.di.cvs_path)
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_add_new_file_raises_file_not_found_error_when_no_such_file(self):
        with self.assertRaises(FileNotFoundError):
            self.index.add_new_file("nosuchfile")

    def test_add_new_file_should_add_to_indexed_files_when_file_exists(self):
        self.index.add_new_file('TESTING.txt')
        count = len(self.index.indexed_files)
        self.assertGreater(count, 0)

    def test_add_new_file_should_copy_file_to_index_when_file_exists(self):
        self.index.add_new_file('TESTING.txt')
        full_path = os.path.join(self.di.working_path, 'TESTING.txt')
        file_exists = os.path.exists(full_path)
        self.assertTrue(file_exists)

    def test_make_commit_should_return_new_commit(self):
        self.index.add_new_file('TESTING.txt')
        commit = self.index.make_commit("new commit", 'master')
        self.assertIsNotNone(commit)

    def test_make_commit_should_set_last_commit(self):
        self.assertIsNone(self.index.last_commit)
        self.index.add_new_file('TESTING.txt')
        self.index.make_commit("new commit", 'master')
        self.assertIsNotNone(self.index.last_commit)

    def test_reset_should_reset_to_head_commit(self):
        head = Head()
        head.current_branch = Branch('master')
        commit = Commit('test')
        commit.branch_name = 'master'
        commit.init_config()
        head.current_branch.current_commit = commit
        self.index.reset(head)
        self.assertEqual(self.index.last_commit, commit)


if __name__ == '__main__':
    unittest.main()
