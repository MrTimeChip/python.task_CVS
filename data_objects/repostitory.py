import configparser

from cvs_trees.head import Head
from data_objects.branch import Branch
from data_objects.commit import Commit
from shutil import copyfile
import os

from data_objects.directory_info import DirectoryInfo


class Repository:

    def __init__(self):
        self.__current_branch_name = ""
        self.last_commit_number = ''
        self.config = configparser.ConfigParser()
        self.head = Head()
        self.directory = DirectoryInfo()

    @property
    def current_branch(self):
        self.load_config()
        return Branch.make_branch_from_config(self.__current_branch_name)

    def set_current_branch_name(self, name):
        self.load_config()
        self.config['info']['current_branch'] = name
        branch = Branch.make_branch_from_config(name)
        commit = branch.get_current_commit()
        if commit is None:
            self.config['info']['last_commit'] = ''
        else:
            self.config['info']['last_commit'] = commit.commit_number
        self.save_config()

    def set_directory_info(self, directory_info: DirectoryInfo):
        """Sets directory info"""
        self.directory = directory_info

    def add_commit(self, commit):
        """Adds new commit to last branch, copying files"""
        di = DirectoryInfo()
        self.load_config()
        for file in commit.files_with_copying_paths:
            path = commit.files_with_copying_paths[file]
            commits_path = di.get_commits_path(
                self.__current_branch_name)
            commit_path = os.path.join(commits_path, commit.commit_number)
            if not os.path.exists(commit_path):
                os.makedirs(commit_path)
            copy_path = os.path.join(commit_path, file)
            copyfile(path, copy_path)
            file_hash = commit.files_hashes[file]
            print(f'File {file} saved - {file_hash}')
        commit.set_previous_commit_number(self.last_commit_number)
        self.last_commit_number = commit.commit_number
        self.config['info']['last_commit'] = commit.commit_number
        branch = Branch.make_branch_from_config(self.__current_branch_name)
        branch.set_current_commit(commit)
        self.save_config()

    def reset_head(self):
        """Resets head"""
        self.load_config()
        self.head.reset()

    def init(self):
        """Initializes repository with master branch"""
        branch = Branch('master')
        branch.init_config()
        self.__current_branch_name = 'master'
        self.head.init_config()
        self.head.current_branch = branch
        self.init_config()

    def make_branch(self, name):
        self.load_config()
        di = DirectoryInfo()
        if di.branch_exists(name):
            print(f'Branch \'{name}\' already exists!')
            return
        di.add_branch_path(name)
        self.current_branch.copy_to_branch(name)
        print(f'Successfully made branch {name}')

    def get_commit_history(self):
        self.load_config()
        print(f'Commit history for branch: {self.__current_branch_name}')
        if self.last_commit_number != '':
            commit = Commit.make_commit_from_config(self.last_commit_number,
                                                    self.__current_branch_name)
            commit.print_info()
        else:
            print('No commits found!')

    def load_config(self):
        di = DirectoryInfo()
        config_path = os.path.join(di.cvs_path, 'repository.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str
        self.config = config
        self.get_data_from_config(config_path)
        self.head = Head.make_head_from_config()

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str

        self.__current_branch_name = config['info']['current_branch']
        self.last_commit_number = config['info']['last_commit']

    def save_config(self):
        di = DirectoryInfo()
        config_path = os.path.join(di.cvs_path, 'repository.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        di = DirectoryInfo()
        path = os.path.join(di.cvs_path, 'repository.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['current_branch'] = self.__current_branch_name
        config['info']['last_commit'] = self.last_commit_number
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
