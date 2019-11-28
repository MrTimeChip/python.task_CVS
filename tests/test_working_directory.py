import unittest

from cvs_trees.working_directory import WorkingDirectory
from data_objects.directory_info import DirectoryInfo


class WorkingDirectoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wd = WorkingDirectory()
        di = DirectoryInfo()
        di.init()
        self.wd.set_directory_info(di)

    def test_find_not_indexed_files_should_find_when_empty_indexed(self):
        self.wd.find_not_indexed_files(set())
        self.assertGreater(len(self.wd.not_indexed_files), 0)

    def test_find_not_indexed_files_should_return_files_in_working_path(self):
        self.wd.find_not_indexed_files(set())
        result = self.wd.not_indexed_files
        self.assertTrue("cvs.py" in result)

    #TODO: write reset test


if __name__ == '__main__':
    unittest.main()
