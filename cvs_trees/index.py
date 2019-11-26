import os
from shutil import copyfile

from cvs_trees.head import Head
from data_objects.commit import Commit


class Index:

    def __init__(self):
        self.working_path = ''
        self.cvs_path = ""
        self.index_path = ""
        self.indexed_files = set()
        self.last_commit = Commit("NONE")

    def set_working_path(self, path):
        self.working_path = path

    def set_cvs_path(self, path):
        self.cvs_path = path
        self.index_path = os.path.join(self.cvs_path, '/INDEX')

    def add_new_file(self, filename):
        if not self.is_file_in_working_directory(filename):
            raise FileNotFoundError("No such file in file directory!")
        self.indexed_files.add(filename)
        source_file = os.path.join(self.working_path, filename)
        file_copy = os.path.join(self.index_path, filename)
        copyfile(source_file, file_copy)

    def is_file_in_working_directory(self, filename) -> bool:
        return os.path.exists(os.path.join(self.working_path, filename))

    def make_commit(self, commit_message) -> Commit:
        commit = Commit(commit_message)
        commit.freeze_files(self.indexed_files, self.index_path)
        self.last_commit = commit
        return commit

    def reset(self, head: Head):
        commit = head.get_current_branch().current_commit
        self.indexed_files = commit.indexed_files
        self.last_commit = commit
