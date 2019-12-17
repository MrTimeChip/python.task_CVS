from data_objects.branch import Branch
from data_objects.commit import Commit


class Head:

    def __init__(self):
        self.__current_branch = Branch("NONE")

    @property
    def current_branch(self):
        return self.__current_branch

    @current_branch.setter
    def current_branch(self, value):
        self.__current_branch = value

    def reset(self):
        """Moves head to previous commit"""
        current_commit = self.__current_branch.get_current_commit()
        previous = current_commit.get_previous_commit()
        self.__current_branch.set_current_commit(previous)
        commit_number = previous.commit_number
        commit_message = previous.commit_message
        print(f'New head commit is {commit_number} {commit_message}')
