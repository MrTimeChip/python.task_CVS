import os
import shutil
import unittest

from cvs import CVS


class TestCVS(unittest.TestCase):
    def setUp(self) -> None:
        self.cvs = CVS()
        self.path = os.path.join(os.getcwd(), 'TESTING')
        self.file_path = os.path.join(self.path, 'TESTING.txt')
        with open(self.file_path, "w+") as file:
            file.write('SOME STRING')

    def tearDown(self) -> None:
        if os.path.exists(self.cvs.directory.cvs_path):
            shutil.rmtree(self.cvs.directory.cvs_path)

    def test_init_should_initialize_all_of_the_classes(self):
        self.cvs.init(self.path)
        not_indexed_files = self.cvs.working_directory.not_indexed_files
        self.assertTrue('TESTING.txt' in not_indexed_files)

    def test_add_should_add_file_to_index(self):
        self.cvs.init(self.path)
        self.cvs.add('TESTING.txt')
        self.assertTrue('TESTING.txt' in self.cvs.index.indexed_files)

    def test_commit_should_add_new_commit_to_repository(self):
        self.cvs.init(self.path)
        self.cvs.add('TESTING.txt')
        self.cvs.commit('New commit')
        self.assertEqual('New commit',
                         self.cvs.repository.last_commit.commit_message)

    def test_reset_should_make_soft_reset(self):
        self.cvs.init(self.path)
        self.cvs.add('TESTING.txt')
        self.cvs.commit('New commit')
        self.cvs.commit('Another commit')
        self.cvs.reset('--soft')
        current_commit = self.cvs.repository.head.current_branch.current_commit
        self.assertEqual('New commit', current_commit.commit_message)


if __name__ == '__main__':
    unittest.main()
