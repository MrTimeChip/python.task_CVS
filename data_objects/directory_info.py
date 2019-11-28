import copy
import os


class DirectoryInfo:

    def __init__(self):
        self.working_path = ""
        self.cvs_path = ""
        self.index_path = ""
        self.__branches_commits_paths = {}
        self.__branches_paths = {}

    @property
    def branches_paths(self):
        return copy.copy(self.__branches_paths)

    @property
    def branches_commits_paths(self):
        return copy.copy(self.__branches_commits_paths)

    def init(self, path):
        """Initializes paths"""
        self.working_path = path
        if not os.path.exists(path):
            os.makedirs(path)
        cvs_path_base = os.path.join(os.getenv('APPDATA'))
        self.cvs_path = os.path.join(cvs_path_base, "CVS")
        if not os.path.exists(self.cvs_path):
            os.makedirs(self.cvs_path)
        self.index_path = os.path.join(self.cvs_path, "INDEX")
        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)

    def add_branch_path(self, branch_name):
        """Adds branch to paths"""
        path_to_branch = os.path.join(self.cvs_path, branch_name)
        self.__branches_paths[branch_name] = path_to_branch
        if not os.path.exists(path_to_branch):
            os.makedirs(path_to_branch)
        path_to_commits = os.path.join(self.cvs_path,
                                       branch_name + "\\COMMITS")
        if not os.path.exists(path_to_commits):
            os.makedirs(path_to_commits)
        self.__branches_commits_paths[branch_name] = path_to_commits

    def get_branch_path(self, branch_name) -> str:
        """Returns branch path"""
        if branch_name not in self.__branches_paths.keys():
            raise ValueError(f"No branch found! {branch_name}")
        return self.__branches_paths[branch_name]

    def get_commits_path(self, branch_name) -> str:
        """Return commits path for branch"""
        if branch_name not in self.__branches_paths.keys():
            raise ValueError(f"No branch found! {branch_name}")
        return self.__branches_commits_paths[branch_name]
