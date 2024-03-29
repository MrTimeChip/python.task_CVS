import os
import unittest

from data_objects.directory_info import DirectoryInfo


class DirectoryInfoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.info = DirectoryInfo()
        self.info.init(os.getcwd())

    def test_init_should_initialize_working_path(self):
        result = self.info.working_path
        self.assertIsNotNone(result)

    def test_init_should_initialize_cvs_path(self):
        result = self.info.cvs_path
        self.assertTrue(result.endswith('CVS'))

    def test_init_should_initialize_index_path(self):
        result = self.info.index_path
        self.assertTrue(result.endswith('INDEX'))

    def test_add_branch_path_should_add_path_to_branch(self):
        self.info.add_branch_path("master")
        count = len(self.info.branches_paths)
        self.assertGreater(count, 0)

    def test_add_branch_path_should_add_path_to_commits(self):
        self.info.add_branch_path("master")
        count = len(self.info.branches_commits_paths)
        self.assertGreater(count, 0)

    def test_get_branch_path_should_get_path_to_branch(self):
        self.info.add_branch_path("master")
        path = self.info.get_branch_path("master")
        self.assertTrue(path.endswith("master"))

    def test_get_commits_path_should_get_commits_path(self):
        self.info.add_branch_path("master")
        path = self.info.get_commits_path("master")
        self.assertTrue(path.endswith("COMMITS"))


if __name__ == '__main__':
    unittest.main()
