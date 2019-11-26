import os
from os.path import join
from shutil import copyfile

from cvs_trees.index import Index


class WorkingDirectory:

    def __init__(self):
        self.working_path = ""
        self.not_indexed_files = set()

    def set_working_path(self, path):
        self.working_path = path

    def find_not_indexed_files(self, indexed: set):
        for file in os.listdir(self.working_path):
            is_file = os.path.isfile(join(self.working_path, file))
            if is_file and file not in indexed:
                self.not_indexed_files.add(is_file)

    def reset(self, index: Index):
        for filename in index.indexed_files:
            file_indexed = os.path.join(index.index_path, filename)
            file_origin = os.path.join(self.working_path, filename)
            copyfile(file_indexed, file_origin)

