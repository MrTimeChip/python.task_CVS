from cvs_trees.head import Head
from cvs_trees.index import Index
from cvs_trees.working_directory import WorkingDirectory
from data_objects.commit import Commit
from data_objects.repostitory import Repository


class CVS:

    def __init__(self):
        self.repository = Repository()
        self.head = Head()
        self.index = Index()
        self.working_directory = WorkingDirectory()

    def init(self):
        self.repository.init(self.head)
        self.working_directory.find_not_indexed_files()

    def add(self, filename):
        self.index.add_new_file(filename)

    def commit(self, commit_message):
        commit = Commit(commit_message)
        commit.copy_from_index(self.index)
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
        self.head.reset()

    def mixed_reset(self):
        self.head.reset()
        self.index.reset()

    def hard_reset(self):
        self.head.reset()
        self.index.reset()
        self.head.reset()

    def log(self) -> str:
        return self.repository.get_commit_history()
