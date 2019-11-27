from data_objects.branch import Branch


class Head:

    def __init__(self):
        self.current_branch = Branch("NONE")

    def set_branch(self, branch: Branch):
        """Sets current branch"""
        self.current_branch = branch

    def get_current_branch(self) -> Branch:
        """
        Returns current branch
        :returns current branch
        """
        return self.current_branch

    def reset(self):
        """Moves head to previous commit"""
        prev_commit = self.current_branch.get_current_commit().previous_commit
        self.current_branch.set_current_commit(prev_commit)
        self.current_branch = prev_commit
