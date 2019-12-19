import copy
import os
import configparser


class DirectoryInfo:

    def __init__(self):
        self.config = None
        self.__working_path = ""
        self.__cvs_path = ""
        self.__index_path = ""
        self.__branches_commits_paths = {}
        self.__branches_paths = {}

    @property
    def cvs_path(self):
        self.load_config()
        return self.__cvs_path

    @property
    def index_path(self):
        self.load_config()
        return self.__index_path

    @property
    def working_path(self):
        self.load_config()
        return self.__working_path

    @property
    def branches_paths(self):
        self.load_config()
        return copy.copy(self.__branches_paths)

    @property
    def branches_commits_paths(self):
        self.load_config()
        return copy.copy(self.__branches_commits_paths)

    def init(self, path):
        """Initializes paths"""
        self.__working_path = path
        if not os.path.exists(path):
            os.makedirs(path)
        self.__cvs_path = os.path.join(self.__working_path, ".CVS")
        if not os.path.exists(self.__cvs_path):
            os.makedirs(self.__cvs_path)
        self.__index_path = os.path.join(self.__cvs_path, "INDEX")
        if not os.path.exists(self.__index_path):
            os.makedirs(self.__index_path)
        self.init_config()
        self.add_branch_path('master')

    def add_branch_path(self, branch_name):
        """Adds branch to paths"""
        self.load_config()
        path_to_branch = os.path.join(self.__cvs_path, branch_name)
        self.config['branches'][branch_name] = path_to_branch
        self.__branches_paths[branch_name] = path_to_branch
        if not os.path.exists(path_to_branch):
            os.makedirs(path_to_branch)
        path_to_commits = os.path.join(self.__cvs_path, branch_name, "COMMITS")
        if not os.path.exists(path_to_commits):
            os.makedirs(path_to_commits)
        self.config['branches_commits'][branch_name] = path_to_commits
        self.__branches_commits_paths[branch_name] = path_to_commits
        self.save_config()

    def get_branch_path(self, branch_name) -> str:
        """Returns branch path"""
        self.load_config()
        if branch_name not in self.config['branches'].keys():
            raise ValueError(f"No branch found! {branch_name}")
        return self.config['branches'][branch_name]

    def get_commits_path(self, branch_name) -> str:
        """Return commits path for branch"""
        self.load_config()
        if branch_name not in self.config['branches'].keys():
            raise ValueError(f"No branch found! {branch_name}")
        return self.config['branches_commits'][branch_name]

    def branch_exists(self, name) -> bool:
        self.load_config()
        return name in self.__branches_paths.keys()

    def print_branches(self):
        self.load_config()
        print('_' * 40)
        print('Branches: ')
        for branch in self.__branches_paths.keys():
            print(f"\t{branch}")

    def load_config(self):
        cwd = os.getcwd()
        config_path = os.path.join(cwd, '.CVS', 'di.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str
        self.config = config
        self.get_data_from_config(config_path)

    def get_data_from_config(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)
        config.optionxform = str

        self.__working_path = config['info']['working_path']
        self.__cvs_path = config['info']['cvs_path']
        self.__index_path = config['info']['index_path']

        for name, path in config['branches'].items():
            self.__branches_paths[name] = path

        for name, path in config['branches_commits'].items():
            self.__branches_commits_paths[name] = path

    def save_config(self):
        cwd = os.getcwd()
        config_path = os.path.join(cwd, '.CVS', 'di.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        cwd = os.getcwd()
        path = os.path.join(cwd, '.CVS', 'di.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['working_path'] = self.__working_path
        config['info']['cvs_path'] = self.__cvs_path
        config['info']['index_path'] = self.__index_path
        config['branches'] = {}
        config['branches_commits'] = {}
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
