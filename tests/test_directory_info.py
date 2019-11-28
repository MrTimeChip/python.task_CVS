import os
import unittest

from data_objects.directory_info import DirectoryInfo


class DirectoryInfoTest(unittest.TestCase):
    def setUp(self) -> None:
        self.info = DirectoryInfo()

    def test_init_should_initialize_working_path(self):
        self.info.init()
        result = self.info.working_path
        self.assertIsNotNone(result)

    def test_init_should_initialize_cvs_path(self):
        self.info.init()
        result = self.info.cvs_path
        self.assertTrue(result.endswith('CVS'))

    def test_init_should_initialize_index_path(self):
        self.info.init()
        result = self.info.index_path
        self.assertTrue(result.endswith('CVS\\INDEX'))

    def test_add_branch_path_should_add_path_to_branch(self):
        self.info.init()
        self.info.add_branch_path("master")
        count = len(self.info.branches_paths)
        self.assertGreater(count, 0)

    def test_add_branch_path_should_add_path_to_commits(self):
        self.info.init()
        self.info.add_branch_path("master")
        count = len(self.info.branches_commits_paths)
        self.assertGreater(count, 0)

    def test_get_branch_path_should_get_path_to_branch(self):
        self.info.init()
        self.info.add_branch_path("master")
        path = self.info.get_branch_path("master")
        self.assertTrue(path.endswith("CVS\\master"))

    def test_get_commits_path_should_get_commits_path(self):
        self.info.init()
        self.info.add_branch_path("master")
        path = self.info.get_commits_path("master")
        self.assertTrue(path.endswith("CVS\\master\\COMMITS"))

    def test_set_custom_path_should_set_custom_working_path(self):
        self.info.set_custom_path(os.getenv('APPDATA'))
        self.info.init()
        path = self.info.working_path
        self.assertEqual(path, os.getenv('APPDATA'))


if __name__ == '__main__':
    unittest.main()
