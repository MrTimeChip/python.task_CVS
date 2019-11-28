import os
import shutil
import unittest

from cvs_trees.index import Index
from data_objects.directory_info import DirectoryInfo
from data_objects.repostitory import Repository


class TestRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.di = DirectoryInfo()
        path = os.path.join(os.getenv('APPDATA'), 'TESTING')
        self.di.set_custom_path(path)
        self.di.init()
        self.di.add_branch_path('master')
        if not os.path.exists(path):
            os.makedirs(path)
        self.file_path = os.path.join(self.di.working_path, 'TESTING.txt')
        with open(self.file_path, "w+") as file:
            file.write('SOME STRING')
        self.rep = Repository()
        self.rep.set_directory_info(self.di)
        self.rep.init()

    def tearDown(self) -> None:
        if os.path.exists(self.di.cvs_path):
            shutil.rmtree(self.di.cvs_path)

    def test_add_commit__should_copy_commit_files(self):
        index = Index()
        index.set_directory_info(self.di)
        index.add_new_file('TESTING.txt')
        self.rep.add_commit(index.make_commit('Testing commit'))
        commits_path = self.di.get_commits_path('master')
        full_path = os.path.join(commits_path, 'TESTING.txt')
        self.assertTrue(os.path.exists(full_path))


if __name__ == '__main__':
    unittest.main()