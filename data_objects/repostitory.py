from cvs_trees.head import Head
from data_objects.branch import Branch
from data_objects.commit import Commit
from shutil import copyfile
import os

from data_objects.directory_info import DirectoryInfo


class Repository:

    def __init__(self):
        self.current_branch = None
        self.last_commit_number = "NONE"
        self.head = Head()
        self.directory = DirectoryInfo()

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets directory info"""
        self.directory = directory_info

    def add_commit(self, commit):
        """Adds new commit to last branch, copying files"""
        for file in commit.files_with_copying_paths:
            path = commit.files_with_copying_paths[file]
            commits_path = self.directory.get_commits_path(
                self.current_branch.name)
            commit_path = os.path.join(commits_path, commit.commit_number)
            if not os.path.exists(commit_path):
                os.makedirs(commit_path)
            copy_path = os.path.join(commit_path, file)
            copyfile(path, copy_path)
            file_hash = commit.files_hashes[file]
            print(f'File {file} saved - {file_hash}')
        commit.set_previous_commit_number(self.last_commit_number)
        self.last_commit_number = commit.commit_number
        self.current_branch.set_current_commit(commit)

    def reset_head(self):
        """Resets head"""
        self.head.reset()

    def point_to_last_commit(self):
        """Points to last commit"""
        last_commit_number = Commit.make_commit_from_config(self.last_commit_number,
                                                     self.current_branch.name)
        self.current_branch.set_current_commit(last_commit_number)

    def init(self):
        """Initializes repository with master branch"""
        self.current_branch = Branch('master')
        self.current_branch.init_config()
        self.directory.add_branch_path('master')
        self.head.init_config()
        self.head.current_branch = self.current_branch

    def get_commit_history(self):
        print('sss')
        #self.last_commit_number.print_info()
