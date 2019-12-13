import unittest

from cvs_trees.head import Head
from data_objects.branch import Branch
from data_objects.commit import Commit


class TestHead(unittest.TestCase):

    def test_reset_should_move_head_to_previous_commit(self):
        head = Head()
        head.current_branch = Branch('master')
        commit = Commit('first')
        commit.branch_name = 'master'
        commit.init_config()
        prev_commit = Commit('second')
        prev_commit.branch_name = 'master'
        prev_commit.init_config()
        commit.set_previous_commit_number(prev_commit.commit_number)
        head.current_branch.current_commit = commit
        head.reset()
        self.assertEqual(head.current_branch.current_commit.commit_number,
                         commit.previous_commit_number)


if __name__ == '__main__':
    unittest.main()
