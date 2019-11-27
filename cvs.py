from cvs_trees.index import Index
from cvs_trees.working_directory import WorkingDirectory
from data_objects.directory_info import DirectoryInfo
from data_objects.repostitory import Repository


class CVS:

    def __init__(self):
        self.repository = Repository()
        self.index = Index()
        self.working_directory = WorkingDirectory()
        self.directory = DirectoryInfo()

    def init(self):
        """Initializes new repository at current directory"""
        self.repository.init()
        self.directory.init()
        self.index.set_directory_info(self.directory)
        self.repository.set_directory_info(self.directory)
        self.working_directory.find_not_indexed_files(self.index.indexed_files)

    def add(self, filename):
        """Adds file to index"""
        self.index.add_new_file(filename)

    def commit(self, commit_message):
        """Makes new commit"""
        commit = self.index.make_commit(commit_message)
        self.repository.add_commit(commit)
        self.repository.point_to_last_commit()

    def reset(self, mode):
        """Resets current cvs state"""
        if mode == '--soft':
            self.soft_reset()
            return
        if mode == '-mixed' or mode == '':
            self.mixed_reset()
            return
        if mode == '--hard':
            self.hard_reset()

    def soft_reset(self):
        """Resets head"""
        self.repository.reset_head()

    def mixed_reset(self):
        """Resets head and index"""
        self.repository.reset_head()
        self.index.reset(self.repository.head)

    def hard_reset(self):
        """Resets head, index and rewrites files in working path"""
        self.repository.reset_head()
        self.index.reset(self.repository.head)
        self.working_directory.reset(self.index)

    def log(self):
        """
        Returns commit history at current branch
        :returns commit history string
        """
        self.repository.get_commit_history()
