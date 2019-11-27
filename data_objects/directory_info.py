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

    def init(self):
        """Initializes paths"""
        self.working_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__),
                         '..'))
        self.cvs_path = os.path.join(self.working_path, "CVS")
        self.index_path = os.path.join(self.cvs_path, "INDEX")

    def add_branch_path(self, branch_name):
        """Adds branch to paths"""
        path_to_branch = os.path.join(self.cvs_path, branch_name)
        self.__branches_paths[branch_name] = path_to_branch
        path_to_commits = os.path.join(self.cvs_path,
                                       branch_name + "\\COMMITS")
        self.__branches_commits_paths[branch_name] = path_to_commits

    def get_branch_path(self, branch_name) -> str:
        """Returns branch path"""
        if branch_name not in self.__branches_paths.keys():
            raise ValueError("No branch found!")
        return self.__branches_paths[branch_name]

    def get_commits_path(self, branch_name) -> str:
        """Return commits path for branch"""
        if branch_name not in self.__branches_paths.keys():
            raise ValueError("No branch found!")
        return self.__branches_commits_paths[branch_name]
