from data_objects.branch import Branch


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
        res_commit = self.__current_branch.get_current_commit().previous_commit
        self.__current_branch.set_current_commit(res_commit)
