import os
from cvs_trees.index import Index
from cvs_trees.working_directory import WorkingDirectory
from data_objects.repostitory import Repository


class CVS:

    def __init__(self):
        self.repository = Repository()
        self.index = Index()
        self.working_directory = WorkingDirectory()
        self.working_path = ""

    def init(self):
        self.__get_working_path()
        self.repository.init()
        self.working_directory.set_working_path(self.working_path)
        self.index.set_working_path(self.working_path)
        self.working_directory.find_not_indexed_files(self.index.indexed_files)

    def add(self, filename):
        self.index.add_new_file(filename)

    def commit(self, commit_message):
        commit = self.index.make_commit(commit_message)
        self.repository.add_commit(commit)
        self.repository.point_to_last_commit()

    def reset(self, mode):
        if mode == '--soft':
            self.soft_reset()
            return
        if mode == '-mixed' or mode == '':
            self.mixed_reset()
            return
        if mode == '--hard':
            self.hard_reset()

    def soft_reset(self):
        self.repository.reset_head()

    def mixed_reset(self):
        self.repository.reset_head()
        self.index.reset(self.repository.head)

    def hard_reset(self):
        self.repository.reset_head()
        self.index.reset(self.repository.head)
        self.working_directory.reset()

    def log(self) -> str:
        return self.repository.get_commit_history()

    def __get_working_path(self):
        self.working_path = os.path.dirname(os.path.abspath(__file__))
