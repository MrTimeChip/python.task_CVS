import os
from os.path import join
from shutil import copyfile

from cvs_trees.index import Index
from data_objects.directory_info import DirectoryInfo


class WorkingDirectory:

    def __init__(self):
        self.not_indexed_files = set()
        self.directory = DirectoryInfo()

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets current directory info"""
        self.directory = directory_info

    def find_not_indexed_files(self, indexed: set):
        """Finds not indexed files"""
        for file in os.listdir(self.directory.working_path):
            is_file = os.path.isfile(join(self.directory.working_path, file))
            if is_file and file not in indexed:
                self.not_indexed_files.add(is_file)

    def reset(self, index: Index):
        """Rewrites file in current working directory"""
        for filename in index.indexed_files:
            file_indexed = os.path.join(self.directory.index_path, filename)
            file_origin = os.path.join(self.directory.working_path, filename)
            copyfile(file_indexed, file_origin)

