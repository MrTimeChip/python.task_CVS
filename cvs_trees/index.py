import copy
import os
from shutil import copyfile

from cvs_trees.head import Head
from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class Index:

    def __init__(self):
        self.__indexed_files = set()
        self.__last_commit = None
        self.__directory = DirectoryInfo()

    @property
    def indexed_files(self):
        return copy.copy(self.__indexed_files)

    @property
    def last_commit(self):
        return self.__last_commit

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets current __directory info"""
        self.__directory = directory_info

    def add_new_file(self, filename):
        """Adds new file, copying it to /CVS/INDEX/..."""
        if not self.__is_file_in_working_directory(filename):
            raise FileNotFoundError("No such file in file __directory!")
        self.__indexed_files.add(filename)
        if not os.path.exists(self.__directory.index_path):
            os.makedirs(self.__directory.index_path)
        source_file = os.path.join(self.__directory.working_path, filename)
        file_copy = os.path.join(self.__directory.index_path, filename)
        copyfile(source_file, file_copy)

    def __is_file_in_working_directory(self, filename) -> bool:
        """Checks if file is in working __directory"""
        return os.path.exists(os.path.join(self.__directory.working_path,
                                           filename))

    def make_commit(self, commit_message) -> Commit:
        """
        Makes commit, freezing current files state
        :returns Commit
        """
        commit = Commit(commit_message)
        commit.freeze_files(self.__indexed_files, self.__directory)
        self.__last_commit = commit
        return commit

    def reset(self, head: Head):
        """Resets index to last commit, that head is pointing to"""
        commit = head.get_current_branch().current_commit
        self.__indexed_files = commit.__indexed_files
        self.__last_commit = commit
