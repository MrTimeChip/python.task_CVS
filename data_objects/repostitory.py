from data_objects.branch import Branch
from data_objects.commit import Commit


class Repository:

    def __init__(self):
        self.current_branch = Branch("NONE")
        self.last_commit = Commit("NONE")

    def add_commit(self, commit):
        if self.last_commit is None:
            self.last_commit = commit
            return
        commit.set_previous_commit(self.last_commit)
        self.last_commit = commit

    def point_to_last_commit(self):
        self.current_branch.set_current_commit(self.last_commit)

    def init(self, head):
        self.current_branch = Branch("master")
        head.set_branch(self.current_branch)

    def get_commit_history(self) -> str:
        return self.last_commit.print_info()