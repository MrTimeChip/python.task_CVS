import configparser
import os

from data_objects.branch import Branch
from data_objects.directory_info import DirectoryInfo


class Head:

    def __init__(self):
        self.__current_branch_name = 'None'
        self.config = configparser.ConfigParser()

    @property
    def current_branch(self):
        self.load_config()
        branch = Branch.make_branch_from_config(self.__current_branch_name)
        return branch

    @current_branch.setter
    def current_branch(self, value):
        self.load_config()
        self.__current_branch_name = value.name
        self.config['info']['current_branch'] = self.__current_branch_name
        self.save_config()

    def reset(self):
        """Moves head to previous commit"""
        self.load_config()
        branch = Branch(self.__current_branch_name)
        current_commit = branch.get_current_commit()
        previous = current_commit.get_previous_commit()
        if previous is None:
            branch.set_current_commit(None)
            print(f'Commits fully reset: no commits anymore')
            return
        branch.set_current_commit(previous)
        commit_number = previous.commit_number
        commit_message = previous.commit_message
        print(f'New head commit is {commit_number} {commit_message}')

    @staticmethod
    def make_head_from_config():
        di = DirectoryInfo()
        path = os.path.join(di.cvs_path, 'head.ini')
        head = Head()
        head.get_data_from_config(path)
        return head

    def load_config(self):
        di = DirectoryInfo()
        config_path = os.path.join(di.cvs_path, 'head.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str
        self.config = config
        self.get_data_from_config(config_path)

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str

        self.__current_branch_name = config['info']['current_branch']

    def save_config(self):
        di = DirectoryInfo()
        config_path = os.path.join(di.cvs_path, 'head.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        di = DirectoryInfo()
        path = os.path.join(di.cvs_path, 'head.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['current_branch'] = self.__current_branch_name
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
