import os


class DirectoryInfo:

    def __init__(self):
        self.working_path = ""
        self.cvs_path = ""
        self.index_path = ""
        self.branches_commits_path = {}
        self.branches_path = {}

    def init(self):
        self.working_path = os.path.dirname(os.path.abspath(__file__))
        self.cvs_path = os.path.join(self.working_path, "/CVS")
        self.index_path = os.path.join(self.cvs_path, "/INDEX")

    def add_branch_path(self, branch_name):
        path_to_branch = os.path.join(self.cvs_path, "/" + branch_name)
        self.branches_path = path_to_branch
        path_to_commits = os.path.join(self.cvs_path,
                                       "/" + branch_name + "/COMMITS")
        self.branches_commits_path[branch_name] = path_to_commits

    def get_branch_path(self, branch_name):
        if branch_name not in self.branches_path.keys():
            raise ValueError("No branch found!")
        return self.branches_path[branch_name]

    def get_commits_path(self, branch_name):
        if branch_name not in self.branches_path.keys():
            raise ValueError("No branch found!")
        return self.branches_commits_path[branch_name]

