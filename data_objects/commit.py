import configparser
import copy
import hashlib
import os
import shutil
import uuid
import datetime

from data_objects.directory_info import DirectoryInfo


class Commit:

    def __init__(self, commit_message):
        self.config = configparser.ConfigParser()
        self.commit_message = commit_message
        self.branch_name = ''
        self.__files = set()
        self.__files_with_copying_paths = {}
        self.__files_hashes = {}
        self.__files_versions = {}
        self.__previous_commit_number = ''
        self.__commit_number = str(uuid.uuid4())
        self.__time = ''

    @property
    def files(self):
        self.load_config()
        return copy.copy(self.__files)

    @property
    def files_with_copying_paths(self):
        self.load_config()
        return copy.copy(self.__files_with_copying_paths)

    @property
    def files_hashes(self):
        self.load_config()
        return copy.copy(self.__files_hashes)

    @property
    def files_versions(self):
        self.load_config()
        return copy.copy(self.__files_versions)

    def freeze_files(self, indexed_files, directory_info: DirectoryInfo):
        """Freezes indexed files making hashes amd remembering their paths"""
        self.load_config()
        index_path = directory_info.index_path
        self.__files = indexed_files
        for filename in indexed_files:
            file_path = os.path.join(index_path, filename)
            file_hash = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            self.config['copy'][filename] = file_path
            self.config['hash'][filename] = file_hash
            self.config['versions'][filename] = self.get_file_version(filename)
        self.save_config()
        self.load_config()

    def get_file_version(self, filename) -> str:
        prev_commit_number = self.__previous_commit_number
        if prev_commit_number == '':
            return '1.0'

        prev_commit = Commit.make_commit_from_config(prev_commit_number,
                                                     self.branch_name)

        if filename in prev_commit.files_versions.keys():
            version = float(prev_commit.files_versions[filename]) + 0.1
            return "{:.1f}".format(version)
        return '1.0'

    def set_previous_commit_number(self, commit: str):
        """Sets previous commit"""
        self.load_config()
        self.config['info']['previous'] = commit
        self.save_config()

    def get_previous_commit_number(self):
        """Sets previous commit"""
        self.load_config()
        return self.config['info']['previous']

    def get_previous_commit(self):
        """
        Returns previous commit
        :return: previous commit
        """
        self.load_config()
        if self.__previous_commit_number == '':
            return None
        commit = self.make_commit_from_config(self.__previous_commit_number,
                                              self.branch_name)
        return commit

    @property
    def commit_number(self):
        """Returns commit number"""
        return self.__commit_number

    def load_config(self):
        di = DirectoryInfo()
        commits = di.get_commits_path(self.branch_name)
        path = os.path.join(commits, self.commit_number, 'commit.ini')
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(path)
        self.config = config
        self.get_data_from_config(path)

    def save_config(self):
        di = DirectoryInfo()
        commits = di.get_commits_path(self.branch_name)
        path = os.path.join(commits, self.commit_number, 'commit.ini')
        with open(path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        di = DirectoryInfo()
        commits = di.get_commits_path(self.branch_name)
        fullpath = os.path.join(commits, self.commit_number)
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        path = os.path.join(fullpath, 'commit.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['branch'] = self.branch_name
        config['info']['message'] = self.commit_message
        config['info']['number'] = self.commit_number
        config['info']['previous'] = self.__previous_commit_number

        config['info']['time'] = str(datetime.datetime.now())

        config['copy'] = {}
        for file, file_path in self.__files_with_copying_paths.items():
            config['copy'][file] = file_path

        config['hash'] = {}
        for file, hashcode in self.__files_hashes.items():
            config['hash'][file] = hashcode

        config['versions'] = {}
        for file, version in self.__files_versions.items():
            config['versions'][file] = version

        open(path, 'a').close()
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.optionxform = str
        config.read(config_path)

        self.commit_message = config['info']['message']
        self.branch_name = config['info']['branch']

        self.__previous_commit_number = config['info']['previous']
        self.__commit_number = config['info']['number']

        self.__time = config['info']['time']

        self.__files = set()
        self.__files_with_copying_paths = {}
        self.__files_hashes = {}
        self.__files_versions = {}

        for file, path in config['copy'].items():
            self.__files.add(file)
            self.__files_with_copying_paths[file] = path

        for file, hashcode in config['hash'].items():
            self.__files_hashes[file] = hashcode

        for file, version in config['versions'].items():
            self.__files_versions[file] = version

    @staticmethod
    def make_commit_from_config(commit_number, branch_name):
        di = DirectoryInfo()
        commits = di.get_commits_path(branch_name)
        path = os.path.join(commits, commit_number, 'commit.ini')
        commit = Commit('none')
        commit.branch_name = branch_name
        commit.get_data_from_config(path)
        return commit

    def delete_commit(self):
        di = DirectoryInfo()
        commits = di.get_commits_path(self.branch_name)
        fullpath = os.path.join(commits, self.commit_number)
        if os.path.exists(fullpath):
            shutil.rmtree(fullpath)

    def print_info(self):
        """Prints commit history, starting from this commit"""
        self.load_config()
        print('_' * 40)
        print(f'{self.commit_number} \n')
        print(f'Time: {self.__time}\n')
        print(f'Message:\n \t{self.commit_message} \n')
        for file in self.__files_hashes:
            hashcode = self.__files_hashes[file]
            version = self.__files_versions[file]
            print(f'{hashcode} {file} {version}\n')
        if self.__previous_commit_number != '':
            prev_commit_number = self.__previous_commit_number
            prev_commit = self.make_commit_from_config(prev_commit_number,
                                                       self.branch_name)
            prev_commit.print_info()
