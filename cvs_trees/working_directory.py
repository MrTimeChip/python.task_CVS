import copy
import os
from os.path import join
from shutil import copyfile

from cvs_trees.index import Index
from data_objects.directory_info import DirectoryInfo


class WorkingDirectory:

    def __init__(self):
        self.__not_indexed_files = set()
        self.__directory = DirectoryInfo()

    @property
    def not_indexed_files(self):
        return copy.copy(self.__not_indexed_files)

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets current __directory info"""
        self.__directory = directory_info

    def find_not_indexed_files(self, indexed: set):
        """Finds not indexed files"""
        for file in os.listdir(self.__directory.working_path):
            is_file = os.path.isfile(join(self.__directory.working_path, file))
            if is_file and file not in indexed:
                self.__not_indexed_files.add(file)

    def reset(self, index: Index):
        """Rewrites file in current working __directory"""
        print('Working directory reset')
        for filename in index.indexed_files:
            file_indexed = os.path.join(self.__directory.index_path, filename)
            file_origin = os.path.join(self.__directory.working_path, filename)
            copyfile(file_indexed, file_origin)
            print(f'Copied file from {file_indexed} to {file_origin}')

