from cvs_trees.head import Head
from data_objects.branch import Branch
from data_objects.commit import Commit
from shutil import copyfile
import os

from data_objects.directory_info import DirectoryInfo


class Repository:

    def __init__(self):
        self.current_branch = Branch("NONE")
        self.last_commit = Commit("NONE")
        self.head = Head()
        self.directory = DirectoryInfo()

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets directory info"""
        self.directory = directory_info

    def add_commit(self, commit):
        """Adds new commit to lst branch, copying files"""
        if self.last_commit is None:
            self.last_commit = commit
        for file, path in commit.files_with_copying_paths:
            commit_path = self.directory.get_commits_path(
                self.current_branch.name)
            copy_path = os.path.join(commit_path, file)
            copyfile(path, copy_path)
        commit.set_previous_commit(self.last_commit)
        self.last_commit = commit
        self.current_branch.set_current_commit(commit)

    def reset_head(self):
        """Resets head"""
        self.head.reset()

    def point_to_last_commit(self):
        """Points to last commit"""
        self.current_branch.set_current_commit(self.last_commit)

    def init(self):
        """Initializes repository with master branch"""
        self.current_branch = Branch("master")
        self.head.set_branch(self.current_branch)

    def get_commit_history(self):
        self.last_commit.print_info()
