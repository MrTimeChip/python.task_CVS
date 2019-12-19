import configparser
import os
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
        self.load_config()
        current_commit = self.get_current_commit()
        found_number = current_commit.search_file_commit_number(filename,
                                                                version)
        if found_number == '':
            print(f'No file {filename} with version {version} found.')
            return
        di = DirectoryInfo()
        branch_path = di.get_commits_path(self.name)
        commit_path = os.path.join(branch_path, found_number)
        file_repo = os.path.join(commit_path, filename)
        file_origin = os.path.join(di.working_path, filename)
        copyfile(file_repo, file_origin)
        print(f'File {filename} version is now {version}')

    def load_config(self):
        di = DirectoryInfo()
        di.init(os.getcwd())
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
        di.init(os.getcwd())
        config_path = os.path.join(di.get_branch_path(self.name), 'branch.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        di = DirectoryInfo()
        di.init(os.getcwd())
        path = os.path.join(di.get_branch_path(self.name), 'branch.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['name'] = self.name
        config['info']['current_commit_number'] = ''
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
