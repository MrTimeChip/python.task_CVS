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
        previous = self.__current_branch.current_commit.get_previous_commit()
        res_commit = Commit.make_commit_from_config(previous.commit_number,
                                                    self.current_branch.name)
        self.__current_branch.current_commit = res_commit
        commit_number = res_commit.commit_number
        commit_message = res_commit.commit_message
        print(f'New head commit is {commit_number} {commit_message}')
