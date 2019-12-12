import copy
import os
import configparser


class DirectoryInfo:

    def __init__(self):
        self.config = None
        self.working_path = ""
        self.cvs_path = ""
        self.index_path = ""
        self.__branches_commits_paths = {}
        self.__branches_paths = {}

    @property
    def branches_paths(self):
        return copy.copy(self.__branches_paths)

    @property
    def branches_commits_paths(self):
        return copy.copy(self.__branches_commits_paths)

    def init(self, path):
        """Initializes paths"""
        self.working_path = path
        if not os.path.exists(path):
            os.makedirs(path)
        self.cvs_path = os.path.join(self.working_path, ".CVS")
        if not os.path.exists(self.cvs_path):
            os.makedirs(self.cvs_path)
        self.index_path = os.path.join(self.cvs_path, "INDEX")
        if not os.path.exists(self.index_path):
            os.makedirs(self.index_path)
        self.init_config()

    def add_branch_path(self, branch_name):
        """Adds branch to paths"""
        self.load_config()
        path_to_branch = os.path.join(self.cvs_path, branch_name)
        self.config['branches'][branch_name] = path_to_branch
        if not os.path.exists(path_to_branch):
            os.makedirs(path_to_branch)
        path_to_commits = os.path.join(self.cvs_path, branch_name, "COMMITS")
        if not os.path.exists(path_to_commits):
            os.makedirs(path_to_commits)
        self.config['branches_commits'][branch_name] = path_to_commits
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

    def load_config(self):
        cwd = os.getcwd()
        config_path = os.path.join(cwd, '.CVS', 'di.ini')
        config = configparser.ConfigParser()
        config.read(config_path)
        self.config = config
        self.load_config_values()

    def load_config_values(self):
        self.working_path = self.config['info']['working_path']
        self.cvs_path = self.config['info']['cvs_path']
        self.index_path = self.config['info']['index_path']

        for name, path in self.config['branches'].items():
            self.branches_paths[name] = path

        for name, path in self.config['branches_commits'].items():
            self.branches_commits_paths[name] = path

    def save_config(self):
        config_path = os.path.join(self.cvs_path, 'di.ini')
        with open(config_path, 'w') as f:
            self.config.write(f)

    def init_config(self):
        path = os.path.join(self.cvs_path, 'di.ini')

        config = configparser.ConfigParser()
        config['info'] = {}
        config['info']['working_path'] = self.working_path
        config['info']['cvs_path'] = self.cvs_path
        config['info']['index_path'] = self.index_path
        config['branches'] = {}
        config['branches_commits'] = {}
        with open(path, 'w') as cfg_file:
            config.write(cfg_file)
