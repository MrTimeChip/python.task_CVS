import configparser
import copy
import os
from shutil import copyfile

from cvs_trees.head import Head
from data_objects.commit import Commit
from data_objects.directory_info import DirectoryInfo


class Index:

    def __init__(self):
        self.__indexed_files = set()
        self.__last_commit = None
        self.__directory = DirectoryInfo()
        self.config = configparser.ConfigParser()

    @property
    def indexed_files(self):
        return copy.copy(self.__indexed_files)

    @property
    def last_commit(self):
        return self.__last_commit

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets current __directory info"""
        self.__directory = directory_info

    def add_new_file(self, filename):
        """Adds new file, copying it to /CVS/INDEX/..."""
        self.load_config()
        if not self.__is_file_in_working_directory(filename):
            path = os.path.join(self.__directory.working_path,
                                filename)
            raise FileNotFoundError(f"No such file '{filename}' in '{path}'!")
        self.__indexed_files.add(filename)
        files = self.config['info']['files']
        self.config['info']['files'] = f'{files},{filename}'.strip(',')
        source_file = os.path.join(self.__directory.working_path, filename)
        file_copy = os.path.join(self.__directory.index_path, filename)
        copyfile(source_file, file_copy)
        print(f'File {source_file} added')
        self.save_config()

    def __is_file_in_working_directory(self, filename) -> bool:
        """Checks if file is in working __directory"""
        return os.path.exists(os.path.join(self.__directory.working_path,
                                           filename))

    def make_commit(self, commit_message, branch_name) -> Commit:
        """
        Makes commit, freezing current files state
        :returns Commit
        """
        self.load_config()
        commit = Commit(commit_message)
        commit.branch_name = branch_name
        commit.freeze_files(self.__indexed_files, self.__directory)
        self.__last_commit = commit
        self.config['info']['files'] = ''
        self.config['info']['last_commit'] = commit.commit_number
        self.config['info']['last_commit_branch'] = commit.branch_name
        self.save_config()
        return commit

    def reset(self, head: Head):
        """Resets index to last commit that head is pointing to"""
        self.load_config()
        commit = head.current_branch.get_current_commit()
        print('Index reset')
        for file in commit.files:
            branch_name = head.current_branch.name
            commits_path = self.__directory.get_commits_path(branch_name)
            commit_path = os.path.join(commits_path, commit.commit_number)
            source_path = os.path.join(commit_path, file)
            copy_path = os.path.join(self.__directory.index_path, file)
            copyfile(source_path, copy_path)
            print(f'Copied file from {source_path} to {copy_path}')
        self.__indexed_files = commit.files
        conf_files = ''
        for file in commit.files:
            conf_files += file
        self.config['info']['files'] = conf_files.strip(',')
        self.__last_commit = commit
        self.config['info']['last_commit'] = commit.commit_number
        self.config['info']['last_commit_branch'] = commit.branch_name
        self.save_config()

    def load_config(self):
        di = DirectoryInfo()
        di.init(os.getcwd())
        config_path = os.path.join(di.index_path, 'index.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str
        self.config = config
        self.get_data_from_config(config_path)

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str

        prev_commit_number = self.config['info']['last_commit']
        prev_commit_branch = self.config['info']['last_commit_branch']
        if prev_commit_number != 'None':
            commit = Commit.make_commit_from_config(prev_commit_number,
                                                    prev_commit_branch)
        else:
            commit = 'None'
        self.__last_commit = commit
        files = config['info']['files']
        if files != '':
            self.__indexed_files = set(files.split(','))

    def save_config(self):
        di = DirectoryInfo()
        di.init(os.getcwd())
        config_path = os.path.join(di.index_path, 'index.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        di = DirectoryInfo()
        di.init(os.getcwd())
        path = os.path.join(di.index_path, 'index.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['last_commit'] = 'None'
        config['info']['last_commit_branch'] = 'None'
        config['info']['files'] = ''
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
