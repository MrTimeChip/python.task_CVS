import os
import shutil
import unittest

from cvs_trees.index import Index
from cvs_trees.working_directory import WorkingDirectory
from data_objects.directory_info import DirectoryInfo


class WorkingDirectoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.wd = WorkingDirectory()
        self.di = DirectoryInfo()
        path = os.getcwd()
        self.di.init(path)
        self.wd.init_config()
        self.file_path = os.path.join(self.di.working_path, 'TESTING.txt')
        with open(self.file_path, "w+") as file:
            file.write('SOME STRING')

    def tearDown(self) -> None:
        if os.path.exists(self.di.cvs_path):
            shutil.rmtree(self.di.cvs_path)
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def test_find_not_indexed_files_should_find_when_empty_indexed(self):
        self.wd.find_not_indexed_files(set())
        self.assertGreater(len(self.wd.not_indexed_files), 0)

    def test_find_not_indexed_files_should_return_files_in_working_path(self):
        self.wd.find_not_indexed_files(set())
        result = self.wd.not_indexed_files
        self.assertTrue("TESTING.txt" in result)

    def test_reset_should_rewrite_files_from_index(self):
        index = Index()
        index.init_config()
        index.set_directory_info(self.di)
        index.add_new_file('TESTING.txt')
        os.remove(self.file_path)
        self.wd.reset(index)
        self.assertTrue(os.path.exists(self.file_path))


if __name__ == '__main__':
    unittest.main()
