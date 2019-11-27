from data_objects.branch import Branch


class Head:

    def __init__(self):
        self.current_branch = Branch("NONE")

    def set_branch(self, branch: Branch):
        self.current_branch = branch

    def get_current_branch(self) -> Branch:
        return self.current_branch

    def reset(self):
        prev_commit = self.current_branch.get_current_commit().previous_commit
        self.current_branch = prev_commit
