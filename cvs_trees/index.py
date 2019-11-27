import os
from shutil import copyfile

from cvs_trees.head import Head
from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class Index:

    def __init__(self):
        self.indexed_files = set()
        self.last_commit = Commit("NONE")
        self.directory = DirectoryInfo()

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets current directory info"""
        self.directory = directory_info

    def add_new_file(self, filename):
        """Adds new file, copying it to /CVS/INDEX/..."""
        if not self.is_file_in_working_directory(filename):
            raise FileNotFoundError("No such file in file directory!")
        self.indexed_files.add(filename)
        source_file = os.path.join(self.directory.working_path, filename)
        file_copy = os.path.join(self.directory.index_path, filename)
        copyfile(source_file, file_copy)

    def is_file_in_working_directory(self, filename) -> bool:
        """Checks if file is in working directory"""
        return os.path.exists(os.path.join(self.directory.working_path,
                                           filename))

    def make_commit(self, commit_message) -> Commit:
        """
        Makes commit, freezing current files state
        :returns Commit
        """
        commit = Commit(commit_message)
        commit.freeze_files(self.indexed_files, self.directory.index_path)
        self.last_commit = commit
        return commit

    def reset(self, head: Head):
        """Resets index to last commit, that head is pointing to"""
        commit = head.get_current_branch().current_commit
        self.indexed_files = commit.indexed_files
        self.last_commit = commit
