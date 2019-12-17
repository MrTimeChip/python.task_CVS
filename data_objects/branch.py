import configparser
import os

from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class Branch:

    def __init__(self, name):
        self.name = name
        self.current_commit_number = None
        self.config = configparser.ConfigParser()

    def set_current_commit(self, commit):
        """Sets current commit"""
        self.current_commit_number = commit.commit_number

    def get_current_commit(self) -> Commit:
        """
        Returns current commit
        :returns current commit
        """
        commit = Commit.make_commit_from_config(self.current_commit_number,
                                                self.name)
        return commit

    def load_config(self):
        di = DirectoryInfo()
        di.init(os.getcwd())
        config_path = os.path.join(di.get_branch_path(self.name), 'branch.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str
        self.config = config
        self.get_data_from_config(config_path)

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str

        commit_number = self.config['info']['current_commit_number']
        if commit_number != 'None':
            commit = Commit.make_commit_from_config(commit_number,
                                                    self.name)
        else:
            commit = 'None'
        self.current_commit_number = commit

        self.name = self.config['info']['name']

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
        config['info']['current_commit_number'] = 'None'
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
