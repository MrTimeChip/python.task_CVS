import unittest

from cvs_trees.head import Head
from data_objects.branch import Branch
from data_objects.commit import Commit


class TestHead(unittest.TestCase):

    def test_reset_should_move_head_to_previous_commit(self):
        head = Head()
        head.current_branch = Branch('master')
        commit = Commit('first')
        commit.previous_commit = Commit('second')
        head.current_branch.current_commit = commit
        head.reset()
        self.assertEqual(head.current_branch.current_commit,
                         commit.previous_commit)


if __name__ == '__main__':
    unittest.main()
