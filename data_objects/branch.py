import configparser
import os
import shutil

import difflib

from shutil import copyfile

from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class Branch:

    def __init__(self, name):
        self.name = name
        self.current_commit_number = None
        self.config = configparser.ConfigParser()

    def set_current_commit(self, commit):
        """Sets current commit"""
        self.load_config()
        if commit is None:
            self.current_commit_number = ''
            self.config['info']['current_commit_number'] = ''
        else:
            self.current_commit_number = commit.commit_number
            self.config['info']['current_commit_number'] = commit.commit_number
        self.save_config()

    def get_current_commit(self):
        """
        Returns current commit
        :returns current commit
        """
        self.load_config()
        if self.current_commit_number == '':
            return None
        commit = Commit.make_commit_from_config(self.current_commit_number,
                                                self.name)
        return commit

    def update(self, filename, version):
        found_number = self.find_commit_file_version_number(filename,
                                                            version)
        if found_number == '':
            return
        di = DirectoryInfo()
        branch_path = di.get_commits_path(self.name)
        commit_path = os.path.join(branch_path, found_number)
        file_repo = os.path.join(commit_path, filename)
        file_origin = os.path.join(di.working_path, filename)
        copyfile(file_repo, file_origin)
        print(f'File {filename} version is now {version}')

    def find_commit_file_version_number(self, filename, version):
        self.load_config()
        current_commit = self.get_current_commit()
        found_number = current_commit.search_file_commit_number(filename,
                                                                version)
        if found_number == '':
            print(f'No file {filename} with version {version} found.')
        return found_number

    def diff(self, filename, first_version, second_version):
        di = DirectoryInfo()
        first_number = self.find_commit_file_version_number(filename,
                                                            first_version)
        second_number = self.find_commit_file_version_number(filename,
                                                             second_version)
        if first_number == '' or second_number == '':
            return
        branch_path = di.get_commits_path(self.name)
        first_commit_path = os.path.join(branch_path, first_number)
        second_commit_path = os.path.join(branch_path, second_number)

        first_file_path = os.path.join(first_commit_path, filename)
        second_file_path = os.path.join(second_commit_path, filename)

        first_file = open(first_file_path).readlines()
        second_file = open(second_file_path).readlines()

        print('_' * 40)
        print(f'Diff between {filename}: {first_version} and {second_version}')

        for line in difflib.unified_diff(first_file, second_file):
            print(line)

    def copy_to_branch(self, name):
        self.load_config()
        di = DirectoryInfo()
        from_commits_path = di.get_commits_path(self.name)
        to_branch_path = di.get_commits_path(name)
        if os.path.exists(to_branch_path):
            shutil.rmtree(to_branch_path)
        shutil.copytree(from_commits_path, to_branch_path)
        branch_to = Branch(name)
        branch_to.init_config()
        branch_to.set_current_commit(self.get_current_commit())

    def load_config(self):
        di = DirectoryInfo()
        config_path = os.path.join(di.get_branch_path(self.name), 'branch.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str
        self.config = config
        self.get_data_from_config(config_path)

    @staticmethod
    def make_branch_from_config(branch_name):
        di = DirectoryInfo()
        branch_path = di.get_branch_path(branch_name)
        path = os.path.join(branch_path, 'branch.ini')
        branch = Branch(branch_name)
        branch.get_data_from_config(path)
        return branch

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str

        commit_number = config['info']['current_commit_number']
        self.current_commit_number = commit_number
        self.name = config['info']['name']

    def save_config(self):
        di = DirectoryInfo()
        config_path = os.path.join(di.get_branch_path(self.name), 'branch.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        di = DirectoryInfo()
        path = os.path.join(di.get_branch_path(self.name), 'branch.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['name'] = self.name
        config['info']['current_commit_number'] = ''
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
