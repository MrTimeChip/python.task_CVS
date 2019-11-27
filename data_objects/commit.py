import hashlib
import os
import uuid

from data_objects.directory_info import DirectoryInfo


class Commit:

    def __init__(self, commit_message):
        self.commit_message = commit_message
        self.files = set()
        self.files_with_copying_paths = {}
        self.files_hashes = {}
        self.previous_commit = None
        self.commit_number = str(uuid.uuid4())

    def freeze_files(self, indexed_files, directory_info: DirectoryInfo):
        """Freezes indexed files, making hashes amd remembering their paths"""
        index_path = directory_info.index_path
        self.files = indexed_files
        for filename in indexed_files:
            file_path = os.path.join(index_path, filename)
            file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            self.files_with_copying_paths[filename] = file_path
            self.files_hashes[file_path] = file_hash

    def set_previous_commit(self, commit):
        """Sets previous commit"""
        self.previous_commit = commit

    def get_previous_commit(self):
        """
        Returns previous commit
        :return: previous commit
        """
        return self.previous_commit

    def get_commit_number(self):
        """Returns commit number"""
        return self.commit_number

    def get_copying_paths(self):
        """Returns copying paths"""
        return self.files_with_copying_paths

    def print_info(self):
        """Prints commit history, starting from this commit"""
        print(self.commit_number + '\n')
        print(self.commit_message + '\n')
        for file, hashcode in self.files_hashes:
            print(f'{hashcode} {file} \n')
        print("")
        if self.previous_commit is not None:
            self.previous_commit.print_info()
