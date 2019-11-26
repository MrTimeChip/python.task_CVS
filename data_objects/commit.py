import hashlib
import os


class Commit:

    def __init__(self, commit_message):
        self.commit_message = commit_message
        self.files = set()
        self.files_paths = set()
        self.files_hashes = {}

    def freeze_files(self, index_files, index_path):
        self.files = index_files
        for filename in index_files:
            file_path = os.path.join(index_path, filename)
            self.files_paths.add(file_path)
            file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            self.files_hashes[file_path] = file_hash

    def set_previous_commit(self, commit):
        pass

    def get_previous_commit(self):
        pass

    def get_commit_number(self):
        pass

    def print_info(self):
        pass
