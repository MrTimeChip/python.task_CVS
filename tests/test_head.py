import os
import unittest

from cvs_trees.head import Head
from data_objects.branch import Branch
from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class TestHead(unittest.TestCase):

    def test_reset_should_move_head_to_previous_commit(self):
        di = DirectoryInfo()
        di.init(os.getcwd())
        head = Head()
        head.current_branch = Branch('master')
        commit = Commit('first')
        commit.branch_name = 'master'
        commit.init_config()
        prev_commit = Commit('second')
        prev_commit.branch_name = 'master'
        prev_commit.init_config()
        commit.set_previous_commit_number(prev_commit.commit_number)
        head.current_branch.set_current_commit(commit)
        head.reset()
        current_commit = head.current_branch.get_current_commit()
        self.assertEqual(current_commit.commit_number,
                         commit.get_previous_commit_number())


if __name__ == '__main__':
    unittest.main()
