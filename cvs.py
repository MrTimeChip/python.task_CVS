from cvs_trees.index import Index
from cvs_trees.working_directory import WorkingDirectory
from data_objects.branch import Branch
from data_objects.directory_info import DirectoryInfo
from data_objects.repostitory import Repository


class CVS:

    def __init__(self):
        self.repository = Repository()
        self.index = Index()
        self.working_directory = WorkingDirectory()
        self.directory = DirectoryInfo()

    def init(self, path):
        """Initializes new repository at given path"""
        self.directory.init(path)
        self.index.init_config()
        self.index.set_directory_info(self.directory)

        self.repository.init()
        self.working_directory.init_config()
        self.working_directory.find_not_indexed_files(self.index.indexed_files)
        print(f'Working path is {path}')
        print(f'CVS path is {self.directory.cvs_path}')

    def add(self, filename):
        """Adds file to index"""
        self.index.add_new_file(filename)

    def commit(self, commit_message):
        """Makes new commit"""
        if len(self.index.indexed_files) == 0:
            print('No changes detected!')
            return
        branch_name = self.repository.current_branch.name
        print('commit is at ' + branch_name)
        commit = self.index.make_commit(commit_message, branch_name)
        self.repository.add_commit(commit)

    def update(self, filename, version):
        """Updates file with a specific version from repository"""
        branch_name = self.repository.current_branch.name
        branch = Branch.make_branch_from_config(branch_name)
        branch.update(filename, version)

    def branch(self, name):
        self.repository.make_branch(name)

    def branches(self):
        di = DirectoryInfo()
        di.print_branches()

    def checkout(self, branch_name):
        di = DirectoryInfo()
        if not di.branch_exists(branch_name):
            print(f'No branch {branch_name} exists!')
        self.repository.set_current_branch_name(branch_name)
        print(f'Current branch is {branch_name}')

    def reset(self, mode):
        """Resets current cvs state"""
        if mode == 'soft':
            self.soft_reset()
            return
        if mode == 'mixed' or mode == '':
            self.mixed_reset()
            return
        if mode == 'hard':
            self.hard_reset()

    def soft_reset(self):
        """Resets head"""
        self.repository.reset_head()

    def mixed_reset(self):
        """Resets head and index"""
        if self.repository.reset_head():
            self.index.reset(self.repository.head)

    def hard_reset(self):
        """Resets head, index and rewrites files in working path"""
        if self.repository.reset_head():
            self.index.reset(self.repository.head)
            self.working_directory.reset(self.index)

    def log(self):
        """
        Returns commit history at current branch
        :returns commit history string
        """
        self.repository.get_commit_history()
